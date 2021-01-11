import login_page
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
import sys
import json
import requests
import face_view_ex

login_url = 'https://ssl.renee-arts.com/sps/api/v1/login'
me_url = 'https://ssl.renee-arts.com/sps//api/v1/user/me'
Dialog = ''


class login_page_ex(QtWidgets.QMainWindow, login_page.Ui_login_page):
    _signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(login_page_ex, self).__init__(parent)
        self.__index = 0
        self.setupUi(self)
        self.updateUI()
        self.token = ''
        self.face_view = ''
        self.headers = {'customer_id': 'YIJIE_2017_FAKE'}

    def updateUI(self):
        self.login_btn.clicked.connect(self.login)
        self.custom_name.setText('jacy.liu@renee-arts.com')
        self.custom_pwd.setText('Renee201906')

    def login(self):

        data = {
            "username": self.custom_name.text(),
            "password": self.custom_pwd.text(),
        }

        json_data = json.dumps(data)
        r = requests.post(login_url, data=json_data)
        response = json.loads(r.content)
        if r.status_code != 200:
            return
        self.token = response['tokenType'] + ' ' + response['token']
        self.headers['authorization'] = self.token
        r2 = requests.get(me_url, headers=self.headers)
        response2 = json.loads(r2.content)
        if r2.status_code != 200:
            return

        Dialog.hide()
        self.face_view = face_view_ex.face_view_ex()
        self.face_view.login_name.setText(response2['userDisplayName'])
        self.face_view.headers = self.headers
        self.face_view.get_data(1)
        self.face_view.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QMainWindow()
    ui = login_page_ex()
    ui.setupUi(Dialog)
    ui.updateUI()
    Dialog.show()
    sys.exit(app.exec_())