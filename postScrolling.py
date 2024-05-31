from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QFont
from win32.win32api import GetSystemMetrics
import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import pygetwindow as gw
import time

screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)
mpDraw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_detection_confidence=0.6,
                      min_tracking_confidence=0.6)

class postScrolling(QMainWindow):
    def __init__(self, window='Edge', reset=2, fps=30, quit=2):
        super(postScrolling, self).__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.5)
        self.showFullScreen()

        self.window = window
        self.priority_indices = [8, 12, 16, 20, 4]
        self.screen_x = 0
        self.screen_y = 0
        self.point_position = (0, 0)  # 记录坐标
        self.thr_positon = (screen_width * 0.08, screen_height * 0.08)
        self.fps = fps
        self.img = None  # 用于保存摄像头图像
        self.judge = False
        self.standard = (0, 0)
        self.count = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_hand_position)
        self.timer.start(int(1000 / self.fps))

        self.quit_hover_start_time = None
        self.hover_duration = quit # 退出悬浮时长
        self.reset_time = reset  # 重置标准位置时间
        # 退出区域矩形框位置
        self.quit_box = QRect(screen_width - 320, 240, 320, screen_height  - 240)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.quit_program()

    def quit_program(self):
        cap.release()
        cv2.destroyAllWindows()
        self.close()

    def update_hand_position(self):
        success, img = cap.read()
        if success:
            self.img = img 

        displayed_point = False
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        if results.multi_hand_landmarks:
            for handlms in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(self.img, handlms, mpHands.HAND_CONNECTIONS)
                index_finger_tip = handlms.landmark[8]

                h, w, c = img.shape
                self.screen_x = int((1 - index_finger_tip.x) * screen_width)
                self.screen_y = int(index_finger_tip.y * screen_height)

                if self.quit_box.contains(self.screen_x, self.screen_y):
                    if self.quit_hover_start_time is None:
                        self.quit_hover_start_time = time.time()
                    elif time.time() - self.quit_hover_start_time >= self.hover_duration:
                        self.quit_program()
                else:
                    self.quit_hover_start_time = None

                if abs(self.screen_x - self.point_position[0]) < self.thr_positon[0] and abs(self.screen_y - self.point_position[1]) < self.thr_positon[1]:
                    self.count += 1
                else:
                    pass

                self.point_position = (self.screen_x, self.screen_y)

                if self.count > self.fps * self.reset_time:
                    self.standard = (self.screen_x, self.screen_y)
                    self.count = 0

                if self.screen_y - self.standard[1] < -self.thr_positon[1] and self.judge:
                    self.judge = False
                    self.switch_to_window(self.window)  
                    pyautogui.press('down')
                    print("Down", self.screen_y - self.standard[1], self.screen_y, self.standard[1])
                
                elif self.screen_y - self.standard[1] > self.thr_positon[1] and self.judge:
                    self.judge = False
                    self.switch_to_window(self.window) 
                    pyautogui.press('up')
                    print("Up", self.screen_y - self.standard[1], self.screen_y, self.standard[1])

                if abs(self.screen_y - self.standard[1]) < self.thr_positon[1]:
                    self.judge = True

                displayed_point = True

        self.update()

    def switch_to_window(self, window_name):
        try:
            window = gw.getWindowsWithTitle(window_name)[0]
            window.activate()
        except IndexError:
            print(f"No window found with title: {window_name}")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(QColor(0, 0, 255, 255), 12))

        try:
            painter.drawPoint(self.screen_x, self.screen_y)
        except:
            pass

        try:
            painter.setPen(QPen(QColor(255, 0, 0, 255), 12))
            painter.drawPoint(screen_width - 10, self.standard[1])
            painter.drawText(screen_width - 100, self.standard[1], "Standard Position")
        except:
            pass

        try:
            painter.setPen(QPen(QColor(255, 0, 0, 255), 3))
            painter.drawRect(self.quit_box)
            painter.setFont(QFont('Arial', 20))
            painter.drawText(self.quit_box, Qt.AlignRight | Qt.AlignTop, "退出区")
        except:
            pass

        try:
            if self.img is not None:
                imgRGB = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
                h, w, ch = imgRGB.shape
                bytesPerLine = ch * w
                qt_image = QImage(imgRGB.data, w, h, bytesPerLine, QImage.Format_RGB888)
                qt_pixmap = QPixmap.fromImage(qt_image)
                scaled_pixmap = qt_pixmap.scaled(320, 240, Qt.KeepAspectRatio)  
                painter.drawPixmap(screen_width - scaled_pixmap.width(), 0, scaled_pixmap)  
        except:
            pass

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = postScrolling()
    window.show()
    sys.exit(app.exec_())
