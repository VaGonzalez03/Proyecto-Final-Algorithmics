from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QDoubleSpinBox, QHeaderView, QMainWindow, QPushButton, QLabel, QSpinBox, QTableWidget, QVBoxLayout, 
                            QWidget, QLineEdit, QHBoxLayout, QGroupBox, QRadioButton, QListWidget)

from text import *
from ventana_1 import Ventana1
from ventana_3 import *

class Ventana2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
       # self.connects()
        self.set_appear()
        self.show()

    def initUI(self):
        self.lbl_concepto=QLabel(txt_concepto,self)
        self.lbl_cantidad=QLabel(txt_cantidad,self)
        self.lbl_precio=QLabel(txt_precio,self)
        self.btn_concepto=QLineEdit(self)
        self.btn_cantidad=QSpinBox(self)
        self.btn_precio=QDoubleSpinBox(self)
        self.btn_agregar=QPushButton(txt_agregar,self)
        self.btn_tabla=QTableWidget(self)
        self.btn_tabla.setRowCount(0)
        self.btn_tabla.setColumnCount(4)
        self.btn_tabla.setHorizontalHeaderLabels([txt_concepto, txt_cantidad, txt_precio, txt_total])
        self.btn_tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    #def nextclick(self):
       # self.tw=Ventana1()
      #  self.hide()

    #def connects(self):
       # self.btn_next.clicked.connect(self.nextclick)

    def set_appear(self):
        self.setWindowTitle(txt_titulo)
        self.resize(win_width, win_height)
        self.move(win_x, win_y)
        v_line=QVBoxLayout()
        h_layout=QHBoxLayout()
        h_layout.addWidget(self.lbl_concepto)
        h_layout.addWidget(self.btn_concepto)
        h_layout.addSpacing(20)
        h_layout.addWidget(self.lbl_cantidad)
        h_layout.addWidget(self.btn_cantidad)
        h_layout.addSpacing(20)
        h_layout.addWidget(self.lbl_precio)
        h_layout.addWidget(self.btn_precio)
        h_layout.addSpacing(20)
        h_layout.addWidget(self.btn_agregar)
        h_layout.addStretch()
        v_line.addSpacing(50)
        v_line.addLayout(h_layout)
        v_line.addSpacing(50)
        v_line.addWidget(self.btn_tabla)
        v_line.addStretch()
        self.setLayout(v_line)
