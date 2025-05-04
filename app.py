from flask import Flask, request, jsonify, send_file
from pdf_generator import crear_presupuesto_pdf
import os
import traceback
import re
from datetime import datetime

app = Flask(__name__)

# Exponer especificación OpenAPI para ChatGPT Plugins
@app.route('/.well-known/openapi.json', methods=['GET'])
def openapi_spec():
    spec_path = os.path.join(app.root_path, '.well-known', 'openapi.json')
    if os.path.exists(spec_path):
        return send_file(spec_path, mimetype='application/json')
    return jsonify({"error": "Especificación no encontrada"}), 404

@app.route('/')
def index():
    return "¡Servidor Flask de Espacio Creativo funcionando!"

@app.route('/generar_presupuesto', methods=['POST'])
def generar_presupuesto():
    try:
        datos = request.form

        # Recolectar datos seguros
        nombre_empresa = datos.get('nombre_empresa', 'Empresa Desconocida')
        nombre_cliente = datos.get('nombre_cliente', 'Cliente Desconocido')
        ciudad = datos.get('ciudad', 'Ciudad no especificada')
        direccion = datos.get('direccion', 'Dirección no especificada')
        espacio = datos.get('espacio', 'Espacio no especificado')
        # Obtener o generar automáticamente el número de presupuesto
        numero_presupuesto = datos.get('numero_presupuesto')
        if not numero_presupuesto:
            numero_presupuesto = datetime.now().strftime('%Y%m%d%H%M%S')

        try:
            total = float(datos.get('total', 0))
        except ValueError:
            total = 0

        # Crear carpetas necesarias
        upload_dir = './uploads'
        output_dir = './outputs'
        os.makedirs(upload_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)

        # Preparar nombre de archivo seguro a partir del número de presupuesto
        safe_numero = re.sub(r'[^A-Za-z0-9_-]', '_', numero_presupuesto)
        nombre_archivo = os.path.join(output_dir, f"presupuesto_{safe_numero}.pdf")

        # Guardar logo
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
            lista_items = eval(datos.get('lista_items', '[]'))
        except Exception:
            lista_items = []

        # Llamar función para crear PDF
        crear_presupuesto_pdf(
            nombre_archivo=nombre_archivo,
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

        # Construir URL de descarga completa para que sea clickable en UI
        archivo_nombre = os.path.basename(nombre_archivo)
        # request.host_url incluye el esquema y host con slash final
        base_url = request.host_url.rstrip('/')
        descarga_url = f"{base_url}/descargar/{archivo_nombre}"
        return jsonify({
            "mensaje": "✅ Presupuesto generado correctamente",
            "archivo": archivo_nombre,
            "url_descarga": descarga_url
        })

    except Exception as e:
        print("❌ ERROR INTERNO:", str(e))
        print(traceback.format_exc())
        return jsonify({
            "mensaje": f"Error al generar presupuesto: {str(e)}",
            "detalle": traceback.format_exc()
        }), 500

@app.route('/descargar/<nombre_archivo>')
def descargar_archivo(nombre_archivo):
    ruta_archivo = os.path.join('./outputs', nombre_archivo)
    if os.path.exists(ruta_archivo):
        # Enviar PDF con cabeceras para permitir CORS en ChatGPT Plugin UI
        response = send_file(ruta_archivo, as_attachment=True)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        return jsonify({"mensaje": "Archivo no encontrado"}), 404

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
