import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, 
                            QWidget, QLineEdit, QHBoxLayout, QGroupBox, QRadioButton, QListWidget)

from text import *
from ventana_2 import *

class Ventana1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.connects()
        self.set_appear()
        self.show()

    def initUI(self):
        self.btn_incial=QLabel(txt_incial,self)
        self.btn_intrucciones=QLabel(txt_instrucciones,self)
        self.btn_next=QPushButton(txt_next,self)
    


    def nextclick(self):
        self.tw=Ventana2()
        self.hide()

    def connects(self):
        self.btn_next.clicked.connect(self.nextclick)

    def set_appear(self):
        self.setWindowTitle(txt_titulo)
        self.resize(win_width, win_height)
        self.move(win_x, win_y)
        v_line=QVBoxLayout()
        v_line.addWidget(self.btn_incial, alignment= Qt.AlignCenter)
        v_line.addWidget(self.btn_intrucciones, alignment= Qt.AlignCenter)
        v_line.addWidget(self.btn_next, alignment= Qt.AlignCenter)
        self.setLayout(v_line)

if __name__ == '__main__':
    app=QApplication([])
    mw=Ventana1()
    sys.exit(app.exec_())
