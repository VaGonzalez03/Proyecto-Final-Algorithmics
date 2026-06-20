import sys
from PyQt5.QtCore import Qt
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QTextDocument
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, 
                            QWidget, QLineEdit, QHBoxLayout, QGroupBox, QRadioButton, QListWidget, QMessageBox)

from text import *
from ventana_1 import *
from ventana_2 import *

class Ventana3(QWidget):
    def __init__(self,datos_tabla=None, contratista="", cliente=""):
        super().__init__()
        self.datos_tabla= datos_tabla if datos_tabla is not None else []
        self.contratista= contratista
        self.cliente= cliente
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
        self.btn_txt_importar_pdf.clicked.connect(self.importar_pdf)

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
        datos += f"Contratista: {self.contratista}\n" f"Cliente: {self.cliente}\n\n"
        datos += "Concepto\t  Cantidad\t  Precio\t  Total\n"
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

    def importar_pdf(self):
        # 1. Validación de datos vacíos
        if not self.datos_tabla:
            QMessageBox.warning(self, "Datos Vacíos", "No hay datos para exportar.")
            return

        try:
            # --- CÁLCULO DEL TOTAL GENERAL Y FILAS ---
            total_general = 0.0
            filas_html = ""
            
            for fila in self.datos_tabla:
                concepto = fila[0] if len(fila) > 0 else ""
                cantidad = fila[1] if len(fila) > 1 else "0"
                precio = fila[2] if len(fila) > 2 else "0.0"
                total = fila[3] if len(fila) > 3 else "0.0"
                
                # Construcción de la fila HTML para cada concepto, con estilos para evitar saltos de línea en números y títulos cortos
                filas_html += f"""
                <tr>
                    <td style="text-align: left;">{concepto}</td>
                    <td class="nobrk" style="text-align: right;">{cantidad}</td>
                    <td class="nobrk" style="text-align: right;">{precio}</td>
                    <td class="nobrk" style="text-align: right;">{total}</td>
                </tr>
                """
                # función para sumar al total general, con manejo de excepciones para datos no numéricos o vacíos
                try:
                    total_general += float(total)
                except (ValueError, TypeError):
                    pass

            # estrtuctura HTML completa para el PDF
            html_content = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40pt; color: #000000; }}
                    h2 {{ text-align: center; font-size: 26pt; font-weight: bold; }}
                    p {{ font-size: 16pt; margin: 8pt 0; }}
                    
                    table {{ border-collapse: collapse; }}
                    th, td {{ border: 2pt solid #000000; padding: 12pt; font-size: 15pt; vertical-align: middle; }}
                    th {{ background-color: #f2f2f2; font-weight: bold; }}
                    
                    .nobrk {{ white-space: nowrap; }}
                    .total {{ font-weight: bold; font-size: 18pt; }}
                </style>
            </head>
            <body>
                <h2>=== COTIZACIÓN / PRESUPUESTO ===</h2>
                
                <p><b>Contratista:</b> {self.contratista}</p>
                <p><b>Cliente:</b> {self.cliente}</p>
                
                <br><br>
                
                <table width="100%">
                    <thead>
                        <tr>
                            <th width="55%" style="text-align: left;">Concepto</th>
                            <th width="15%" class="nobrk" style="text-align: right;">Cantidad</th>
                            <th width="15%" class="nobrk" style="text-align: right;">Precio</th>
                            <th width="15%" class="nobrk" style="text-align: right;">Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filas_html}
                        <tr class="total">
                            <td colspan="3" style="text-align: left; padding: 15pt 12pt;">TOTAL GENERAL:</td>
                            <td class="nobrk" style="text-align: right; padding: 15pt 12pt;">{total_general:.2f}</td>
                        </tr>
                    </tbody>
                </table>
            </body>
            </html>
            """

            # Creación del documento y configuración de la impresora para generar el PDF
            documento = QTextDocument()
            documento.setHtml(html_content)

            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName("cotizacion.pdf")

            documento.print_(printer)

            QMessageBox.information(self, "Éxito", "Archivo 'cotizacion.pdf' guardado correctamente.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo PDF: {e}")

if __name__ == '__main__':
    app=QApplication([])
    mw=Ventana3()
    sys.exit(app.exec_())

