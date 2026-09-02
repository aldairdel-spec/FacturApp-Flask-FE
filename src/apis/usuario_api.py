import requests
from src.apis import BACKEND_URL


def obtener_todos():
    """Obtiene todos los usuarios (vendedores) del backend."""
    try:
        respuesta = requests.get(f"{BACKEND_URL}/usuarios/", timeout=5)
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


def obtener_por_id(id):
    """Obtiene un usuario (vendedor) por su ID del backend."""
    try:
        respuesta = requests.get(f"{BACKEND_URL}/usuarios/{id}", timeout=5)
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
    """Crea un usuario (vendedor) nuevo en el backend."""
    try:
        respuesta = requests.post(f"{BACKEND_URL}/usuarios/", json=datos, timeout=5)
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
    """Actualiza un usuario (vendedor) existente en el backend."""
    try:
        respuesta = requests.put(f"{BACKEND_URL}/usuarios/{id}", json=datos, timeout=5)
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
    """Elimina un usuario (vendedor) del backend."""
    try:
        respuesta = requests.delete(f"{BACKEND_URL}/usuarios/{id}", timeout=5)
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

