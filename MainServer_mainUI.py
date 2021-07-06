# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainUI_mainserver.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_MainServer(object):
    def setupUi(self, Dialog_MainServer):
        Dialog_MainServer.setObjectName("Dialog_MainServer")
        Dialog_MainServer.setEnabled(True)
        Dialog_MainServer.resize(700, 60)
        Dialog_MainServer.setMinimumSize(QtCore.QSize(700, 60))
        Dialog_MainServer.setMaximumSize(QtCore.QSize(700, 60))
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Dialog_MainServer)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 681, 42))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.lineEdit_MainIP = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.lineEdit_MainIP.setFont(font)
        self.lineEdit_MainIP.setObjectName("lineEdit_MainIP")
        self.horizontalLayout_2.addWidget(self.lineEdit_MainIP)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_MainPort = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_MainPort.sizePolicy().hasHeightForWidth())
        self.lineEdit_MainPort.setSizePolicy(sizePolicy)
        self.lineEdit_MainPort.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_MainPort.setMaximumSize(QtCore.QSize(140, 16777215))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.lineEdit_MainPort.setFont(font)
        self.lineEdit_MainPort.setObjectName("lineEdit_MainPort")
        self.horizontalLayout_2.addWidget(self.lineEdit_MainPort)
        self.pushButton_Start = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_Start.setObjectName("pushButton_Start")
        self.horizontalLayout_2.addWidget(self.pushButton_Start)
        self.pushButton_hint = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_hint.setEnabled(False)
        self.pushButton_hint.setMinimumSize(QtCore.QSize(40, 40))
        self.pushButton_hint.setMaximumSize(QtCore.QSize(40, 40))
        self.pushButton_hint.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("sources/green.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_hint.setIcon(icon)
        self.pushButton_hint.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_hint.setFlat(False)
        self.pushButton_hint.setObjectName("pushButton_hint")
        self.horizontalLayout_2.addWidget(self.pushButton_hint)

        self.retranslateUi(Dialog_MainServer)
        QtCore.QMetaObject.connectSlotsByName(Dialog_MainServer)

    def retranslateUi(self, Dialog_MainServer):
        _translate = QtCore.QCoreApplication.translate
        Dialog_MainServer.setWindowTitle(_translate("Dialog_MainServer", "淮安市纪委监委文件分发系统服务器"))
        self.label.setText(_translate("Dialog_MainServer", "服务器IP"))
        self.label_2.setText(_translate("Dialog_MainServer", "端口"))
        self.pushButton_Start.setText(_translate("Dialog_MainServer", "启动"))

