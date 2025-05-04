from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def crear_presupuesto_pdf(
    nombre_empresa,
    nombre_cliente,
    ciudad,
    direccion,
    espacio,
    lista_items,
    total,
    numero_presupuesto,
    logo_path=None,
    imagenes_gpt=None,
    imagenes_cliente=None,
    planos=None,
    cutlist_resultado=None
):
    nombre_archivo = f"presupuesto_{nombre_cliente.replace(' ', '_')}.pdf"
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    width, height = letter

    # Encabezado con logo y empresa
    if logo_path and os.path.exists(logo_path):
        c.drawImage(logo_path, 50, height - 100, width=100, height=50, preserveAspectRatio=True)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(200, height - 50, f"PRESUPUESTO - {nombre_empresa}")

    # Datos del cliente
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 130, f"N° Presupuesto: {numero_presupuesto}")
    c.drawString(300, height - 130, f"Fecha: {datetime.today().strftime('%d/%m/%Y')}")
    c.drawString(50, height - 150, f"Cliente: {nombre_cliente}")
    c.drawString(50, height - 170, f"Ciudad: {ciudad}")
    c.drawString(50, height - 190, f"Dirección: {direccion}")
    c.drawString(50, height - 210, f"Espacio: {espacio}")

    y = height - 240
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Detalle de mobiliario presupuestado:")
    y -= 20

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Código")
    c.drawString(100, y, "Descripción")
    c.drawString(250, y, "Cantidad")
    c.drawString(320, y, "Precio Unitario")
    c.drawString(420, y, "Subtotal")
    y -= 20

    c.setFont("Helvetica", 10)
    for item in lista_items or []:
        subtotal = item.get('cantidad', 0) * item.get('precio_unitario', 0)
        c.drawString(50, y, str(item.get('codigo', '')))
        c.drawString(100, y, str(item.get('descripcion', '')))
        c.drawString(250, y, str(item.get('cantidad', 0)))
        c.drawString(320, y, f"${item.get('precio_unitario', 0)}")
        c.drawString(420, y, f"${subtotal}")
        y -= 20
        if y < 100:
            c.showPage()
            y = height - 50

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Total general: ${total}")
    y -= 40

    # Cutlist
    if cutlist_resultado:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Lista de materiales (Cutlist):")
        y -= 20
        c.setFont("Helvetica", 10)
        for pieza in cutlist_resultado.get('piezas', []):
            c.drawString(50, y, f"{pieza['nombre']} - {pieza['ancho']}cm x {pieza['alto']}cm x {pieza['cantidad']}u")
            y -= 15
            if y < 100:
                c.showPage()
                y = height - 50
        c.drawString(50, y, f"Tableros necesarios: {cutlist_resultado.get('tableros_necesarios', 0)}")
        y -= 40

    # Imágenes GPT
    if imagenes_gpt:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Propuestas visuales generadas por Espacio Creativo:")
        y -= 20
        for img_path in imagenes_gpt:
            if os.path.exists(img_path):
                c.drawImage(img_path, 50, y - 200, width=500, height=200, preserveAspectRatio=True)
                y -= 220
                if y < 100:
                    c.showPage()
                    y = height - 50

    # Imágenes cliente
    if imagenes_cliente:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Imágenes enviadas por el cliente:")
        y -= 20
        for img_path in imagenes_cliente:
            if os.path.exists(img_path):
                c.drawImage(img_path, 50, y - 200, width=500, height=200, preserveAspectRatio=True)
                y -= 220
                if y < 100:
                    c.showPage()
                    y = height - 50

    # Planos
    if planos:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Planos con medidas:")
        y -= 20
        for plano_path in planos:
            if os.path.exists(plano_path):
                c.drawImage(plano_path, 50, y - 200, width=500, height=200, preserveAspectRatio=True)
                y -= 220
                if y < 100:
                    c.showPage()
                    y = height - 50

    # Pie de página
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 30, "Generado por Espacio Creativo GPTs")

    c.save()
    print(f"Archivo PDF generado: {os.path.abspath(nombre_archivo)}")
