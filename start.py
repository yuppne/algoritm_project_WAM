import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

from PyQt5.QtGui import *
import subway_resource.geoLine as line
import subway_resource.linkData as link
import subway_resource.nodeData as node
import os.path
import meet
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie



# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("stUI.ui")[0]

class St_WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # QPixmap 객체 생성 후 이미지 파일을 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        #self.qPixmapFileVar = QPixmap()
        # self.qPixmapFileVar.load("st_background.jpg")
        #self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(1286)
        # self.label.setPixmap(self.qPixmapFileVar)
        self.topbgcolor.setStyleSheet("background-color: #B00020")
        self.topbgcolor_2.setStyleSheet("background-color: #B00020")
        self.to_meet_lbl.setStyleSheet("Color: white")
        self.to_way_lbl.setStyleSheet("Color: white")
        self.start_bg.setPixmap(QPixmap("start_page.png"))
        # set qmovie as label
        self.movie = QMovie("train.gif")
        self.label_gif.setMovie(self.movie)
        self.movie.start()

        # set the title
        title = "W.A.M"
        self.setWindowTitle(title)


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    #app = QApplication(sys.argv)
    app = QtWidgets.QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    sw_Window = St_WindowClass()

    # 프로그램 화면을 보여주는 코드
    # myWindow.show()

    window = QtWidgets.QMainWindow()

    sw_Window.setupUi(window)
    window.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    #app.exec_()
    sys.exit(app.exec_())


