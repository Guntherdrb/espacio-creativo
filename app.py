from flask import Flask, request, jsonify, send_file
from pdf_generator import crear_presupuesto_pdf
import os
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    return "¡Servidor Flask de Espacio Creativo funcionando!"

@app.route('/generar_presupuesto', methods=['POST'])
def generar_presupuesto():
    try:
        datos = request.form
        logo = request.files.get('logo')

        nombre_cliente = datos.get('nombre_cliente', '').replace(' ', '_')
        if not nombre_cliente:
            raise ValueError("Falta el nombre del cliente.")

        nombre_archivo = f"presupuesto_{nombre_cliente}.pdf"

        # Crear carpeta uploads si no existe
        upload_dir = './uploads'
        os.makedirs(upload_dir, exist_ok=True)

        # Guardar logo si viene
        logo_path = None
        if logo:
            logo_path = os.path.join(upload_dir, logo.filename)
            logo.save(logo_path)

        # Guardar imágenes GPT
        imagenes_gpt = []
        for file in request.files.getlist('imagenes_gpt'):
            if file.filename:
                img_path = os.path.join(upload_dir, file.filename)
                file.save(img_path)
                imagenes_gpt.append(img_path)

        # Guardar imágenes cliente
        imagenes_cliente = []
        for file in request.files.getlist('imagenes_cliente'):
            if file.filename:
                img_path = os.path.join(upload_dir, file.filename)
                file.save(img_path)
                imagenes_cliente.append(img_path)

        # Guardar planos
        planos = []
        for file in request.files.getlist('planos'):
            if file.filename:
                plano_path = os.path.join(upload_dir, file.filename)
                file.save(plano_path)
                planos.append(plano_path)

        # Convertir lista_items y cutlist
        try:
            lista_items = eval(datos['lista_items'])  # ¡Debe llegar como string de lista!
        except Exception:
            raise ValueError("El campo 'lista_items' no es válido.")

        cutlist_resultado = None
        if 'cutlist' in datos and datos['cutlist']:
            try:
                cutlist_resultado = eval(datos['cutlist'])
            except Exception:
                raise ValueError("El campo 'cutlist' no es válido.")

        total = float(datos.get('total', 0))
        if total <= 0:
            raise ValueError("El campo 'total' es obligatorio y debe ser mayor a cero.")

        crear_presupuesto_pdf(
            nombre_cliente=datos['nombre_cliente'],
            ciudad=datos.get('ciudad', ''),
            direccion=datos.get('direccion', ''),
            lista_items=lista_items,
            total=total,
            cutlist_resultado=cutlist_resultado,
            nombre_archivo=nombre_archivo,
            numero_presupuesto=datos.get('numero_presupuesto', '0001'),
            logo_path=logo_path,
            imagenes_gpt=imagenes_gpt,
            imagenes_cliente=imagenes_cliente,
            planos=planos
        )

        print(f"✅ PDF generado exitosamente: {nombre_archivo}")
        return jsonify({"mensaje": "Presupuesto generado", "archivo": nombre_archivo, "url_descarga": f"/descargar/{nombre_archivo}"})

    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"❌ ERROR INTERNO: {str(e)}\n{error_trace}")
        return jsonify({"mensaje": f"Error al generar presupuesto: {str(e)}"}), 500

@app.route('/descargar/<nombre_archivo>')
def descargar_archivo(nombre_archivo):
    ruta_archivo = f"./{nombre_archivo}"
    if os.path.exists(ruta_archivo):
        return send_file(ruta_archivo, as_attachment=True)
    else:
        return jsonify({"mensaje": f"Archivo no encontrado: {nombre_archivo}"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
