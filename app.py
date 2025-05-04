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

        # Validar campos obligatorios
        nombre_cliente = datos.get('nombre_cliente')
        ciudad = datos.get('ciudad')
        direccion = datos.get('direccion')
        lista_items = datos.get('lista_items')
        total = datos.get('total')

        if not nombre_cliente:
            return jsonify({"error": "Falta el nombre del cliente."}), 400
        if not ciudad:
            return jsonify({"error": "Falta la ciudad."}), 400
        if not direccion:
            return jsonify({"error": "Falta la dirección."}), 400
        if not lista_items:
            return jsonify({"error": "Falta la lista de ítems."}), 400
        if not total:
            return jsonify({"error": "Falta el total."}), 400

        nombre_archivo = f"presupuesto_{nombre_cliente.replace(' ', '_')}.pdf"
        upload_dir = './uploads'
        os.makedirs(upload_dir, exist_ok=True)

        # Guardar logo (opcional)
        logo = request.files.get('logo')
        logo_path = None
        if logo:
            logo_path = os.path.join(upload_dir, logo.filename)
            logo.save(logo_path)

        # Guardar imágenes GPT (opcional)
        imagenes_gpt = []
        for file in request.files.getlist('imagenes_gpt'):
            img_path = os.path.join(upload_dir, file.filename)
            file.save(img_path)
            imagenes_gpt.append(img_path)

        # Guardar imágenes cliente (opcional)
        imagenes_cliente = []
        for file in request.files.getlist('imagenes_cliente'):
            img_path = os.path.join(upload_dir, file.filename)
            file.save(img_path)
            imagenes_cliente.append(img_path)

        # Guardar planos (opcional)
        planos = []
        for file in request.files.getlist('planos'):
            plano_path = os.path.join(upload_dir, file.filename)
            file.save(plano_path)
            planos.append(plano_path)

        # Convertir lista_items
        lista_items = eval(lista_items)
        cutlist_resultado = eval(datos.get('cutlist', 'None'))

        crear_presupuesto_pdf(
            nombre_cliente=nombre_cliente,
            ciudad=ciudad,
            direccion=direccion,
            lista_items=lista_items,
            total=float(total),
            cutlist_resultado=cutlist_resultado,
            nombre_archivo=nombre_archivo,
            numero_presupuesto=datos.get('numero_presupuesto', '0001'),
            logo_path=logo_path,
            imagenes_gpt=imagenes_gpt,
            imagenes_cliente=imagenes_cliente,
            planos=planos
        )

        return jsonify({
            "mensaje": "Presupuesto generado correctamente.",
            "archivo": nombre_archivo,
            "url_descarga": f"/descargar/{nombre_archivo}"
        })

    except Exception as e:
        return jsonify({"error": f"Error interno al generar presupuesto: {str(e)}"}), 500

@app.route('/descargar/<nombre_archivo>')
def descargar_archivo(nombre_archivo):
    ruta_archivo = f"./{nombre_archivo}"
    return send_file(ruta_archivo, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
