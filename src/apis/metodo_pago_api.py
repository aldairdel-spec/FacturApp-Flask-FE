import requests
from src.apis import BACKEND_URL


def obtener_todos():
    """Obtiene todos los metodos de pago del backend."""
    try:
        respuesta = requests.get(f"{BACKEND_URL}/metodos_pago/", timeout=5)
        return {
            "status": respuesta.status_code,
            "datos": respuesta.json()
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": 503,
            "datos": {"message": "No se pudo conectar con el servidor. Verifique que el backend este ejecutandose."}
        }
    except requests.exceptions.Timeout:
        return {
            "status": 504,
            "datos": {"message": "La peticion al backend tardo demasiado. Intente de nuevo."}
        }
    except Exception as e:
        return {
            "status": 500,
            "datos": {"message": f"Error inesperado: {str(e)}"}
        }


def obtener_por_id(id):
    """Obtiene un metodo de pago por su ID del backend."""
    try:
        respuesta = requests.get(f"{BACKEND_URL}/metodos_pago/{id}", timeout=5)
        return {
            "status": respuesta.status_code,
            "datos": respuesta.json()
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": 503,
            "datos": {"message": "No se pudo conectar con el servidor. Verifique que el backend este ejecutandose."}
        }
    except requests.exceptions.Timeout:
        return {
            "status": 504,
            "datos": {"message": "La peticion al backend tardo demasiado. Intente de nuevo."}
        }
    except Exception as e:
        return {
            "status": 500,
            "datos": {"message": f"Error inesperado: {str(e)}"}
        }


def crear(datos):
    """Crea un metodo de pago nuevo en el backend."""
    try:
        respuesta = requests.post(f"{BACKEND_URL}/metodos_pago/", json=datos, timeout=5)
        return {
            "status": respuesta.status_code,
            "datos": respuesta.json()
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": 503,
            "datos": {"message": "No se pudo conectar con el servidor. Verifique que el backend este ejecutandose."}
        }
    except requests.exceptions.Timeout:
        return {
            "status": 504,
            "datos": {"message": "La peticion al backend tardo demasiado. Intente de nuevo."}
        }
    except Exception as e:
        return {
            "status": 500,
            "datos": {"message": f"Error inesperado: {str(e)}"}
        }


def actualizar(id, datos):
    """Actualiza un metodo de pago existente en el backend."""
    try:
        respuesta = requests.put(f"{BACKEND_URL}/metodos_pago/{id}", json=datos, timeout=5)
        return {
            "status": respuesta.status_code,
            "datos": respuesta.json()
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": 503,
            "datos": {"message": "No se pudo conectar con el servidor. Verifique que el backend este ejecutandose."}
        }
    except requests.exceptions.Timeout:
        return {
            "status": 504,
            "datos": {"message": "La peticion al backend tardo demasiado. Intente de nuevo."}
        }
    except Exception as e:
        return {
            "status": 500,
            "datos": {"message": f"Error inesperado: {str(e)}"}
        }


def eliminar(id):
    """Elimina un metodo de pago del backend."""
    try:
        respuesta = requests.delete(f"{BACKEND_URL}/metodos_pago/{id}", timeout=5)
        return {
            "status": respuesta.status_code,
            "datos": respuesta.json()
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": 503,
            "datos": {"message": "No se pudo conectar con el servidor. Verifique que el backend este ejecutandose."}
        }
    except requests.exceptions.Timeout:
        return {
            "status": 504,
            "datos": {"message": "La peticion al backend tardo demasiado. Intente de nuevo."}
        }
    except Exception as e:
        return {
            "status": 500,
            "datos": {"message": f"Error inesperado: {str(e)}"}
        }

