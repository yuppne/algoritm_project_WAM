import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import subway_resource.geoLine as line
import subway_resource.linkData as link
import subway_resource.nodeData as node
import os.path

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("meetUI.ui")[0]

class Meet_WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # QPixmap 객체 생성 후 이미지 파일을 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        # self.qPixmapFileVar = QPixmap()
        # self.qPixmapFileVar.load("mt_background.png")
        # self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(1286)
        # self.label.setPixmap(self.qPixmapFileVar)

        self.frame.setStyleSheet("background-color: #B00020")

        self.home.setStyleSheet("background-color: #B00020")
        self.home.setPixmap(QPixmap("cabin.png"))
        self.to_way_lbl.setStyleSheet("Color: white")
        self.result_consol.setStyleSheet("background-color: white")


        #self.label_3.setPixmap(QPixmap("samgakgi.png"))


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = Meet_WindowClass()

    # 프로그램 화면을 보여주는 코드
    # myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()