# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wildtrack.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(676, 409)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.button_play_pause = QtWidgets.QPushButton(self.centralwidget)
        self.button_play_pause.setGeometry(QtCore.QRect(20, 290, 91, 31))
        self.button_play_pause.setObjectName("button_play_pause")
        self.video_slider = QtWidgets.QSlider(self.centralwidget)
        self.video_slider.setGeometry(QtCore.QRect(110, 290, 281, 22))
        self.video_slider.setOrientation(QtCore.Qt.Horizontal)
        self.video_slider.setObjectName("video_slider")
        self.video_widget = QVideoWidget(self.centralwidget)
        self.video_widget.setGeometry(QtCore.QRect(20, 50, 371, 231))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.video_widget.sizePolicy().hasHeightForWidth())
        self.video_widget.setSizePolicy(sizePolicy)
        self.video_widget.setBaseSize(QtCore.QSize(50, 100))
        self.video_widget.setObjectName("video_widget")
        self.label_info = QtWidgets.QTextBrowser(self.centralwidget)
        self.label_info.setGeometry(QtCore.QRect(410, 10, 256, 141))
        self.label_info.setBaseSize(QtCore.QSize(50, 50))
        self.label_info.setObjectName("label_info")
        self.button_load = QtWidgets.QPushButton(self.centralwidget)
        self.button_load.setGeometry(QtCore.QRect(310, 20, 80, 31))
        self.button_load.setObjectName("button_load")
        self.file_info = QtWidgets.QTextBrowser(self.centralwidget)
        self.file_info.setGeometry(QtCore.QRect(20, 20, 291, 21))
        self.file_info.setObjectName("file_info")
        self.original_video_widget = QVideoWidget(self.centralwidget)
        self.original_video_widget.setGeometry(QtCore.QRect(410, 160, 251, 191))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.original_video_widget.sizePolicy().hasHeightForWidth())
        self.original_video_widget.setSizePolicy(sizePolicy)
        self.original_video_widget.setBaseSize(QtCore.QSize(50, 100))
        self.original_video_widget.setObjectName("original_video_widget")
        self.button_track = QtWidgets.QPushButton(self.centralwidget)
        self.button_track.setGeometry(QtCore.QRect(170, 340, 81, 31))
        self.button_track.setObjectName("button_track")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button_play_pause.setText(_translate("MainWindow", "Play/Pause"))
        self.button_load.setText(_translate("MainWindow", "Load"))
        self.file_info.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">No file loaded...</span></p></body></html>"))
        self.button_track.setText(_translate("MainWindow", "Track"))

from PyQt5.QtMultimediaWidgets import QVideoWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

