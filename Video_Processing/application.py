#!/usr/bin/env python3

from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QVideoProbe
from PyQt5.QtCore import QDir, Qt, QUrl, QCoreApplication, QStandardPaths
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QMainWindow)
from WildTrack import Ui_MainWindow

import os
import sys
import subprocess

import detection

# The class that handles the application itself
class ApplicationWindow(QMainWindow):
    ## Accessing files in Processed Stuff ##
    QDir.setCurrent(QCoreApplication.applicationDirPath())
    processedVideoPath = QDir.currentPath() + "/ProcessedStuff/horses_1_predicted.mp4";
    textFilePath = QDir.currentPath() + "/ProcessedStuff/labels_example.txt";

    # Environmental Variable
    # os.environ['PYTHONPATH'] = "$(pwd)/detection:$(pwd)/detection/slim"
    # subprocess.check_call(['sqsub', '-np', sys.argv[1], 'application.py'],
    #                   env=dict(os.environ, SQSUB_VAR="visible in this subprocess"))

    ## Important variables ##
    videoLoaded = False
    fileReceived = False
    playing = False
    fileName = None
    labels = []
    nextLine = 0

    def __init__(self):
        # Create the Qt5 application backend
        super(ApplicationWindow, self).__init__()

        # Load in and display the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## CONNECT EVENTS (like button presses) to functions ##
        self.ui.playPauseButton.clicked.connect(self.playPauseButtonClicked)
        self.ui.openButton.clicked.connect(self.openButtonClicked)
        self.ui.detectButton.clicked.connect(self.detectButtonClicked)

        # Configure the original video widget
        # self.original_video_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        # self.original_video_player.durationChanged.connect(self.durationChanged)
        # self.original_video_player.setVideoOutput(self.ui.original_video_widget)

        # Configure the processed video widget
        self.videoPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoPlayer.setNotifyInterval(30)
        self.videoPlayer.durationChanged.connect(self.durationChanged)
        self.videoPlayer.positionChanged.connect(self.positionChanged)
        self.videoPlayer.stateChanged.connect(self.stopped)
        self.videoPlayer.setVideoOutput(self.ui.videoWidget)

        # Configure the video slider
        self.ui.slider.sliderPressed.connect(self.sliderPressed)
        self.ui.slider.sliderReleased.connect(self.sliderReleased)

        # Update states
        self.updateStates()

    ##  CALLBACK FUNCTIONS ##
    def playPauseButtonClicked(self):
        if self.playing:
            print("Pause!")
            self.pause()
        else:
            print("Play!")
            self.play()

    def saveButtonClicked(self):
        print("Save!")

    def openButtonClicked(self):
        print("Load!")
        # fileName, _ = QFileDialog.getOpenFileName(
        #     self,
        #     "Choose a video",
        #     QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation),
        #     "Vide files (*mp4 *mp3)")
        # file = open("ProcessedStuff/labels_example.txt","w")
        # file.write("labels = []\n")
        # file.close()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Files")

        if fileName != "":
            self.ui.filepathLabel.setText(fileName)
            print("Video filepath: " + fileName)
            self.fileName = fileName
            self.fileReceived = True
            self.nextLine = 0
            self.updateStates()

    def detectButtonClicked(self):
        print("Track!")

        # Do processing and call following method when completed #
        detection.detection_code(self.fileName)
        self.processingFinished()

    def sliderReleased(self):
        newPosition = self.ui.slider.value()
        self.setPosition(newPosition)

    def sliderPressed(self):
        self.pause()

    def durationChanged(self):
        self.videoLoaded = True
        self.updateStates()
        self.ui.slider.setMaximum(self.videoPlayer.duration())

    def positionChanged(self):
        if not self.playing:
            return
        position = self.videoPlayer.position()
        # Update video progress bar
        self.ui.slider.setValue(position)
        # Update information label
        self.updateLabel(position)

    def stopped(self):
        if self.videoPlayer.state() == QMediaPlayer.StoppedState:
            self.playing = False
            self.ui.infoLabel.setText("")

    ## Helper Functions ##
    def play(self):
        # self.original_video_player.play()
        self.videoPlayer.play()
        self.playing = True

    def pause(self):
        self.playing = False
        self.original_video_player.pause()
        self.video_player.pause()

    def setPosition(self, position):
        self.resetNextLine(position)
        self.updateLabel(position)
        # self.original_video_player.setPosition(position)
        self.videoPlayer.setPosition(position)
        self.play()

    def updateStates(self):
        self.ui.playPauseButton.setEnabled(self.videoLoaded)
        self.ui.slider.setEnabled(self.videoLoaded)
        self.ui.detectButton.setEnabled(self.fileReceived and not self.playing)

    def processingFinished(self):
        print("Text file location: " + self.textFilePath)
        file = open(self.textFilePath, "r")
        self.labels = [line.split(',') for line in file]
        file.close()
        print(self.processedVideoPath)
        self.videoPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.processedVideoPath)))
        # self.original_video_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.fileName)))
        self.play()

    # When the user changes the slider the next line changes
    def resetNextLine(self, position):
        while (position < int(self.labels[self.nextLine][0])):
            self.nextLine -= 1
            if (self.nextLine <= 0):
                break
        if self.nextLine+1<=len(self.labels)-1:
            while (position >= int(self.labels[self.nextLine+1][0])):
                self.nextLine += 1
                if (self.nextLine >= len(self.labels)-1):
                    break

    def updateLabel(self, position):
        if position >= int(self.labels[self.nextLine][0]):
            label = self.labels[self.nextLine]
            messageStr = "Count: " + label[1]
            for i in range(2,len(label),2):
                messageStr += ("\n%s. %s %s" % (i-int(i/2),label[i],label[i+1]))
            self.ui.infoLabel.setText(messageStr)
            if self.nextLine < len(self.labels)-1:
                self.nextLine += 1

# The "main()" function, like a C program
def main():
    print("Loading application...")
    app = QApplication(sys.argv)
    application = ApplicationWindow()
    print("Application loaded.")
    application.show()
    sys.exit(app.exec_())

# Provides a start point for out code
if __name__ == "__main__":
    main()
