import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, 
                            QWidget, QLineEdit, QHBoxLayout, QGroupBox, QRadioButton, QMessageBox)

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

        #Etiqueta de (inicio)
        self.txt_incial=QLabel(txt_incial,self)
        self.lbl_nombre_contratista=QLabel(txt_nombre_contratista,self)
        self.lbl_nombre_cliente=QLabel(txt_nombre_cliente,self)

        # Cuadros de texto para ingresar el nombre del contratista y el cliente y ajustar su tamaño
        self.txt_nombre_contratista=QLineEdit(self)
        self.txt_nombre_cliente=QLineEdit(self)
        self.txt_nombre_contratista.setFixedWidth(200) 
        self.txt_nombre_cliente.setFixedWidth(200) 

        # Boton para pasar a la siguiente ventana
        self.btn_next=QPushButton(txt_next,self)

        # Diseño de la ventana utilizando layouts
        v_line=QVBoxLayout()
        h_layout=QHBoxLayout()
        v_line.addWidget(self.txt_incial, alignment= Qt.AlignCenter)
        v_line.addWidget(self.lbl_nombre_contratista, alignment= Qt.AlignCenter)
        v_line.addWidget(self.txt_nombre_contratista, alignment= Qt.AlignCenter)
        v_line.addWidget(self.lbl_nombre_cliente, alignment= Qt.AlignCenter)
        v_line.addWidget(self.txt_nombre_cliente, alignment= Qt.AlignCenter)
        v_line.addWidget(self.btn_next, alignment= Qt.AlignCenter)
        self.setLayout(v_line)


    def nextclick(self):
        nombre=[]
        # Obtener los nombres del contratista y cliente, eliminando espacios en blanco al inicio y al final
        contratista = self.txt_nombre_contratista.text().strip()
        cliente = self.txt_nombre_cliente.text().strip()
        
        # verificacion de que los campos no estén vacíos
        if contratista == "" or cliente == "":

            alerta = QMessageBox(self)
            alerta.setIcon(QMessageBox.Critical) # Icono de error crítico (X roja)
            alerta.setWindowTitle("Datos Faltantes")
            alerta.setText("No se puede iniciar el generador.")
            alerta.setInformativeText("Debe ingresar obligatoriamente tanto el Nombre del Contratista como el Nombre del Cliente.")
            alerta.exec_()
            
            return
        nombre.append(contratista)
        nombre.append(cliente)

        # Funcion para pasar a la siguiente ventana
        self.tw=Ventana2(contratista=nombre[0], cliente=nombre[1])
        self.hide()

    def connects(self):
        # Funcion para conectar el boton con la funcion que pasa a la siguiente ventana
        self.btn_next.clicked.connect(self.nextclick)

    def set_appear(self):
        # Funcion para establecer la apariencia de la ventana (etiqueta, tamaño, ubicación)
        self.setWindowTitle(txt_titulo)
        self.resize(win_width, win_height)
        self.move(win_x, win_y)
        
if __name__ == '__main__':
    app=QApplication([])
    
    # Aplicar un estilo de gradiente a todas las ventanas y personalizar los colores de los textos(excepto los mensajes de alerta)
    app.setStyleSheet("""
        Ventana1, Ventana2, Ventana3 {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                        stop:0 #068562, 
                                        stop:1 #013F4A);
        }
        Ventana1 QLabel, Ventana2 QLabel, Ventana3 QLabel {
            color: #ffffff;
            font-weight: bold;
        }
        QMessageBox QLabel {
            color: #000000;
            font-weight: normal;
        }
    """)
    mw=Ventana1()
    sys.exit(app.exec_())
