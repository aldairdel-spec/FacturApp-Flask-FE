import requests
from src.apis import BACKEND_URL, auth_headers


def obtener_todas():
    response = requests.get(f"{BACKEND_URL}/facturas/", headers=auth_headers())
    if response.status_code == 200:
        return response.json()
    return []


def obtener_paginadas(page=1, per_page=10):
    """Obtiene una página de facturas del backend."""
    response = requests.get(
        f"{BACKEND_URL}/facturas/",
        params={"page": page, "per_page": per_page},
        headers=auth_headers(),
    )
    if response.status_code == 200:
        datos = response.json()
        return {
            "status": 200,
            "datos": datos.get("datos", []),
            "page": datos.get("page", page),
            "per_page": datos.get("per_page", per_page),
            "total": datos.get("total", 0),
            "total_pages": datos.get("total_pages", 0),
        }
    return {"status": response.status_code, "datos": response.json()}


def obtener_por_id(id):
    response = requests.get(f"{BACKEND_URL}/facturas/{id}", headers=auth_headers())
    if response.status_code == 200:
        return response.json()
    return None


def crear(data):
    response = requests.post(f"{BACKEND_URL}/facturas/", json=data, headers=auth_headers())
    return response.status_code, response.json()


def actualizar(id, data):
    response = requests.put(f"{BACKEND_URL}/facturas/{id}", json=data, headers=auth_headers())
    return response.status_code, response.json()


def eliminar(id):
    response = requests.delete(f"{BACKEND_URL}/facturas/{id}", headers=auth_headers())
    return response.status_code, response.json()

