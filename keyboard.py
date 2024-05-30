from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor
from win32.win32api import GetSystemMetrics
import cv2
import mediapipe as mp
import numpy as np

screen_width = GetSystemMetrics(0)  
screen_height = GetSystemMetrics(1) 

cap = cv2.VideoCapture(0)  

mpHands = mp.solutions.hands   
hands = mpHands.Hands(static_image_mode=False,  
                      max_num_hands=2,  
                      min_detection_confidence=0.5,  
                      min_tracking_confidence=0.5)  

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()


        self.setWindowOpacity(0.5)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

        self.priority_indices = [8, 12, 16, 20, 4]
        self.screen_x = 0
        self.screen_y = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_hand_position)
        self.timer.start(int(30))  

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            cap.release()
            cv2.destroyAllWindows()
            self.close()

    def update_hand_position(self):
        success, img = cap.read()
        displayed_point = False
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        if results.multi_hand_landmarks:
            for handlms in results.multi_hand_landmarks:
                for index in self.priority_indices:
                    if handlms.landmark[index] is not None and not displayed_point:
                        lm = handlms.landmark[index] 
                        h, w, c = img.shape
                        self.screen_x = int((1-lm.x) * screen_width)
                        self.screen_y = int(lm.y * screen_height)
                        displayed_point = True

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(QColor(0, 0, 255, 255), 12))
        try:
            painter.drawPoint(self.screen_x, self.screen_y)
        except:
            pass

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
