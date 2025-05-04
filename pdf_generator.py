from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from datetime import datetime
import os

def crear_presupuesto_pdf(nombre_cliente, ciudad, direccion, lista_items, total, cutlist_resultado=None, nombre_archivo='presupuesto.pdf', numero_presupuesto='0001', logo_path=None):
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    width, height = letter

    if logo_path and os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        c.drawImage(logo, 50, height - 80, width=80, preserveAspectRatio=True, mask='auto')

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 50, "PRESUPUESTO DE MOBILIARIO")
    c.setLineWidth(2)
    c.setStrokeColor(colors.grey)
    c.line(50, height - 60, width - 50, height - 60)

    c.setFont("Helvetica", 10)
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    c.drawString(50, height - 100, f"N° Presupuesto: {numero_presupuesto}")
    c.drawString(200, height - 100, f"Fecha: {fecha_actual}")
    c.drawString(50, height - 115, f"Cliente: {nombre_cliente}")
    c.drawString(50, height - 130, f"Ciudad: {ciudad}")
    c.drawString(50, height - 145, f"Dirección: {direccion}")

    y = height - 175

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Detalle de mobiliario presupuestado:")
    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Código")
    c.drawString(100, y, "Descripción")
    c.drawString(250, y, "Cantidad")
    c.drawString(320, y, "Precio Unitario")
    c.drawString(420, y, "Subtotal")
    c.line(50, y - 2, width - 50, y - 2)
    y -= 15
    c.setFont("Helvetica", 10)

    for item in lista_items:
        subtotal = item['cantidad'] * item['precio_unitario']
        c.drawString(50, y, item['codigo'])
        c.drawString(100, y, item['descripcion'])
        c.drawString(250, y, str(item['cantidad']))
        c.drawString(320, y, f"${item['precio_unitario']}")
        c.drawString(420, y, f"${subtotal}")
        y -= 15
        if y < 100:
            c.showPage()
            y = height - 50

    c.setFont("Helvetica-Bold", 11)
    c.line(50, y, width - 50, y)
    y -= 15
    c.drawString(320, y, "Total general:")
    c.drawString(420, y, f"${total}")
    y -= 30

    if cutlist_resultado:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Resumen de materiales (Cutlist):")
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Área total de piezas: {cutlist_resultado['area_total_piezas']} cm²")
        y -= 15
        c.drawString(50, y, f"Área por tablero: {cutlist_resultado['area_por_tablero']} cm²")
        y -= 15
        c.drawString(50, y, f"Tableros necesarios: {cutlist_resultado['tableros_necesarios']}")
        y -= 30

    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.grey)
    c.drawCentredString(width / 2, 50, "Este presupuesto fue generado por Espacio Creativo GPTs")
    c.setFillColor(colors.black)

    c.save()
    print(f"Archivo PDF generado: {os.path.abspath(nombre_archivo)}")
