import requests

URL_BASE = "https://espacio-creativo-production.up.railway.app"

data = {
    "nombre_cliente": "Juan Pérez",
    "ciudad": "Caracas",
    "direccion": "Avenida Central",
    "numero_presupuesto": "0001",
    "lista_items": [
        {"codigo": "C001", "descripcion": "Mueble bajo", "cantidad": 2, "precio_unitario": 120},
        {"codigo": "C002", "descripcion": "Mueble alto", "cantidad": 1, "precio_unitario": 150}
    ],
    "total": 390,
    "imagenes_gpt": [
        "https://via.placeholder.com/500x300.png?text=Propuesta1"
    ],
    "imagenes_cliente": [
        "https://via.placeholder.com/500x300.png?text=Cliente1"
    ],
    "planos": [
        "https://via.placeholder.com/500x300.png?text=Plano1"
    ]
}

try:
    response = requests.post(f"{URL_BASE}/generar_presupuesto", json=data)
    response.raise_for_status()
    print("✅ Respuesta del servidor:")
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"❌ Error al enviar solicitud: {e}")
    if response is not None:
        print(response.text)
