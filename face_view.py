# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'face_view.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_faceView(object):
    def setupUi(self, Dialog_faceView):
        Dialog_faceView.setObjectName("Dialog_faceView")
        Dialog_faceView.resize(807, 597)
        self.layoutWidget = QtWidgets.QWidget(Dialog_faceView)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 10, 761, 28))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.select_school = QtWidgets.QComboBox(self.layoutWidget)
        self.select_school.setObjectName("select_school")
        self.select_school.addItem("")
        self.select_school.addItem("")
        self.horizontalLayout.addWidget(self.select_school)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.login_name = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.login_name.setFont(font)
        self.login_name.setObjectName("login_name")
        self.horizontalLayout_2.addWidget(self.login_name)
        self.down_arrow = QtWidgets.QToolButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.NoAntialias)
        self.down_arrow.setFont(font)
        self.down_arrow.setStyleSheet("border:none")
        self.down_arrow.setText("")
        self.down_arrow.setIconSize(QtCore.QSize(14, 14))
        self.down_arrow.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
        self.down_arrow.setArrowType(QtCore.Qt.DownArrow)
        self.down_arrow.setObjectName("down_arrow")
        self.horizontalLayout_2.addWidget(self.down_arrow)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.exit_btn = QtWidgets.QLabel(Dialog_faceView)
        self.exit_btn.setEnabled(True)
        self.exit_btn.setGeometry(QtCore.QRect(724, 40, 31, 16))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.exit_btn.setFont(font)
        self.exit_btn.setObjectName("exit_btn")
        self.tableView = QtWidgets.QTableView(Dialog_faceView)
        self.tableView.setGeometry(QtCore.QRect(0, 70, 801, 531))
        font = QtGui.QFont()
        font.setKerning(True)
        self.tableView.setFont(font)
        self.tableView.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tableView.setToolTipDuration(0)
        self.tableView.setLineWidth(0)
        self.tableView.setGridStyle(QtCore.Qt.NoPen)
        self.tableView.setObjectName("tableView")
        self.tableWidget = QtWidgets.QTableWidget(Dialog_faceView)
        self.tableWidget.setGeometry(QtCore.QRect(0, 70, 807, 480))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.layoutWidget1 = QtWidgets.QWidget(Dialog_faceView)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 40, 351, 25))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.search_text = QtWidgets.QLineEdit(self.layoutWidget1)
        self.search_text.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.search_text.setObjectName("search_text")
        self.horizontalLayout_4.addWidget(self.search_text)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.search_btn = QtWidgets.QToolButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.NoAntialias)
        self.search_btn.setFont(font)
        self.search_btn.setStyleSheet("border:none")
        self.search_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("sousuo1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_btn.setIcon(icon)
        self.search_btn.setIconSize(QtCore.QSize(14, 14))
        self.search_btn.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
        self.search_btn.setArrowType(QtCore.Qt.NoArrow)
        self.search_btn.setObjectName("search_btn")
        self.horizontalLayout_5.addWidget(self.search_btn)
        self.add_btn = QtWidgets.QPushButton(Dialog_faceView)
        self.add_btn.setGeometry(QtCore.QRect(400, 40, 113, 32))
        self.add_btn.setObjectName("add_btn")
        self.layoutWidget2 = QtWidgets.QWidget(Dialog_faceView)
        self.layoutWidget2.setGeometry(QtCore.QRect(2, 558, 811, 32))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.prePage = QtWidgets.QPushButton(self.layoutWidget2)
        self.prePage.setObjectName("prePage")
        self.horizontalLayout_6.addWidget(self.prePage)
        self.nextPage = QtWidgets.QPushButton(self.layoutWidget2)
        self.nextPage.setObjectName("nextPage")
        self.horizontalLayout_6.addWidget(self.nextPage)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.import_btn = QtWidgets.QPushButton(Dialog_faceView)
        self.import_btn.setGeometry(QtCore.QRect(520, 40, 113, 32))
        self.import_btn.setObjectName("import_btn")

        self.retranslateUi(Dialog_faceView)
        QtCore.QMetaObject.connectSlotsByName(Dialog_faceView)

    def retranslateUi(self, Dialog_faceView):
        _translate = QtCore.QCoreApplication.translate
        Dialog_faceView.setWindowTitle(_translate("Dialog_faceView", "客户面部特征管理"))
        self.label.setText(_translate("Dialog_faceView", "当前校区："))
        self.select_school.setItemText(0, _translate("Dialog_faceView", "顺义校区"))
        self.select_school.setItemText(1, _translate("Dialog_faceView", "蓝港校区"))
        self.login_name.setText(_translate("Dialog_faceView", "张扬"))
        self.exit_btn.setText(_translate("Dialog_faceView", "退出"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog_faceView", "学员姓名"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog_faceView", "性别"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog_faceView", "年龄"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog_faceView", "客户编码"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog_faceView", "客户姓名"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Dialog_faceView", "客户手机号"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Dialog_faceView", "操作"))
        self.label_2.setText(_translate("Dialog_faceView", "搜       索："))
        self.add_btn.setText(_translate("Dialog_faceView", "新增"))
        self.prePage.setText(_translate("Dialog_faceView", "上一页"))
        self.nextPage.setText(_translate("Dialog_faceView", "下一页"))
        self.import_btn.setText(_translate("Dialog_faceView", "导入"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_faceView = QtWidgets.QDialog()
    ui = Ui_Dialog_faceView()
    ui.setupUi(Dialog_faceView)
    Dialog_faceView.show()
    sys.exit(app.exec_())
