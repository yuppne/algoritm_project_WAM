import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import meet2
import main
import start
import meet
import way

def clickable(widget):
    class Filter(QObject):
        clicked = pyqtSignal()  # pyside2 사용자는 pyqtSignal() -> Signal()로 변경

        def eventFilter(self, obj, event):

            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        # The developer can opt for .emit(obj) to get the object within the slot.
                        return True

            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked


def hide_window(Windows):
    for i in range(len(Windows)):
        Windows[i].hide()


def load_st_window():
    hide_window(Windows)
    st_Window.show()


def load_meet_window():
    hide_window(Windows)
    meet_Window.show()


def load_meet_window2():
    hide_window(Windows)
    meet_Window2.show()


def load_main_window():
    hide_window(Windows)
    main_Window.show()


def load_way_window():
    hide_window(Windows)
    way_Window.show()


def run_mid_point():
    p = main_Window.get_start_pos()
    load_meet_window()
    result = main.find_way(p, main_Window.dist)

    text = ""
    for i in result:
        text += i + " "

    if text == '삼각지 ':
        meet_Window.label_3.setPixmap(QPixmap("samgakgi.png"))
    elif text == '잠원 ':
        meet_Window.label_3.setPixmap(QPixmap("jamwon.png"))
    elif text == '선정릉 ':
        meet_Window.label_3.setPixmap(QPixmap("seonjung.png"))
    else:
        meet_Window.label_3.setStyleSheet("background-color: #B00020")

    text += "역에서 만나\n"

    meet_Window.result_consol.setText(text)


def run_way_point():
    s, t = way_Window.get_start_pos()
    load_meet_window2()
    result = main.shortest_path(s, t)

    text = ""
    for i in result:
        if result.index(i) != len(result)-1:
            text += i + " > "
        else:
            text += i

    meet_Window2.result_consol.setText(text)
    meet_Window2.result_consol.setStyleSheet("background-color: #B00020")
    meet_Window2.result_consol.setStyleSheet("QTextEdit {color:white}")


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #######################################
    Windows = list()
    # load all windows
    st_Window = start.St_WindowClass()
    Windows.append(st_Window)

    main_Window = main.Main_WindowClass()
    Windows.append(main_Window)

    load_st_window()

    meet_Window = meet.Meet_WindowClass()
    Windows.append(meet_Window)

    meet_Window2 = meet2.Meet_WindowClass()
    Windows.append(meet_Window2)

    way_Window = way.Way_WindowClass()
    Windows.append(way_Window)

    #########################################

    # st_window event listen
    clickable(st_Window.to_meet_lbl).connect(load_main_window)
    clickable(st_Window.to_way_lbl).connect(load_way_window)

    # meet_window event listen
    clickable(meet_Window.home).connect(load_st_window)
    clickable(meet_Window.to_way_lbl).connect(load_way_window)

    # main_window event listen
    clickable(main_Window.home).connect(load_st_window)
    clickable(main_Window.run_button2).connect(run_mid_point)

    # way_window event listen
    clickable(way_Window.home).connect(load_st_window)
    clickable(way_Window.run_button3).connect(run_way_point)

    clickable(meet_Window2.home).connect(load_st_window)

    # 프로그램 화면을 보여주는 코드
    # myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
