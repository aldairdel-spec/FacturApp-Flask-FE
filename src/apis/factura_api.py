import requests
from src.apis import BACKEND_URL


def obtener_todas():
    response = requests.get(f"{BACKEND_URL}/facturas/")
    if response.status_code == 200:
        return response.json()
    return []


def obtener_por_id(id):
    response = requests.get(f"{BACKEND_URL}/facturas/{id}")
    if response.status_code == 200:
        return response.json()
    return None


def crear(data):
    response = requests.post(f"{BACKEND_URL}/facturas/", json=data)
    return response.status_code, response.json()


def actualizar(id, data):
    response = requests.put(f"{BACKEND_URL}/facturas/{id}", json=data)
    return response.status_code, response.json()


def eliminar(id):
    response = requests.delete(f"{BACKEND_URL}/facturas/{id}")
    return response.status_code, response.json()

