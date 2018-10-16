# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WildTrack.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(836, 429)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.filepathLabel = QtWidgets.QTextBrowser(self.centralwidget)
        self.filepathLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.filepathLabel.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.filepathLabel.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.filepathLabel.setObjectName("filepathLabel")
        self.horizontalLayout.addWidget(self.filepathLabel)
        self.openButton = QtWidgets.QPushButton(self.centralwidget)
        self.openButton.setMinimumSize(QtCore.QSize(80, 0))
        self.openButton.setObjectName("openButton")
        self.horizontalLayout.addWidget(self.openButton)
        self.detectButton = QtWidgets.QPushButton(self.centralwidget)
        self.detectButton.setMinimumSize(QtCore.QSize(80, 0))
        self.detectButton.setObjectName("detectButton")
        self.horizontalLayout.addWidget(self.detectButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.videoWidget = QVideoWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videoWidget.sizePolicy().hasHeightForWidth())
        self.videoWidget.setSizePolicy(sizePolicy)
        self.videoWidget.setMinimumSize(QtCore.QSize(560, 315))
        self.videoWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.videoWidget.setBaseSize(QtCore.QSize(50, 100))
        self.videoWidget.setObjectName("videoWidget")
        self.horizontalLayout_2.addWidget(self.videoWidget)
        self.infoLabel = QtWidgets.QTextBrowser(self.centralwidget)
        self.infoLabel.setMinimumSize(QtCore.QSize(250, 0))
        self.infoLabel.setMaximumSize(QtCore.QSize(250, 16777215))
        self.infoLabel.setBaseSize(QtCore.QSize(50, 50))
        self.infoLabel.setObjectName("infoLabel")
        self.horizontalLayout_2.addWidget(self.infoLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setMaximumSize(QtCore.QSize(32, 32))
        self.stopButton.setText("")
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout_5.addWidget(self.stopButton)
        self.playPauseButton = QtWidgets.QPushButton(self.centralwidget)
        self.playPauseButton.setMaximumSize(QtCore.QSize(32, 32))
        self.playPauseButton.setText("")
        self.playPauseButton.setObjectName("playPauseButton")
        self.horizontalLayout_5.addWidget(self.playPauseButton)
        self.durationLabel = QtWidgets.QLabel(self.centralwidget)
        self.durationLabel.setObjectName("durationLabel")
        self.horizontalLayout_5.addWidget(self.durationLabel)
        self.slider = QtWidgets.QSlider(self.centralwidget)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")
        self.horizontalLayout_5.addWidget(self.slider)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_5)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "WildTracker"))
        self.filepathLabel.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">No file loaded...</span></p></body></html>"))
        self.openButton.setText(_translate("MainWindow", "Open"))
        self.detectButton.setText(_translate("MainWindow", "Detect"))
        self.durationLabel.setText(_translate("MainWindow", "00:00/00:00"))

from PyQt5.QtMultimediaWidgets import QVideoWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

