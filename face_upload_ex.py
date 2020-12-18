# 实现一个小应用，

import face_upload
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
import sys
import face_recognition
import requests
import json

URL = "https://www.baidu.com"


class face_upload_ex(QtWidgets.QMainWindow, face_upload.Ui_MainWindow):
    _signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(face_upload_ex, self).__init__(parent)
        self.__index = 0
        self.face_encode = ''
        self.setupUi(self)
        self.updateUI()

    def updateUI(self):
        self.clear.clicked.connect(self.data_clear)
        self.upload.clicked.connect(self.data_upload)
        self.upload_face.setScaledContents(True)
        self.upload_face.mousePressEvent = self.open_image

    def data_clear(self):
        self.custom_name.setText('')
        self.custom_id.setText('')
        print("已清空")

    def data_upload(self):
            # data = {
            #     "face_encoding": self.face_encoding,
            #     "custom_name": self.custom_name.text(),
            #     "custom_id": self.custom_id.text(),
            #     "select_school": self.select_school.currentText()
            # }
            # print(data)
            # headers = {'content-type': 'application/json',
            #            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
            # r = requests.post(url, data)
            r = requests.get(URL)
            print(r)

            QMessageBox.warning(self, "图片上传", "上传成功！", QMessageBox.Yes)

    def open_image(self, e):
        img_name, img_type = QFileDialog.getOpenFileName(self, "打开图片", "", "*.png;;*.jpg")
        print(img_name, img_type)
        if img_name != "":
            img = QtGui.QPixmap(img_name)
            print(img.size)
            self.upload_face.setPixmap(img)
            a_images = face_recognition.load_image_file(img_name)
            self.face_encoding = face_recognition.face_encodings(a_images)[0]


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QMainWindow()
    ui = face_upload_ex()
    ui.setupUi(Dialog)
    ui.updateUI()
    Dialog.show()
    sys.exit(app.exec_())
