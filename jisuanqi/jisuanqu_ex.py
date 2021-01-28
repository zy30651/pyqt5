from jisuanqi import jisuanqi1
from PyQt5 import QtCore, QtGui, QtWidgets


class jisuanqi_ex(QtWidgets.QMainWindow, jisuanqi1.Ui_Dialog):
    _signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(jisuanqi_ex, self).__init__(parent)
        self.__index = 0
        self.setupUi(self)
        self.updateUI()

    def updateUI(self):
        self.line_value.setEnabled(False)
        self.btn_0.clicked.connect(self.updateData)
        self.btn_1.clicked.connect(self.updateData)
        self.btn_2.clicked.connect(self.updateData)
        self.btn_3.clicked.connect(self.updateData)
        self.btn_4.clicked.connect(self.updateData)
        self.btn_5.clicked.connect(self.updateData)
        self.btn_6.clicked.connect(self.updateData)
        self.btn_7.clicked.connect(self.updateData)
        self.btn_8.clicked.connect(self.updateData)
        self.btn_9.clicked.connect(self.updateData)
        self.btn_add.clicked.connect(self.updateData)
        self.btn_jian.clicked.connect(self.updateData)
        self.btn_cheng.clicked.connect(self.updateData)
        self.btn_chu.clicked.connect(self.updateData)
        self.btn_100.clicked.connect(self.updateData)
        self.btn_clear.clicked.connect(self.updateData)
        self.btn_point.clicked.connect(self.updateData)
        self.btn_eq.clicked.connect(self.updateData)
        self.btn_eq.clicked.connect(self.updateData)

    def updateData(self):
        sender = self.sender()
        print(sender.text())
        str = sender.text()
        self.line_value.setText(str)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QMainWindow()
    ui = jisuanqi_ex()
    ui.setupUi(Dialog)
    ui.updateUI()
    Dialog.show()
    sys.exit(app.exec_())
