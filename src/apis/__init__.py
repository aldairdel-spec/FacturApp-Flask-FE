import requests
from flask import session, flash, redirect, url_for
from flask_login import logout_user

BACKEND_URL = "http://127.0.0.1:5000"


def auth_headers():
    """Devuelve los headers con el JWT almacenado en la sesión."""
    token = session.get("access_token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def login_backend(usuario, password):
    """Autentica contra el backend y devuelve (status, json)."""
    try:
        respuesta = requests.post(
            f"{BACKEND_URL}/usuarios/login",
            json={"usuario": usuario, "password": password},
            timeout=5,
        )
        return respuesta.status_code, respuesta.json()
    except requests.exceptions.ConnectionError:
        return 503, {"message": "No se pudo conectar con el servidor. Verifique que el backend esté ejecutándose."}
    except requests.exceptions.Timeout:
        return 504, {"message": "La petición al backend tardó demasiado. Intente de nuevo."}
    except Exception as e:
        return 500, {"message": f"Error inesperado: {str(e)}"}


def cerrar_sesion_por_401():
    """Limpia la sesión JWT y redirige al login cuando el backend responde 401."""
    session.pop("access_token", None)
    session.pop("user_info", None)
    logout_user()
    flash("Su sesión ha expirado. Inicie sesión nuevamente.", "error")
    return redirect(url_for("login"))
