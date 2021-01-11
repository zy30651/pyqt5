# 实现一个小应用，
import pymysql
from PyQt5.QtCore import QTime
from PyQt5.QtGui import QIntValidator, QCloseEvent

pymysql.install_as_MySQLdb()

from PyQt5.QtWidgets import QMessageBox, QFileDialog
import pandas as pd
import import_excel, sys
from PyQt5 import QtWidgets, QtCore, QtGui


class import_excel_ex(QtWidgets.QMainWindow, import_excel.Ui_MainWindow):
    _signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(import_excel_ex, self).__init__(parent)
        self.__index = 0
        self.conn = ''
        self.data = ''
        self.sheet_name = ''
        self.sheet_titles = ''
        self.setupUi(self)
        self.updateUI()

    def updateUI(self):
        self.port_name.setValidator(QIntValidator(0, 99999))
        self.server_name.setInputMask('000.000.000.000;')
        self.connect_btn.clicked.connect(self.connect_mysql)
        self.import_btn.clicked.connect(self.import_click)
        self.open_btn.clicked.connect(self.open_click)
        self.sheet_list.clicked.connect(self.sheet_click)

    def connect_mysql(self):
        if self.import_btn.isEnabled():
            print('数据库已连接,准备断开')
            try:
                self.conn.close()
                self.status_line.setText('数据库已断开连接')
                self.import_btn.setEnabled(False)
                self.connect_btn.setText('连接')
            except BaseException as e:
                print(str(e))

        else:
            print('数据库没有链接，准备连接')
            db_name = self.db_name.text()
            port_name = int(self.port_name.text())
            server_name = self.server_name.text()
            user_name = self.user_name.text()
            pwd_name = self.pwd_name.text()

            try:
                self.conn = pymysql.connect(
                    host=server_name,
                    port=port_name,
                    user=user_name,
                    passwd=pwd_name,
                    db=db_name,
                    charset="utf8")

                print('数据库连接成功')
                self.status_line.setText('数据库连接成功！')
                self.connect_btn.setText('断开')

                if (self.connect_btn.text() == '断开') and len(self.sheet_titles) > 0:
                    self.import_btn.setEnabled(True)
            except BaseException as e:
                print(e)
                QMessageBox.about(self, '连接失败', str(e))

    def open_click(self):
        self.sheet_list.clear()
        self.excel_title_list.clear()
        filepath, _ = QFileDialog.getOpenFileName(
            self, '选中文件', '', 'Excel File(*.xlsx , *.xls)')
        self.file_path.setText(filepath)
        try:
            # data = pd.read_excel(filepath, sheet_name=None)
            self.data = pd.ExcelFile(filepath, engine='xlrd')
            sheets = self.data.sheet_names
            self.sheet_list.addItems(sheets)
        except BaseException as e:
            print(e)
            QMessageBox.about(self, '打开失败，请检查文件', str(e))

    def sheet_click(self):
        self.excel_title_list.clear()
        # 点击第一列sheet，给第二个表展示表内title字段
        self.sheet_name = self.sheet_list.currentItem().text()
        print("点击的是： %s" % self.sheet_name)
        df = self.data.parse(self.sheet_name)
        self.sheet_titles = []
        for i in df.columns.values:
            self.sheet_titles.append(str(i))
        self.excel_title_list.addItems(self.sheet_titles)
        if (self.connect_btn.text() == '断开') and len(self.sheet_titles) > 0:
            self.import_btn.setEnabled(True)

    def import_click(self):
        # 拿到上一次点击的那一个sheet
        start_time = QTime.currentTime()
        # 建表语句
        df = self.data.parse(self.sheet_name)
        table_name = 't_teacher'
        sql_createtable = "CREATE TABLE IF NOT EXISTS `" + table_name + "`("
        sql_createtable_word = ""
        for n in range(len(self.sheet_titles)):
            if n == len(self.sheet_titles)-1:
                sql_createtable_word += "`" + str(self.sheet_titles[n]) + "`" + " varchar(255))"
            else:
                sql_createtable_word += "`" + str(self.sheet_titles[n]) + "`" + " varchar(255),"

            # if self.sheet_titles[n] != '':
            #     sql_createtable_word += "`" + str(self.sheet_titles[n]) + "`" + " varchar(255),"
            # else:
            #     sql_createtable_word += "`" + str(n) + "`" + " varchar(255),"

        sql_createtable += sql_createtable_word
        print("sql: %s" % sql_createtable)

        # 执行SQL语句建表，如果表不存在
        cur = self.conn.cursor()
        try:
            cur.execute(sql_createtable)
        except BaseException as e:
            QMessageBox.about(self, 'error', str(e))

        # 插入语句
        sql_insert_array = []
        sql_insert_table_temp = "INSERT INTO `" + table_name + "`VALUES ("
        x = 0
        while x < len(df.values):
            print('_'*30)
            # 如果x小于行数
            sql_insert_word = ""
            for y in df.values[x]:
                if y is df.values[x][-1]:
                    sql_insert_word = sql_insert_word + "'" + str(y)
                else:
                    sql_insert_word = sql_insert_word + "'" + str(y) + "',"
            sql_insert_table = sql_insert_table_temp + sql_insert_word + "')"
            print(sql_insert_table)
            sql_insert_array.append(sql_insert_table)
            x = x+1
        print(sql_insert_array)

        # 执行SQL语句插入数据
        cur = self.conn.cursor()
        try:
            for n in sql_insert_array:
                cur.execute(str(n))
        except BaseException as e:
            print(e)
            QMessageBox.about(self, 'error', str(e))
        finally:
            self.conn.commit()
            cur.close()

        # 记录导入时间
        end_time = QTime.currentTime()
        time = QTime.msecsTo(start_time, end_time) / 1000
        s = "成功导入：" + str(len(df.values)) + "条数据，" + "用时: " + str(time) + "秒"
        self.status_line.setText(s)
        self.import_btn.setEnabled(False)

    def conn_disconnect(self):
        try:
            if self.conn is '':
                print("数据库未连接，不需要断开")
            else:
                self.conn.close()
            self.status_line.setText("数据库已断开连接")
            self.import_btn.setEnabled(False)
            self.open_btn.setText("打开")
        except BaseException as e:
            print(e)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        res = QMessageBox.question(self, "消息", "是否关闭这个窗口？ 这将断开数据库连接。",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if res == QMessageBox.Yes:
            self.conn_disconnect()
            QCloseEvent.accept(a0)
        else:
            QCloseEvent.ignore()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QMainWindow()
    ui = import_excel_ex()
    ui.setupUi(Dialog)
    ui.updateUI()
    Dialog.show()
    sys.exit(app.exec_())
