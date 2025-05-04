from flask import Flask, request, jsonify, send_file
from pdf_generator import crear_presupuesto_pdf
from cutlist_calculator import calcular_cutlist
import os
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return "¡Servidor Flask de Espacio Creativo funcionando!"

@app.route('/generar_presupuesto', methods=['POST'])
def generar_presupuesto():
    if request.is_json:
        datos = request.get_json()
    else:
        return jsonify({"error": "El cuerpo debe ser JSON"}), 400

    nombre_archivo = f"presupuesto_{datos['nombre_cliente'].replace(' ', '_')}.pdf"

    # Crear carpeta uploads si no existe
    upload_dir = './uploads'
    os.makedirs(upload_dir, exist_ok=True)

    # Descargar imágenes generadas por GPT
    imagenes_gpt_locales = []
    for i, url in enumerate(datos.get('imagenes_gpt', [])):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                img_path = os.path.join(upload_dir, f"gpt_{i}.jpg")
                with open(img_path, 'wb') as f:
                    f.write(response.content)
                imagenes_gpt_locales.append(img_path)
        except Exception as e:
            print(f"Error al descargar imagen GPT {url}: {e}")

    # Descargar imágenes enviadas por el cliente
    imagenes_cliente_locales = []
    for i, url in enumerate(datos.get('imagenes_cliente', [])):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                img_path = os.path.join(upload_dir, f"cliente_{i}.jpg")
                with open(img_path, 'wb') as f:
                    f.write(response.content)
                imagenes_cliente_locales.append(img_path)
        except Exception as e:
            print(f"Error al descargar imagen cliente {url}: {e}")

    # Descargar planos
    planos_locales = []
    for i, url in enumerate(datos.get('planos', [])):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                img_path = os.path.join(upload_dir, f"plano_{i}.jpg")
                with open(img_path, 'wb') as f:
                    f.write(response.content)
                planos_locales.append(img_path)
        except Exception as e:
            print(f"Error al descargar plano {url}: {e}")

    lista_items = datos['lista_items']
    cutlist_resultado = datos.get('cutlist', None)

    crear_presupuesto_pdf(
        nombre_cliente=datos['nombre_cliente'],
        ciudad=datos['ciudad'],
        direccion=datos['direccion'],
        lista_items=lista_items,
        total=float(datos['total']),
        cutlist_resultado=cutlist_resultado,
        nombre_archivo=nombre_archivo,
        numero_presupuesto=datos.get('numero_presupuesto', '0001'),
        logo_path=None,  # puedes agregar si lo necesitas
        imagenes_gpt=imagenes_gpt_locales,
        imagenes_cliente=imagenes_cliente_locales,
        planos=planos_locales
    )

    return jsonify({
        "mensaje": "Presupuesto generado con imágenes",
        "archivo": nombre_archivo,
        "url_descarga": f"/descargar/{nombre_archivo}"
    })

@app.route('/descargar/<nombre_archivo>')
def descargar_archivo(nombre_archivo):
    ruta_archivo = f"./{nombre_archivo}"
    if os.path.exists(ruta_archivo):
        return send_file(ruta_archivo, as_attachment=True)
    else:
        return jsonify({"error": "Archivo no encontrado"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
