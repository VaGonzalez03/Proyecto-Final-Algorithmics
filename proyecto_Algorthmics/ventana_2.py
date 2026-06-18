from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QDoubleSpinBox, QHeaderView, QMainWindow, QPushButton, QLabel, QSpinBox, QTableWidget, QVBoxLayout, 
                            QWidget, QLineEdit, QHBoxLayout, QGroupBox, QRadioButton, QMessageBox, QTableWidgetItem)

from text import *
from ventana_1 import Ventana1
from ventana_3 import *

class Ventana2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.connects()
        self.set_appear()
        self.show()

    def initUI(self):
        # Etiquetas para los campos de concepto, cantidad y precio
        self.lbl_concepto=QLabel(txt_concepto,self)
        self.lbl_cantidad=QLabel(txt_cantidad,self)
        self.lbl_precio=QLabel(txt_precio,self)


        # Campos de entrada para concepto, cantidad y precio
        self.btn_concepto=QLineEdit(self)
        self.btn_cantidad=QSpinBox(self)
        self.btn_cantidad.setRange(0, 9999)  # Establecer un rango para la cantidad
        self.btn_precio=QDoubleSpinBox(self)
        self.btn_precio.setRange(0.0, 9999.99)  # Establecer un rango para el precio

        # Botones para agregar el concepto a la tabla y para culminar la cotización/presupuesto
        self.btn_agregar=QPushButton(txt_agregar,self)
        self.btn_culminar=QPushButton(txt_terminar,self)

        # Tabla para mostrar los conceptos, cantidades, precios y totales
        self.btn_tabla=QTableWidget(self)
        self.btn_tabla.setRowCount(0)
        self.btn_tabla.setColumnCount(4)
        self.btn_tabla.setHorizontalHeaderLabels([txt_concepto, txt_cantidad, txt_precio, txt_total])
        self.btn_tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Diseño de la ventana utilizando layouts
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
        v_line.addWidget(self.btn_culminar, alignment= Qt.AlignCenter)
        v_line.addStretch()
        self.setLayout(v_line)

    def agregar_click(self):
        # Función para agregar un concepto a la tabla con su cantidad, precio y total
        concepto = self.btn_concepto.text().strip()
        cantidad = self.btn_cantidad.value()
        precio = self.btn_precio.value()
    
        # Comprobamos si el concepto está vacío o si los números están en cero
        if concepto == "" or cantidad == 0 or precio == 0.0:
            
            alerta = QMessageBox(self)
            alerta.setIcon(QMessageBox.Warning) # Icono de advertencia amarillo
            alerta.setWindowTitle("Campos Inválidos")
            alerta.setText("No se puede agregar el producto.")
            alerta.setInformativeText("Asegúrese de escribir un concepto y que la cantidad y el precio sean mayores a cero.")
            alerta.exec_() 
            
            return
    
        # Calcular el total y agregar una nueva fila a la tabla con los datos ingresados
        total=cantidad*precio
        fila_pos = self.btn_tabla.rowCount()
        self.btn_tabla.insertRow(fila_pos)
        self.btn_tabla.setItem(fila_pos, 0, QTableWidgetItem(concepto))
        self.btn_tabla.setItem(fila_pos, 1, QTableWidgetItem(str(cantidad)))
        self.btn_tabla.setItem(fila_pos, 2, QTableWidgetItem(str(precio)))
        self.btn_tabla.setItem(fila_pos, 3, QTableWidgetItem(str(total)))

        # Bloquear la edición de la celda del total para que el usuario no pueda modificarla
        item_total_bloquear = self.btn_tabla.item(fila_pos, 3)
        if item_total_bloquear:
            item_total_bloquear.setFlags(item_total_bloquear.flags() ^ Qt.ItemIsEditable)

        # Limpiar los campos de entrada para el próximo concepto
        self.btn_concepto.clear()
        self.btn_cantidad.setValue(0)       
        self.btn_precio.setValue(0.0)

    def actualizar_valores_tabla(self, row, column):
        
        if column == 1 or column == 2:
            
            # Desconecion de la tabla para evitar un bucle infinito
            self.btn_tabla.cellChanged.disconnect(self.actualizar_valores_tabla)
            
            # Bloque de seguridad para que el programa no se caiga por datos inválidos
            try:
                # Obtenemos los objetos contenedores de las celdas
                item_cantidad = self.btn_tabla.item(row, 1)
                item_precio = self.btn_tabla.item(row, 2)
                
               # validacion de cantidad, precio y la recalculación del total
                if item_cantidad:
                    texto_cantidad = item_cantidad.text()
                    cantidad = float(texto_cantidad)
                else:
                    cantidad = 0.0
                    
                if item_precio:
                    texto_precio = item_precio.text()
                    precio = float(texto_precio)
                else:
                    precio = 0.0
                
                nuevo_total = cantidad * precio
                
                # Actualizacion del total en la tabla
                texto_total = str(nuevo_total)
                celda_total = QTableWidgetItem(texto_total)
                self.btn_tabla.setItem(row, 3, celda_total)
              
                # Bloquear la edición de la celda del total para que el usuario no pueda modificarla
                item_total_actualizado = self.btn_tabla.item(row, 3)
                if item_total_actualizado:
                    item_total_actualizado.setFlags(item_total_actualizado.flags() ^ Qt.ItemIsEditable)
                
            except ValueError:
                # excepción para datos no numéricos o datos vacíos 
                celda_error = QTableWidgetItem("0.0")
                self.btn_tabla.setItem(row, 3, celda_error)
              
                # Bloquear la edición de la celda del total para que el usuario no pueda modificarla
                item_error = self.btn_tabla.item(row, 3)
                if item_error:
                    item_error.setFlags(item_error.flags() ^ Qt.ItemIsEditable)
            
            # reconecion de la tabla
            self.btn_tabla.cellChanged.connect(self.actualizar_valores_tabla)


    def connects(self):
        # Funcion para conectar los botones con la funcion de agregar concepto a la tabla y con la funcion que pasa a la siguiente ventana
        self.btn_agregar.clicked.connect(self.agregar_click)
        self.btn_culminar.clicked.connect(self.nextclick)

        #actualizacion de datos por si el usuario los edita directamente en la tabla, se recalcula el total
        self.btn_tabla.cellChanged.connect(self.actualizar_valores_tabla)

    def nextclick(self):
        # Funcion para pasar a la siguiente ventana
        self.tw=Ventana3()
        self.hide()

    def set_appear(self):
        # Funcion para establecer la apariencia de la ventana (etiqueta, tamaño, ubicación)
        self.setWindowTitle(txt_titulo)
        self.resize(win_width, win_height)
        self.move(win_x, win_y)
