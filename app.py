from flask import Flask, request, jsonify, send_file
from pdf_generator import crear_presupuesto_pdf
from cutlist_calculator import calcular_cutlist
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "¡Servidor Flask de Espacio Creativo funcionando!"

@app.route('/generar_presupuesto', methods=['POST'])
def generar_presupuesto():
    datos = request.form
    logo = request.files.get('logo')
    nombre_archivo = f"presupuesto_{datos['nombre_cliente'].replace(' ', '_')}.pdf"

    # Guardar logo si existe
    logo_path = None
    if logo:
        upload_dir = './uploads'
        os.makedirs(upload_dir, exist_ok=True)
        logo_path = os.path.join(upload_dir, logo.filename)
        logo.save(logo_path)

    lista_items = eval(datos['lista_items'])  # ¡IMPORTANTE! Esto debe enviarse como string de lista
    cutlist_resultado = eval(datos.get('cutlist', 'None'))

    crear_presupuesto_pdf(
        nombre_cliente=datos['nombre_cliente'],
        ciudad=datos['ciudad'],
        direccion=datos['direccion'],
        lista_items=lista_items,
        total=float(datos['total']),
        cutlist_resultado=cutlist_resultado,
        nombre_archivo=nombre_archivo,
        numero_presupuesto=datos.get('numero_presupuesto', '0001'),
        logo_path=logo_path
    )
    return jsonify({"mensaje": "Presupuesto generado", "archivo": nombre_archivo, "url_descarga": f"/descargar/{nombre_archivo}"})

@app.route('/descargar/<nombre_archivo>')
def descargar_archivo(nombre_archivo):
    ruta_archivo = f"./{nombre_archivo}"
    return send_file(ruta_archivo, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
