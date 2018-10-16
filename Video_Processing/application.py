#!/usr/bin/env python3

from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QVideoProbe
from PyQt5.QtCore import QDir, Qt, QUrl, QCoreApplication, QStandardPaths, QTime
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QMainWindow, QProgressDialog, QMessageBox)
from WildTrack import Ui_MainWindow
import PyQt5.QtTest

import os
import sys
import subprocess
import time

import detection
import PyQtThreading

# The class that handles the application itself
class ApplicationWindow(QMainWindow):
    ## Accessing files in Processed Stuff ##
    processedVideoPath = QDir.currentPath() + "/ProcessedStuff/horses_1_predicted.mp4";
    textFilePath = QDir.currentPath() + "/ProcessedStuff/labels_example.txt";

    # Environmental Variable
    # os.environ['PYTHONPATH'] = "$(pwd)/detection:$(pwd)/detection/slim"
    # subprocess.check_call(['sqsub', '-np', sys.argv[1], 'application.py'],
    #                   env=dict(os.environ, SQSUB_VAR="visible in this subprocess"))

    ## Important variables ##
    # 3 key states
    fileUploaded = False
    fileProcessed = False
    processing = False

    videoLoaded = False
    fileReceived = False
    playing = False
    fileName = None
    duration = 0
    labels = []
    nextLine = 0
    state = QMediaPlayer.StoppedState
    originalState = QMediaPlayer.StoppedState

    def __init__(self):
        # Create the Qt5 application backend
        super(ApplicationWindow, self).__init__()

        # Load in and display the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## CONFIGURING GUI WIDGETS ##
        # Play button
        self.ui.playPauseButton.clicked.connect(self.playPauseButtonClicked) # configuring callback method
        self.ui.playPauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay)) # play icon

        # Stop button
        self.ui.stopButton.clicked.connect(self.stopButtonClicked)
        self.ui.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop)) # stop icon

        # Open (folder) button
        self.ui.openButton.clicked.connect(self.openButtonClicked)

        # Detect button
        self.ui.detectButton.clicked.connect(self.detectButtonClicked)

        # Help button
        self.ui.helpButton.clicked.connect(self.helpButtonClicked)

        # Video player
        self.videoPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface) # QMediaPlayer object
        self.videoPlayer.durationChanged.connect(self.durationChanged)
        self.videoPlayer.positionChanged.connect(self.positionChanged)
        self.videoPlayer.stateChanged.connect(self.stateChanged)
        self.videoPlayer.setNotifyInterval(10) # Check for changes (to duration, position, state) every X ms
        self.videoPlayer.setVideoOutput(self.ui.videoWidget) # Video will output to the video widget

        # Slider
        self.ui.slider.sliderPressed.connect(self.sliderPressed)
        self.ui.slider.sliderMoved.connect(self.sliderMoved)
        self.ui.slider.sliderReleased.connect(self.sliderReleased)

        # Update states
        self.updateStates()


    ##  CALLBACK METHODS ##
    def playPauseButtonClicked(self):
        if self.playing:
            print("Pause!")
            self.pause()
            self.ui.playPauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            print("Play!")
            self.play()
            self.ui.playPauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

    def stopButtonClicked(self):
        # self.ui.slider.setValue(0)
        # self.setPosition(0)
        self.stop()

    def saveButtonClicked(self):
        print("Save!")

    def openButtonClicked(self):
        print("Load!")
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Choose a video",
            QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation),
            "Video files (*mp4 *mp3)")
        # fileName, _ = QFileDialog.getOpenFileName(self, "Open Files")

        if fileName != "":
            # file = open("ProcessedStuff/labels_example.txt","w")
            # file.write("labels = []\n")
            # file.close()
            self.fileProcessed = False
            self.fileUploaded = True
            self.ui.filepathLabel.setText(fileName)
            print("Video filepath: " + fileName)
            self.fileName = fileName
            self.nextLine = 0
            self.updateStates()

    def helpButtonClicked(self):
        print("Help!")
        message = QMessageBox.about(self, 'Help',
        "To begin processing your drone footage, simply press the Open button and select your target file, then press the Detect button.")

    # Threading
    def worker(self, inval):
        # print("in worker, received '%s'" % inval)
        detection.detection_code(self.fileName)
        time.sleep(2)
        return inval

    def on_send_finished(self, result):
        # print("got %s. Type is %s" % (result, type(result)))
        self.processingFinished()
        self.processing = False
        self.fileProcessed = True
        self.updateStates()

    def detectButtonClicked(self):
        print("Track!")
        self.processing = True
        self.updateStates()
        # time.sleep(500)
        # QApplication.processEvents()

        # progress = QProgressDialog("Detection in progress...", "Close", 0, 100, self);

        self.t1 = PyQtThreading.RunThread(self.worker, self.on_send_finished, "test")

        # DETECTION
        # detection.detection_code(self.fileName)
        #
        # self.processingFinished()
        # self.updateStates()

    def sliderPressed(self):
        self.originalState = self.state
        self.pause()

    def sliderMoved(self):
        newPosition = self.ui.slider.value()
        self.resetNextLine(newPosition)
        self.updateLabel(newPosition)
        self.updateDurationInfo(newPosition)
        self.videoPlayer.setPosition(newPosition)

    def sliderReleased(self):
        newPosition = self.ui.slider.value()
        self.setPosition(newPosition)

    def durationChanged(self, duration):
        self.duration = duration
        self.ui.slider.setMaximum(duration)

    def positionChanged(self, position):
        if not self.playing:
            return
        # Update video progress bar
        self.ui.slider.setValue(position)
        # Update information label
        self.updateLabel(position)
        self.updateDurationInfo(position)

    def stateChanged(self, state):
        self.state = state
        if state == QMediaPlayer.StoppedState:
            self.stop()

    ## Helper Functions ##
    def play(self):
        self.playing = True
        self.videoPlayer.play()

    def pause(self):
        self.playing = False
        self.videoPlayer.pause()

    def stop(self):
        self.playing = False
        self.ui.slider.setValue(0)
        self.setPosition(0)
        self.videoPlayer.stop()
        self.originalState = QMediaPlayer.StoppedState
        self.ui.playPauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def setPosition(self, position):
        self.resetNextLine(position)
        self.updateLabel(position)
        self.updateDurationInfo(position)
        self.videoPlayer.setPosition(position)
        if self.originalState == QMediaPlayer.PlayingState:
            self.play()

    def updateStates(self):
        self.ui.playPauseButton.setEnabled(self.fileProcessed and not self.processing)
        self.ui.stopButton.setEnabled(self.fileProcessed and not self.processing)
        self.ui.slider.setEnabled(self.fileProcessed)
        # self.ui.saveButton.setEnabled(self.videoLoaded)
        self.ui.detectButton.setEnabled(self.fileUploaded and not self.processing)
        self.ui.openButton.setEnabled(not self.processing)

    def processingFinished(self):
        print("Text file location: " + self.textFilePath)
        file = open(self.textFilePath, "r")
        self.labels = [line.split(',') for line in file]
        file.close()
        print(self.processedVideoPath)
        self.videoPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.processedVideoPath)))
        self.videoLoaded = True
        self.processing = False

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

    def updateDurationInfo(self, currentInfo):
        duration = self.duration / 1000
        currentInfo /= 1000
        if currentInfo or duration:
            currentTime = QTime((currentInfo/3600)%60, (currentInfo/60)%60,
                    currentInfo%60, (currentInfo*1000)%1000)
            totalTime = QTime((duration/3600)%60, (duration/60)%60,
                    duration%60, (duration*1000)%1000);

            format = 'hh:mm:ss' if duration > 3600 else 'mm:ss'
            tStr = currentTime.toString(format) + " / " + totalTime.toString(format)
        else:
            tStr = ""

        self.ui.durationLabel.setText(tStr)

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
