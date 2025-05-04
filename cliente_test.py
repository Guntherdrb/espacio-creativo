import requests

url = 'http://127.0.0.1:5000/generar_presupuesto'

data = {
    'nombre_cliente': 'Juan Pérez',
    'ciudad': 'Caracas',
    'direccion': 'Av. Principal, Torre Espacio Creativo, Caracas',
    'lista_items': str([
        {'codigo': 'C001', 'descripcion': 'Mueble bajo', 'cantidad': 2, 'precio_unitario': 120},
        {'codigo': 'C002', 'descripcion': 'Mueble alto', 'cantidad': 1, 'precio_unitario': 150}
    ]),
    'total': '390',
    'numero_presupuesto': '0001'
}

# Si tienes un logo, coloca aquí el nombre del archivo (debe estar en la misma carpeta)
files = {
    'logo': open('logo_cliente.png', 'rb')  # si no tienes logo, comenta esta línea usando #
}

response = requests.post(url, data=data, files=files)
print(response.json())
