import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import subway_resource.geoLine as line
import subway_resource.linkData as link
import subway_resource.nodeData as node
import os.path
from collections import defaultdict
import math
from heapq import heapify, heappush, heappop

import main
import start
import meet
import exe

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.

form_class = uic.loadUiType("wayUI.ui")[0]

class Way_WindowClass(QMainWindow, form_class):
    result = list()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.topbgcolor.setStyleSheet("background-color: #B00020")
        self.topbgcolor_2.setStyleSheet("background-color: #B00020")
        self.howmany.setStyleSheet("Color: white")
        self.people_group_11.setStyleSheet("Color: white")
        self.people_group_22.setStyleSheet("Color: white")
        self.run_button3.setPixmap(QPixmap("go_button.png"))
        #self.run_button.setStyleSheet("background-color : white")
        self.p_start_lbl_11.setStyleSheet("Color: black")
        self.p_start_lbl_22.setStyleSheet("Color: black")

        self.home.setPixmap(QPixmap("cabin.png"))
        self.home.setStyleSheet("background-color: #B00020")
        self.label_snowman.setPixmap(QPixmap("snowman.png"))

        # set the title
        title = "Find Shortest Path"
        self.setWindowTitle(title)

    def get_start_pos(self):
        s = self.p_start_lbl_11.text()
        t = self.p_start_lbl_22.text()

        return s, t





if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = Way_WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()