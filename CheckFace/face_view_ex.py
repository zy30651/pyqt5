import json
from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QPushButton, QMessageBox
from CheckFace import  face_view, face_upload_ex, import_excel_ex
import requests
"""
1：从服务器拿数据，tableView展示
2：新增、更新、删除人脸数据
3：搜索数据
4：默认校区展示
"""
customer_url = 'https://ssl.renee-arts.com/sps//api/v1/parent/parentListByOrgId'


class face_view_ex(QtWidgets.QMainWindow, face_view.Ui_Dialog_faceView):
    _signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(face_view_ex, self).__init__(parent)
        self.__index = 0
        self.setupUi(self)
        self.headers = ''
        self.updateUI()
        self.upload_view = ''
        self.import_view = ''
        self.page = 1
        self.max_page = 100
        self.data = []

    def updateUI(self):
        self.add_btn.clicked.connect(lambda: self.add_table())
        self.tableWidget.setColumnWidth(0, 130)
        self.tableWidget.setColumnWidth(1, 50)
        self.tableWidget.setColumnWidth(2, 50)
        self.tableWidget.setColumnWidth(3, 130)
        self.tableWidget.setColumnWidth(4, 130)
        self.tableWidget.setColumnWidth(5, 130)

        self.exit_btn.setHidden(True)
        self.down_arrow.clicked.connect(self.exit_action)
        self.prePage.clicked.connect(self.pre_page_action)
        self.nextPage.clicked.connect(self.next_page_action)
        self.search_btn.clicked.connect(self.search_action)
        self.search_text.returnPressed.connect(self.search_action)
        self.import_btn.clicked.connect(self.import_view)

    def exit_action(self):
        self.exit_btn.setHidden(False) if self.exit_btn.isHidden() else self.exit_btn.setHidden(True)

    def buttonForRow(self, row_data):
        widget = QWidget()
        update_btn = QPushButton('修改')
        update_btn.setStyleSheet(''' text-align : center;
                                           background-color : NavajoWhite;
                                           height : 50px;
                                           border-style: outset;
                                           font : 13px  ''')
        update_btn.clicked.connect(lambda: self.update_table(row_data))

        delete_btn = QPushButton('删除')
        delete_btn.setStyleSheet(''' text-align : center;
                                           background-color : red;
                                           height : 50px;
                                           border-style: outset;
                                           font : 13px  ''')
        delete_btn.clicked.connect(lambda: self.delete_table(row_data))

        layout = QHBoxLayout()
        layout.addWidget(update_btn)
        layout.addWidget(delete_btn)
        layout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(layout)
        return widget

    def update_table(self, row_data):
        self.upload_view = face_upload_ex.face_upload_ex()
        self.upload_view.custom_name.setText(row_data[0])
        self.upload_view.custom_id.setText(row_data[3])
        self.upload_view.show()

    def import_view(self):
        self.import_view = import_excel_ex.import_excel_ex()
        self.import_view.show()

    def add_table(self):
        self.upload_view = face_upload_ex.face_upload_ex()
        self.upload_view.show()

    def delete_table(self, row_data):
        reply = QMessageBox.warning(self, "删除客户人脸特征", "确认删除么！", QMessageBox.No | QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            # 删除接口
            print('YES')
        else:
            print('NO')

    def get_data(self, page, search_key=None):
        param = {
            'orgId': '7210',
            'customerId': 'YIJIE_2017_FAKE',
            'ifOrder': 'true',
            'pageNum': page,
            'pageSize': '20',
            'searchKey': search_key
        }
        r2 = requests.get(customer_url, params=param, headers=self.headers)
        response2 = json.loads(r2.content)
        if r2.status_code == 200:
            for customer in response2['results']:
                stu_name = customer['customerModel']['person']['nameOriental']
                stu_gender = customer['customerModel']['person']['gender']
                stu_age = customer['customerModel']['person']['age']
                customer_code = customer['customerModel']['customer']['customerCode']
                customer_name = customer['customerModel']['person']['nameOriental']
                customer_phone = customer['customerModel']['person']['contactInfos'][0]['contactInfo']
                self.data.append((stu_name, stu_gender, stu_age, customer_code, customer_name, customer_phone))

        for row_number, row_data in enumerate(self.data):
            self.tableWidget.insertRow(row_number)
            for i in range(len(row_data) + 1):
                if i < len(row_data):
                    self.tableWidget.setItem(row_number, i, QtWidgets.QTableWidgetItem(str(row_data[i])))
                if i == len(row_data):
                    self.tableWidget.setCellWidget(row_number, i, self.buttonForRow(row_data))

    def pre_page_action(self):
        if self.page == 1:
            QMessageBox.warning(self, "更新", "已经第一页了", QMessageBox.Yes)
        else:
            self.page -= 1
            self.get_data(self.page)

    def next_page_action(self):
        if self.page == self.max_page:
            QMessageBox.warning(self, "更新", "已经最后一页了", QMessageBox.Yes)
        else:
            self.page += 1
            self.get_data(self.page)

    def search_action(self):
        self.get_data(self.page, self.search_text.text())
