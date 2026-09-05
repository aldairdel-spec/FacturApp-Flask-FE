import requests
from src.apis import BACKEND_URL, auth_headers


def obtener_todos():
    """Obtiene todos los productos del backend."""
    try:
        respuesta = requests.get(f"{BACKEND_URL}/productos/", headers=auth_headers(), timeout=5)
        return {
            "status": respuesta.status_code,
            "datos": respuesta.json()
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": 503,
            "datos": {"message": "No se pudo conectar con el servidor. Verifique que el backend esté ejecutándose."}
        }
    except requests.exceptions.Timeout:
        return {
            "status": 504,
            "datos": {"message": "La petición al backend tardó demasiado. Intente de nuevo."}
        }
    except Exception as e:
        return {
            "status": 500,
            "datos": {"message": f"Error inesperado: {str(e)}"}
        }


def obtener_paginado(page=1, per_page=10):
    """Obtiene una página de productos del backend."""
    try:
        respuesta = requests.get(
            f"{BACKEND_URL}/productos/",
            params={"page": page, "per_page": per_page},
            headers=auth_headers(),
            timeout=5,
        )
        datos = respuesta.json()
        if respuesta.status_code == 200:
            return {
                "status": 200,
                "datos": datos.get("datos", []),
                "page": datos.get("page", page),
                "per_page": datos.get("per_page", per_page),
                "total": datos.get("total", 0),
                "total_pages": datos.get("total_pages", 0),
            }
        return {"status": respuesta.status_code, "datos": datos}
    except requests.exceptions.ConnectionError:
        return {
            "status": 503,
            "datos": {"message": "No se pudo conectar con el servidor. Verifique que el backend esté ejecutándose."}
        }
    except requests.exceptions.Timeout:
        return {
            "status": 504,
            "datos": {"message": "La petición al backend tardó demasiado. Intente de nuevo."}
        }
    except Exception as e:
        return {
            "status": 500,
            "datos": {"message": f"Error inesperado: {str(e)}"}
        }


def obtener_por_id(id):
    """Obtiene un producto por su ID del backend."""
    try:
        respuesta = requests.get(f"{BACKEND_URL}/productos/{id}", headers=auth_headers(), timeout=5)
        return {
            "status": respuesta.status_code,
            "datos": respuesta.json()
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": 503,
            "datos": {"message": "No se pudo conectar con el servidor. Verifique que el backend esté ejecutándose."}
        }
    except requests.exceptions.Timeout:
        return {
            "status": 504,
            "datos": {"message": "La petición al backend tardó demasiado. Intente de nuevo."}
        }
    except Exception as e:
        return {
            "status": 500,
            "datos": {"message": f"Error inesperado: {str(e)}"}
        }


def crear(datos):
    """Crea un producto nuevo en el backend."""
    try:
        respuesta = requests.post(f"{BACKEND_URL}/productos/", json=datos, headers=auth_headers(), timeout=5)
        return {
            "status": respuesta.status_code,
            "datos": respuesta.json()
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": 503,
            "datos": {"message": "No se pudo conectar con el servidor. Verifique que el backend esté ejecutándose."}
        }
    except requests.exceptions.Timeout:
        return {
            "status": 504,
            "datos": {"message": "La petición al backend tardó demasiado. Intente de nuevo."}
        }
    except Exception as e:
        return {
            "status": 500,
            "datos": {"message": f"Error inesperado: {str(e)}"}
        }


def actualizar(id, datos):
    """Actualiza un producto existente en el backend."""
    try:
        respuesta = requests.put(f"{BACKEND_URL}/productos/{id}", json=datos, headers=auth_headers(), timeout=5)
        return {
            "status": respuesta.status_code,
            "datos": respuesta.json()
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": 503,
            "datos": {"message": "No se pudo conectar con el servidor. Verifique que el backend esté ejecutándose."}
        }
    except requests.exceptions.Timeout:
        return {
            "status": 504,
            "datos": {"message": "La petición al backend tardó demasiado. Intente de nuevo."}
        }
    except Exception as e:
        return {
            "status": 500,
            "datos": {"message": f"Error inesperado: {str(e)}"}
        }


def eliminar(id):
    """Elimina un producto del backend."""
    try:
        respuesta = requests.delete(f"{BACKEND_URL}/productos/{id}", headers=auth_headers(), timeout=5)
        return {
            "status": respuesta.status_code,
            "datos": respuesta.json()
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": 503,
            "datos": {"message": "No se pudo conectar con el servidor. Verifique que el backend esté ejecutándose."}
        }
    except requests.exceptions.Timeout:
        return {
            "status": 504,
            "datos": {"message": "La petición al backend tardó demasiado. Intente de nuevo."}
        }
    except Exception as e:
        return {
            "status": 500,
            "datos": {"message": f"Error inesperado: {str(e)}"}
        }

