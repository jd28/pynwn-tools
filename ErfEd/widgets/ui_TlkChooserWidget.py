# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TlkChooserWidget.ui'
#
# Created: Thu Sep 18 02:37:01 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TlkFiles(object):
    def setupUi(self, TlkFiles):
        TlkFiles.setObjectName("TlkFiles")
        TlkFiles.resize(400, 160)
        self.verticalLayout = QtWidgets.QVBoxLayout(TlkFiles)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tlkGroupBox = QtWidgets.QGroupBox(TlkFiles)
        self.tlkGroupBox.setObjectName("tlkGroupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.tlkGroupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.defaultTlk = QtWidgets.QLineEdit(self.tlkGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.defaultTlk.sizePolicy().hasHeightForWidth())
        self.defaultTlk.setSizePolicy(sizePolicy)
        self.defaultTlk.setObjectName("defaultTlk")
        self.gridLayout.addWidget(self.defaultTlk, 0, 1, 1, 1)
        self.customTlk = QtWidgets.QLineEdit(self.tlkGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customTlk.sizePolicy().hasHeightForWidth())
        self.customTlk.setSizePolicy(sizePolicy)
        self.customTlk.setObjectName("customTlk")
        self.gridLayout.addWidget(self.customTlk, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.tlkGroupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tlkGroupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.fileDefaultTlk = QtWidgets.QToolButton(self.tlkGroupBox)
        self.fileDefaultTlk.setObjectName("fileDefaultTlk")
        self.gridLayout.addWidget(self.fileDefaultTlk, 0, 2, 1, 1)
        self.fileCustomTlk = QtWidgets.QToolButton(self.tlkGroupBox)
        self.fileCustomTlk.setObjectName("fileCustomTlk")
        self.gridLayout.addWidget(self.fileCustomTlk, 1, 2, 1, 1)
        self.verticalLayout.addWidget(self.tlkGroupBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(TlkFiles)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(TlkFiles)
        self.buttonBox.accepted.connect(TlkFiles.accept)
        self.buttonBox.rejected.connect(TlkFiles.reject)
        QtCore.QMetaObject.connectSlotsByName(TlkFiles)

    def retranslateUi(self, TlkFiles):
        _translate = QtCore.QCoreApplication.translate
        TlkFiles.setWindowTitle(_translate("TlkFiles", "Dialog"))
        self.tlkGroupBox.setTitle(_translate("TlkFiles", "TLK Files"))
        self.label.setText(_translate("TlkFiles", "Default:"))
        self.label_2.setText(_translate("TlkFiles", "Custom:"))
        self.fileDefaultTlk.setText(_translate("TlkFiles", "..."))
        self.fileCustomTlk.setText(_translate("TlkFiles", "..."))

