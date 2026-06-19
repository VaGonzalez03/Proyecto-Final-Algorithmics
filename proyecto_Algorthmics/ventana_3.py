import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, 
                            QWidget, QLineEdit, QHBoxLayout, QGroupBox, QRadioButton, QListWidget, QMessageBox)

from text import *
from ventana_1 import *
from ventana_2 import *

class Ventana3(QWidget):
    def __init__(self,datos_tabla=None):
        super().__init__()
        self.datos_tabla= datos_tabla if datos_tabla is not None else []
        self.initUI()
        self.connects()
        self.set_appear()
        self.show()
        

    def initUI(self):
        #Botones para importar a archivos txt y PDF
        self.btn_txt_importar_txt=QPushButton(txt_importar_txt,self)
        self.btn_txt_importar_pdf=QPushButton(txt_importar_pdf,self)

        v_line=QVBoxLayout()
        layout = QVBoxLayout()
        v_line.addWidget(self.btn_txt_importar_txt, alignment= Qt.AlignCenter)
        v_line.addWidget(self.btn_txt_importar_pdf, alignment= Qt.AlignCenter)
        self.setLayout(v_line)

    def connects(self):
        self.btn_txt_importar_txt.clicked.connect(self.importar_txt)
        #self.btn_txt_importar_pdf.clicked.connect(self.importar_pdf)

    def set_appear(self):
        self.setWindowTitle(txt_titulo)
        self.resize(win_width, win_height)
        self.move(win_x, win_y)

    def importar_txt(self):
        # Función para importar a un archivo txt
        if not self.datos_tabla:
            QMessageBox.warning(self, "Datos Vacíos", "No hay datos para exportar.")
            return

        #Encabezado del archivo txt
        datos= "===COTIZACIÓN/PRESUPUESTO===\n\n"
        datos += "Concepto\tCantidad\tPrecio\tTotal\n"
        datos += "-"*60 + "\n"

        #Variable para total general
        total_general=0.0

        #Recorrer filas de la tabla
        for fila in self.datos_tabla:
            concepto = fila[0] if len(fila)>0  else ""
            cantidad =fila[1] if len(fila)>1 else "0"
            precio = fila[2] if len(fila)>2 else "0.0"
            total = fila[3] if len(fila)>3 else "0.0"

        # Agregar fila al archivo
            datos += f"{concepto:<15}\t{cantidad:>8}\t{precio:>8}\t{total:>8}\n"

        # Sumar al total general
            try:
                total_general += float(total)
            except (ValueError, TypeError):
                pass

        datos += "-"*60 + "\n"
        datos += f"{'TOTAL GENERAL:':<35}\t{total_general:>8}\n"
        # Guardar archivo
        try:
            with open("cotizacion.txt", "w", encoding="utf-8") as file:
                file.write(datos)
            QMessageBox.information(self, "Éxito", "Archivo 'cotizacion.txt' guardado correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo: {e}")

if __name__ == '__main__':
    app=QApplication([])
    mw=Ventana3()
    sys.exit(app.exec_())

