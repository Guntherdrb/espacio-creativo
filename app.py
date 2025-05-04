from flask import Flask, request, jsonify, send_file
from pdf_generator import crear_presupuesto_pdf
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "¡Servidor Flask de Espacio Creativo funcionando!"

@app.route('/generar_presupuesto', methods=['POST'])
def generar_presupuesto():
    try:
        datos = request.form

        # Recolectar datos, si faltan usar 'N/A' o valores por defecto
        nombre_empresa = datos.get('nombre_empresa', 'N/A')
        nombre_cliente = datos.get('nombre_cliente', 'N/A')
        ciudad = datos.get('ciudad', 'N/A')
        direccion = datos.get('direccion', 'N/A')
        espacio = datos.get('espacio', 'N/A')
        numero_presupuesto = datos.get('numero_presupuesto', '0001')
        total = float(datos.get('total', 0))

        # Crear carpeta uploads si no existe
        upload_dir = './uploads'
        os.makedirs(upload_dir, exist_ok=True)

        # Guardar logo si viene
        logo_path = None
        logo = request.files.get('logo')
        if logo:
            logo_path = os.path.join(upload_dir, logo.filename)
            logo.save(logo_path)

        # Guardar imágenes GPT
        imagenes_gpt = []
        for file in request.files.getlist('imagenes_gpt'):
            img_path = os.path.join(upload_dir, file.filename)
            file.save(img_path)
            imagenes_gpt.append(img_path)

        # Guardar imágenes cliente
        imagenes_cliente = []
        for file in request.files.getlist('imagenes_cliente'):
            img_path = os.path.join(upload_dir, file.filename)
            file.save(img_path)
            imagenes_cliente.append(img_path)

        # Guardar planos
        planos = []
        for file in request.files.getlist('planos'):
            plano_path = os.path.join(upload_dir, file.filename)
            file.save(plano_path)
            planos.append(plano_path)

        # Convertir lista_items
        try:
            lista_items = eval(datos.get('lista_items', '[]'))  # Si no viene nada, usar lista vacía
        except Exception:
            lista_items = []

        # Crear PDF
        nombre_archivo = f"presupuesto_{nombre_cliente.replace(' ', '_')}.pdf"
        crear_presupuesto_pdf(
            nombre_empresa=nombre_empresa,
            nombre_cliente=nombre_cliente,
            ciudad=ciudad,
            direccion=direccion,
            espacio=espacio,
            lista_items=lista_items,
            total=total,
            numero_presupuesto=numero_presupuesto,
            logo_path=logo_path,
            imagenes_gpt=imagenes_gpt,
            imagenes_cliente=imagenes_cliente,
            planos=planos
        )

        return jsonify({
            "mensaje": "Presupuesto generado",
            "archivo": nombre_archivo,
            "url_descarga": f"/descargar/{nombre_archivo}"
        })

    except Exception as e:
        return jsonify({"mensaje": f"Error al generar presupuesto: {str(e)}"}), 500

@app.route('/descargar/<nombre_archivo>')
def descargar_archivo(nombre_archivo):
    ruta_archivo = f"./{nombre_archivo}"
    return send_file(ruta_archivo, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
