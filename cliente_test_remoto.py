import requests

URL_BASE = "https://espacio-creativo-production.up.railway.app"

# Datos
data = {
    'nombre_cliente': 'Juan Pérez',
    'ciudad': 'Caracas',
    'direccion': 'Calle Falsa 123',
    'lista_items': str([
        {'codigo': 'C001', 'descripcion': 'Mueble bajo', 'cantidad': 2, 'precio_unitario': 120},
        {'codigo': 'C002', 'descripcion': 'Mueble alto', 'cantidad': 1, 'precio_unitario': 150}
    ]),
    'total': '390',
    'numero_presupuesto': '0001'
}

# Archivos opcionales (logo + imágenes)
files = {
    # 'logo': open('ruta_a_logo.png', 'rb'),  # si tienes un logo, descomenta y ajusta
    # 'imagenes_gpt': (None, ''),  # agregar archivos reales si tienes
    # 'imagenes_cliente': (None, ''),  # agregar archivos reales si tienes
    # 'planos': (None, '')  # agregar archivos reales si tienes
}

try:
    response = requests.post(f"{URL_BASE}/generar_presupuesto", data=data, files=files)
    response.raise_for_status()
    print("✅ Respuesta del servidor:")
    print(response.json())
except Exception as e:
    print(f"❌ Error al enviar solicitud: {e}")
    if e.response is not None:
        print(e.response.text)
