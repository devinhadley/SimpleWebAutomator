# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DirectoryWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Directory(object):
    def setupUi(self, Directory):
        Directory.setObjectName("Directory")
        Directory.resize(341, 127)
        self.gridLayout_2 = QtWidgets.QGridLayout(Directory)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(Directory)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Directory)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Directory)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 2, 0, 1, 1)

        self.retranslateUi(Directory)
        QtCore.QMetaObject.connectSlotsByName(Directory)

    def retranslateUi(self, Directory):
        _translate = QtCore.QCoreApplication.translate
        Directory.setWindowTitle(_translate("Directory", "Enter Directory"))
        self.label.setText(_translate("Directory", "Please enter the driver directory."))
        self.pushButton.setText(_translate("Directory", "Save"))
