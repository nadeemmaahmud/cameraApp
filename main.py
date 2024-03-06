"""
    Basic Camera App
    Author : -- Nadim Mahmud
"""

import sys 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import QTimer
import cv2
import datetime

class Window(QWidget):
    """ Main app window """
    def __init__(self):
        super().__init__()

        # Variables for app window
        self.windowWidth = 640
        self.windowHeight = 400

        # Image variables
        self.imgWidth = 640
        self.imgHeight = 480

        # Other variables
        self.dT = '0-0-0 0-0-0'
        self.recFlag = False
        self.showDot = True

        # Load icons
        self.camIcon = QIcon(camIconPath)
        self.recIcon = QIcon(recIconPath)
        self.stopIcon = QIcon(stopIconPath)

        # Save video
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

        # Setup the window
        self.setWindowTitle("Nadims Camera")
        self.setGeometry(100, 100, self.windowWidth, self.windowHeight)
        self.setFixedSize(self.windowWidth, self.windowHeight)

        # Setup timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

        self.ui()

    def ui(self):
        """ Contains all UI things """
        # Layout
        grid = QGridLayout()
        self.setLayout(grid)

        # Image label
        self.imageLabel = QLabel(self)
        self.imageLabel.setGeometry(0, 0, self.imgWidth, self.imgHeight)

        # Capture button
        self.camBtn = QPushButton(self)
        self.camBtn.setIcon(self.camIcon)
        self.camBtn.setStyleSheet("border-radius : 30; border : 2px solid blue; border-width : 3px;")
        self.camBtn.setFixedSize(60, 60)
        self.camBtn.clicked.connect(self.saveImg)

        # Record button
        self.recBtn = QPushButton(self)
        #self.recBtn.setIcon(self.recIcon)
        self.recBtn.setStyleSheet("border-radius : 30; border : 2px solid blue; border-width : 3px;")
        self.recBtn.setFixedSize(60, 60)
        self.recBtn.clicked.connect(self.record)

        if not self.timer.isActive():
            self.cap = cv2.VideoCapture(0)
            self.timer.start(20)

        # Add things to layout
        grid.addWidget(self.camBtn, 0, 0)
        grid.addWidget(self.imageLabel, 0, 1, 2, 3)
        grid.addWidget(self.recBtn, 1, 0)

        self.show()

    def update(self):
        """ Update frames """
        _, self.frame = self.cap.read()

        if self.recFlag:
            self.recBtn.setIcon(self.stopIcon)
            if self.showDot:
                self.frame = cv2.circle(self.frame, (20, 70), 5, (0, 0, 255), 10)
            self.showDot = not self.showDot
        else:
            self.recBtn.setIcon(self.recIcon)

        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        step = channel * width

        qFrame = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        self.imageLabel.setPixmap(QPixmap.fromImage(qFrame))

    def saveImg(self):
        """ Save images from camers """
        self.dateTime()
        cv2.imwrite(f"/Users/nadimmahmud/Documents/Coding/Phitron/basicCameraApp/myCaps/{self.dT}.jpg", self.frame)
        print("Image saved!")
        
    def record(self):
        """ Record video """
        if self.recFlag:
            self.recFlag = False
            print("Stopping...")
        else:
            self.recFlag = True
            print("Recording...")
            self.dateTime()

            self.out = cv2.VideoWriter(f"/Users/nadimmahmud/Documents/Coding/Phitron/basicCameraApp/myCaps/{self.dT}.avi", self.fourcc, 20.0, (self.imgWidth, self.imgHeight))

    def dateTime(self):
        now = datetime.datetime.now()
        self.dT = now.strftime("%m-%d-%y %H-%M-%S")

# Run
if __name__ == '__main__':
    camIconPath = '/Users/nadimmahmud/Documents/Coding/Phitron/basicCameraApp/assets/camera.png'
    recIconPath = '/Users/nadimmahmud/Documents/Coding/Phitron/basicCameraApp/assets/video.png'
    stopIconPath = '/Users/nadimmahmud/Documents/Coding/Phitron/basicCameraApp/assets/stop.png'

    app = QApplication(sys.argv)
    win = Window()

    sys.exit(app.exec_())