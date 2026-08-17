import requests
from apis import BACKEND_URL


def obtener_todos():
    """Obtiene todos los clientes del backend."""
    try:
        respuesta = requests.get(f"{BACKEND_URL}/clientes/", timeout=5)
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
    """Obtiene un cliente por su ID del backend."""
    try:
        respuesta = requests.get(f"{BACKEND_URL}/clientes/{id}", timeout=5)
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
    """Crea un cliente nuevo en el backend."""
    try:
        respuesta = requests.post(f"{BACKEND_URL}/clientes/", json=datos, timeout=5)
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
    """Actualiza un cliente existente en el backend."""
    try:
        respuesta = requests.put(f"{BACKEND_URL}/clientes/{id}", json=datos, timeout=5)
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
    """Elimina un cliente del backend."""
    try:
        respuesta = requests.delete(f"{BACKEND_URL}/clientes/{id}", timeout=5)
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
