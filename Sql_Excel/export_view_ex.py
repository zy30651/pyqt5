import datetime

from PyQt5.QtGui import QColor
import pymysql
pymysql.install_as_MySQLdb()
from Sql_Excel import export_view
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
import pandas as pd
import openpyxl

db_server = "rm-2zeal9um71e33a491.mysql.rds.aliyuncs.com"
user = "mtoliv"
pwd = "Renee2020Tom"
db_name = "oliveperson"
port = 3306
school_dict = {'全部校区': '',
               '顺义校区':'7210',
               '回龙观校区': '5b5874f13327b0e479137421',
               '和平里校区':'5d47a588db25b0e4fbe77a67',
               '蓝港校区': '5c00da2f7507b0e4012d0877',
               '八大关校区':'5c259a7572b9b0e4e4dacd60',
               '常营校区': '7310',
               }

class ExportViewEx(QtWidgets.QMainWindow, export_view.Ui_MainWindow):
    _signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(ExportViewEx, self).__init__(parent)
        # 加入vpn运行
        self.__index = 0
        self.conn = None
        self.setupUi(self)
        self.update_ui()

    def update_ui(self):
        tab_bar = self.view_sel.tabBar()
        tab_bar.setTabTextColor(0, QColor(0, 0, 0))
        tab_bar.setTabTextColor(1, QColor(0, 0, 0))
        tab_bar.setTabTextColor(2, QColor(0, 0, 0))
        self.export_btn_card.clicked.connect(self.export_card_fun)
        self.export_btn_order.clicked.connect(self.export_order_fun)
        self.export_btn_flow.clicked.connect(self.export_flow_fun)
        tab_bar.setCurrentIndex(0)

        self.connect_mysql()


    def connect_mysql(self):
        try:
            self.conn = pymysql.connect(
                host=db_server,
                port=port,
                passwd=pwd,
                user=user,
                db=db_name,
                charset="utf8")
            print('数据库连接成功 %s'% self.conn)
        except BaseException as e:
            print(e)
            QMessageBox.about(self, '连接失败', str(e))
        finally:
            print(self.conn.cursor())

    def export_card_fun(self):
        school = self.sel_school_card
        sql_test = '''
        SELECT id, name From oliveperson.t_ethnic_group
        '''
        sql = '''SELECT
                if(organization.`name` is not null, organization.`name`, '顺义校区'),
                person.given_name_oriental,
                customer.customer_code,
                contact_info.contact_info,
              student.student_name,
                payment_method.`name`,
                receipt.receivables
            FROM	olivesps.t_receipt receipt
            LEFT JOIN oliveorder.t_payment_method payment_method ON receipt.receipt_type_id = payment_method.id
            LEFT JOIN olivecustomer.t_c_customer c_customer ON receipt.parent_id = c_customer.person_id
            LEFT JOIN olivecustomer.t_customer customer ON c_customer.id = customer.id
            LEFT JOIN oliveperson.t_person person ON c_customer.person_id = person.id
            LEFT JOIN olivecontactinfo.t_contact_info contact_info ON contact_info.owner_id = person.id
            LEFT JOIN olivesps.t_school_student student ON student.parent_id = c_customer.person_id
            LEFT JOIN oliveorganization.t_organization organization ON student.org_id = organization.id
            WHERE	student.customer_id = 'YIJIE_2017_FAKE' and receipt.receivables > 0
            GROUP BY organization.`name`,person.given_name_oriental,customer.customer_code,payment_method.`name`
            ORDER BY
                organization.`name`,
                person.given_name_oriental,
                customer.customer_code,
                payment_method.`name`'''

        cursor = self.conn.cursor()
        try:
            cursor.execute(sql_test)
            data = cursor.fetchall()
            df = pd.DataFrame(data)
            header = []
            i = 0
            count = len(cursor.description)

            while i < count:
                header.insert(i, cursor.description[i][0])
                i+=1
            print(header)
            path = "./%s客户会籍卡余额.xlsx" % datetime.datetime.now().strftime("%Y-%m-%d")
            df.to_excel(path, encoding="utf_8_sig", header=header)

        except BaseException as e:
            print(e)
            QMessageBox.about(self, 'error', str(e))
        finally:
            self.conn.commit()
            cursor.close()

    def export_order_fun(self):
        # warm 读取参数，放入SQL语句
        # 时间 估计能能剪切sql语句，才能拼接时间
        start_time = self.start_time_order.text()
        end_time = self.end_time_order.text()

        print("%s   ->  %s" %  (start_time, end_time))
        if self.cardSelBtn_order.isChecked():
            print("购卡退卡明细")
            school = self.sel_school_card
            sql_test = '''
                    SELECT id, name From oliveperson.t_ethnic_group
                    '''
            sql = '''
                    SELECT
                        t3.`name`,
                        t3.`日期`,
                        t3.seq_number,
                        t3.`摘要`,
                        t3.given_name_oriental,
                        t3.`客户编码`,
                        t3.`学生`,
                        t3.`实收金额`,
                        t3.`赠送金额`,
                        t3.name2,
                        t3.remarks,
                        t3.given_name_oriental2,
                        t3.`购课数量` 
                    FROM
                        (
                    SELECT
                        organization1.`name`,
                        date_format( voucher1.recording_time, '%Y-%m-%d' ) '日期',
                        voucher1.seq_number,
                        '购卡或充值' AS '摘要',
                        person1.given_name_oriental,
                        customer1.customer_code '客户编码',
                        student1.student_name '学生',
                        receipt_info.proceeds '实收金额',
                    IF
                        ( receipt_info.give_money IS NULL, 0, receipt_info.give_money ) AS '赠送金额',
                        payment_method1.`name` AS name2,
                        REPLACE ( REPLACE ( receipt_info.remark, CHAR ( 10 ), ' ' ), CHAR ( 13 ), ' ' ) AS remarks,
                    -- receipt_info.remark,
                        advisor1.given_name_oriental AS given_name_oriental2,
                        '' AS '购课数量',
                        voucher1.id 
                    FROM
                        oliveais.t_voucher voucher1
                        INNER JOIN olivesps.t_receipt_info receipt_info ON voucher1.id = receipt_info.voucher_id
                        LEFT JOIN olivesps.t_receipt receipt1 ON receipt1.id = receipt_info.receipt_id
                        LEFT JOIN oliveorder.t_payment_method payment_method1 ON receipt1.receipt_type_id = payment_method1.id
                        LEFT JOIN olivecustomer.t_c_customer c_customer1 ON receipt1.parent_id = c_customer1.person_id
                        LEFT JOIN olivecustomer.t_customer customer1 ON c_customer1.id = customer1.id
                        LEFT JOIN oliveperson.t_person person1 ON c_customer1.person_id = person1.id
                        LEFT JOIN olivesps.t_school_student student1 ON student1.parent_id = c_customer1.person_id
                        LEFT JOIN oliveorganization.t_organization organization1 ON voucher1.company_id = organization1.id
                        LEFT JOIN oliveuser.t_user user1 ON receipt_info.operational_advisor_id = user1.id
                        LEFT JOIN oliveperson.t_person advisor1 ON advisor1.id = user1.person_id 
                    WHERE
                        student1.customer_id = 'YIJIE_2017_FAKE' -- 	 DATE_SUB( CURDATE( ), INTERVAL 4 DAY ) < voucher1.recording_time AND
                    -- AND TO_DAYS( voucher1.recording_time ) = TO_DAYS( now( ) )
                        
                        AND voucher1.recording_time >= '2020-10-01 0:0:0' 
                        AND voucher1.recording_time < '2020-11-01 0:0:0' UNION ALL
                    SELECT
                        organization2.`name`,
                        date_format( voucher2.recording_time, '%Y-%m-%d' ) '日期',
                        voucher2.seq_number,
                        '退卡或退款' AS '摘要',
                        person2.given_name_oriental,
                        customer2.customer_code '客户编码',
                        student2.student_name '学生',
                        ( 0 - receipt_refund.refund_amount ) '实收金额',
                        0 AS '赠送金额',
                        payment_method2.`name` AS name2,
                        REPLACE ( REPLACE ( receipt_refund.remark, CHAR ( 10 ), '' ), CHAR ( 13 ), '' ),
                        advisor2.given_name_oriental AS given_name_oriental2,
                        '' AS '购课数量',
                        voucher2.id 
                    FROM
                        oliveais.t_voucher voucher2
                        INNER JOIN olivesps.t_receipt_refund receipt_refund ON voucher2.id = receipt_refund.voucher_id
                        LEFT JOIN olivesps.t_receipt receipt2 ON receipt2.id = receipt_refund.receipt_id
                        LEFT JOIN oliveorder.t_payment_method payment_method2 ON receipt2.receipt_type_id = payment_method2.id
                        LEFT JOIN olivecustomer.t_c_customer c_customer2 ON receipt2.parent_id = c_customer2.person_id
                        LEFT JOIN olivecustomer.t_customer customer2 ON c_customer2.id = customer2.id
                        LEFT JOIN oliveperson.t_person person2 ON c_customer2.person_id = person2.id
                        LEFT JOIN olivesps.t_school_student student2 ON student2.parent_id = c_customer2.person_id
                        LEFT JOIN oliveorganization.t_organization organization2 ON voucher2.company_id = organization2.id
                        LEFT JOIN oliveuser.t_user user2 ON receipt_refund.operational_advisor_id = user2.id
                        LEFT JOIN oliveperson.t_person advisor2 ON advisor2.id = user2.person_id 
                    WHERE
                        student2.customer_id = 'YIJIE_2017_FAKE' -- 	AND DATE_SUB( CURDATE( ), INTERVAL 4 DAY ) < voucher2.recording_time
                    -- AND TO_DAYS( voucher2.recording_time ) = TO_DAYS( now( ) )
                        
                        AND voucher2.recording_time >= '2020-10-01 0:0:0' 
                        AND voucher2.recording_time < '2020-11-01 0:0:0' 
                        ) t3 
                    GROUP BY
                        t3.id 
                    ORDER BY
                        t3.`name`,
                        t3.id,
                    t3.given_name_oriental'''

            cursor = self.conn.cursor()
            try:
                cursor.execute(sql_test)
                data = cursor.fetchall()
                df = pd.DataFrame(data)
                header = []
                i = 0
                count = len(cursor.description)

                while i < count:
                    header.insert(i, cursor.description[i][0])
                    i += 1
                print(header)
                path = "./%s购卡退卡明细.xlsx" % datetime.datetime.now().strftime("%Y-%m-%d")
                df.to_excel(path, encoding="utf_8_sig", header=header)

            except BaseException as e:
                print(e)
                QMessageBox.about(self, 'error', str(e))
            finally:
                self.conn.commit()
                cursor.close()
        else:
            print("购课退课明细")
            school = self.sel_school_card
            sql_test = '''
                    SELECT id, name From oliveperson.t_ethnic_group
                    '''
            sql = '''
                        SELECT
                organization.`name`,
                -- voucher.recording_time,
                date_format(
                    voucher.recording_time,
                    '%Y-%m-%d'
                ) '日期',
                voucher.seq_number,
                (
                    CASE
                    WHEN record.`type` = 0 THEN
                        '购课'
                    WHEN record.`type` = 1 THEN
                        '退课'
                    END
                ) AS '摘要',
                parent.given_name_oriental,
                customer.customer_code,
                student.student_name,
            -- record.receivable '应收金额',
            (
                    CASE
                    WHEN record.`type` = 0 THEN
                        record.receivable
                    WHEN record.`type` = 1 THEN
                        (0 - record.receivable)
                    END
                ) AS '应收金额',
                (
                    CASE
                    WHEN record.`type` = 0 THEN
                        record.receipt
                    WHEN record.`type` = 1 THEN
                        (0 - record.receipt)
                    END
                ) AS '实收金额',
                product.name,
                payment_method.`name` '支付方式',
                advisor.given_name_oriental '顾问',
                record.amount_expired '数量'
            FROM
                olivesps.t_student_pay_record record
            LEFT JOIN olivesps.t_school_student student ON student.id = record.school_student_id
            LEFT JOIN olivecustomer.t_c_customer c_customer ON student.parent_id = c_customer.person_id
            LEFT JOIN olivecustomer.t_customer customer ON c_customer.id = customer.id
            LEFT JOIN oliveperson.t_person parent ON c_customer.person_id = parent.id
            LEFT JOIN oliveproduct.t_product_base product ON product.id = record.product_id
            LEFT JOIN oliveorganization.t_organization organization ON product.org_id = organization.id
            LEFT JOIN oliveais.t_voucher voucher ON voucher.id = record.voucher_id
            LEFT JOIN oliveorder.t_payment_method payment_method ON record.receipt_id = payment_method.id
            LEFT JOIN oliveuser.t_user `user` ON voucher.operator_id = `user`.id
            LEFT JOIN oliveperson.t_person advisor ON advisor.id = `user`.person_id
            WHERE
                student.customer_id = 'YIJIE_2017_FAKE' -- and
                and voucher.recording_time >= '2020-09-01 0:0:0' 
                and voucher.recording_time < '2020-10-01 0:0:0'
            -- and student.id = '5dc679854eb2b0e48b3c102e'
            order by organization.`name`,voucher.recording_time,parent.given_name_oriental;
            
            '''

            cursor = self.conn.cursor()
            try:
                cursor.execute(sql_test)
                data = cursor.fetchall()
                df = pd.DataFrame(data)
                header = []
                i = 0
                count = len(cursor.description)

                while i < count:
                    header.insert(i, cursor.description[i][0])
                    i += 1
                print(header)
                path = "./%s购课退课明细.xlsx" % datetime.datetime.now().strftime("%Y-%m-%d")
                df.to_excel(path, encoding="utf_8_sig", header=header)

            except BaseException as e:
                print(e)
                QMessageBox.about(self, 'error', str(e))
            finally:
                self.conn.commit()
                cursor.close()

    def export_flow_fun(self):
        #warm 读取参数，放入SQL语句 # 时间
        start_time = self.start_time_flow.text()
        end_time = self.end_time_flow.text()
        print("%s   ->  %s" % (start_time, end_time))
        if self.cardSelBtn_flow.isChecked():
            print("购卡退卡的审批明细")
            school = self.sel_school_card
            sql_test = '''
                    SELECT id, name From oliveperson.t_ethnic_group
                    '''
            sql = '''
                    SELECT
            t3.`name`,
            t3.`日期`,
            t3.`摘要`,
            t3.given_name_oriental,
            t3.`客户编码`,
            t3.`学生`,
            t3.`实收金额`,
            t3.`赠送金额`,
            t3.name2,
            t3.remarks,
            t3.given_name_oriental2
        FROM
            (
        SELECT
            organization1.`name`,
            notification.created_time as '日期',
            '购卡或续费' AS '摘要',
            person1.given_name_oriental,
            customer1.customer_code '客户编码',
            student1.student_name '学生',
            receipt_info.proceeds '实收金额',
        IF
            ( receipt_info.give_money IS NULL, 0, receipt_info.give_money ) AS '赠送金额',
            payment_method1.`name` AS name2,
            REPLACE ( REPLACE ( receipt_info.remark, CHAR ( 10 ), ' ' ), CHAR ( 13 ), ' ' ) AS remarks,
        -- receipt_info.remark,
            advisor1.given_name_oriental AS given_name_oriental2
        FROM
            olivesps.t_notification notification
            INNER JOIN olivesps.t_receipt_info receipt_info ON notification.content = receipt_info.id
            LEFT JOIN olivesps.t_receipt receipt1 ON receipt1.id = receipt_info.receipt_id
            LEFT JOIN oliveorder.t_payment_method payment_method1 ON receipt1.receipt_type_id = payment_method1.id
            LEFT JOIN olivecustomer.t_c_customer c_customer1 ON receipt1.parent_id = c_customer1.person_id
            LEFT JOIN olivecustomer.t_customer customer1 ON c_customer1.id = customer1.id
            LEFT JOIN oliveperson.t_person person1 ON c_customer1.person_id = person1.id
            LEFT JOIN olivesps.t_school_student student1 ON student1.parent_id = c_customer1.person_id
            LEFT JOIN oliveorganization.t_organization organization1 ON student1.org_id = organization1.id
            LEFT JOIN oliveuser.t_user user1 ON receipt_info.operational_advisor_id = user1.id
            LEFT JOIN oliveperson.t_person advisor1 ON advisor1.id = user1.person_id 
        WHERE
            notification.receiver_id = '5ac75260e5dfb0e479d7350c' 
            AND notification.created_time > '2020-12-28 0:0:0' 
            AND notification.`status` = 3
            
            union all 
            
        SELECT
            organization2.`name`,
            notification2.created_time,
            '退卡或退款' AS '摘要',
            person2.given_name_oriental,
            customer2.customer_code '客户编码',
            student2.student_name '学生',
            ( 0 - receipt_refund.refund_amount ) '实收金额',
            0 AS '赠送金额',
            payment_method2.`name` AS name2,
            REPLACE ( REPLACE ( receipt_refund.remark, CHAR ( 10 ), '' ), CHAR ( 13 ), '' ),
            advisor2.given_name_oriental AS given_name_oriental2
        FROM
            olivesps.t_notification notification2
            INNER JOIN olivesps.t_receipt_refund receipt_refund ON notification2.content = receipt_refund.id
            LEFT JOIN olivesps.t_receipt receipt2 ON receipt2.id = receipt_refund.receipt_id
            LEFT JOIN oliveorder.t_payment_method payment_method2 ON receipt2.receipt_type_id = payment_method2.id
            LEFT JOIN olivecustomer.t_c_customer c_customer2 ON receipt2.parent_id = c_customer2.person_id
            LEFT JOIN olivecustomer.t_customer customer2 ON c_customer2.id = customer2.id
            LEFT JOIN oliveperson.t_person person2 ON c_customer2.person_id = person2.id
            LEFT JOIN olivesps.t_school_student student2 ON student2.parent_id = c_customer2.person_id
            LEFT JOIN oliveorganization.t_organization organization2 ON student2.org_id = organization2.id
            LEFT JOIN oliveuser.t_user user2 ON receipt_refund.operational_advisor_id = user2.id
            LEFT JOIN oliveperson.t_person advisor2 ON advisor2.id = user2.person_id 
        WHERE
        
            notification2.receiver_id = '5ac75260e5dfb0e479d7350c' 
            AND notification2.created_time > '2020-12-28 0:0:0' 
            AND notification2.`status` = 3
            
            
            ) t3 
        ORDER BY
            t3.`name`,
            t3.`日期`,
        t3.given_name_oriental'''

            cursor = self.conn.cursor()
            try:
                cursor.execute(sql_test)
                data = cursor.fetchall()
                df = pd.DataFrame(data)
                header = []
                i = 0
                count = len(cursor.description)

                while i < count:
                    header.insert(i, cursor.description[i][0])
                    i += 1
                print(header)
                path = "./%s客户会籍卡余额.xlsx" % datetime.datetime.now().strftime("%Y-%m-%d")
                df.to_excel(path, encoding="utf_8_sig", header=header)


            except BaseException as e:
                print(e)
                QMessageBox.about(self, 'error', str(e))
            finally:
                self.conn.commit()
                cursor.close()
        else:
            print("购课退课的审批明细")
            school = self.sel_school_card
            sql_test = '''
                    SELECT id, name From oliveperson.t_ethnic_group
                    '''
            sql = '''
                    SELECT
                    org.name,
                    notification.created_time,
                    '购课或退课' AS '摘要',
                    parent.given_name_oriental,
                    customer.customer_code,
                    pay_record.student_name,
                    payment_method.`name`,
                    pay_record.`subject_name`,
                    (
                        CASE
                        WHEN pay_record.`type` = 0 THEN
                            '购课'
                        WHEN pay_record.`type` = 1 THEN
                            '退课'
                        END
                    ) AS '摘要',
                    (
                        CASE
                        WHEN pay_record.`type` = 0 THEN
                            pay_record.receivable
                        WHEN pay_record.`type` = 1 THEN
                            (0 - pay_record.receivable)
                        END
                    ) AS '应收金额',
                    (
                        CASE
                        WHEN pay_record.`type` = 0 THEN
                            pay_record.receipt
                        WHEN pay_record.`type` = 1 THEN
                            (0 - pay_record.receipt)
                        END
                    ) AS '实收金额',
                    pay_record.remark 
                    FROM
                    t_notification notification
                    inner JOIN t_student_pay_record pay_record ON pay_record.id = notification.content
                    inner join t_school_student student on student.id = pay_record.school_student_id
                    inner join oliveperson.t_person parent on parent.id = student.parent_id
                        LEFT JOIN olivecustomer.t_c_customer c_customer ON parent.id = c_customer.person_id
                    LEFT JOIN olivecustomer.t_customer customer ON c_customer.id = customer.id
                    LEFT JOIN oliveuser.t_user advisor_user ON advisor_user.id = pay_record.operational_advisor_id
                    LEFT JOIN oliveperson.t_person advisor ON advisor.id = advisor_user.person_id
                    LEFT JOIN oliveorder.t_payment_method payment_method ON payment_method.id = pay_record.receipt_id
                    left join oliveorganization.t_organization org on org.id = pay_record.org_id
                    
                    WHERE
                    notification.receiver_id = '5ac75260e5dfb0e479d7350c' 
                    AND notification.created_time > '2020-12-28 0:0:0' 
                    AND notification.`status` = 3'''

            cursor = self.conn.cursor()
            try:
                cursor.execute(sql_test)
                data = cursor.fetchall()
                df = pd.DataFrame(data)
                header = []
                i = 0
                count = len(cursor.description)

                while i < count:
                    header.insert(i, cursor.description[i][0])
                    i += 1
                print(header)
                path = "./%s客户会籍卡余额.xlsx" % datetime.datetime.now().strftime("%Y-%m-%d")
                df.to_excel(path, encoding="utf_8_sig", header=header)


            except BaseException as e:
                print(e)
                QMessageBox.about(self, 'error', str(e))
            finally:
                self.conn.commit()
                cursor.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = ExportViewEx()
    dlg.show()
    sys.exit(app.exec())
