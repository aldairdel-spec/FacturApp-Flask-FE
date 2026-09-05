from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from src.controladores import registrar_controladores
from src.apis import login_backend
from src.apis import cliente_api, producto_api, usuario_api, factura_api

app = Flask(__name__)
app.secret_key = 'facturapp_secret_key_2024'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_info):
        self.user_info = user_info
        self.id = str(user_info.get("usuario") or user_info.get("id") or "")
        self.username = user_info.get("usuario", "")

@login_manager.user_loader
def load_user(username):
    user_info = session.get("user_info")
    if user_info and str(user_info.get("usuario") or user_info.get("id") or "") == username:
        return User(user_info)
    return None

clientes = []

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        usuario = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        status, data = login_backend(usuario, password)
        access_token = data.get("access_token") if isinstance(data, dict) else None
        user_info = data.get("usuario") if isinstance(data, dict) else None
        if status == 200 and access_token and user_info:
            session["access_token"] = access_token
            session["user_info"] = user_info
            login_user(User(user_info))
            flash(f"Bienvenido, {user_info.get('usuario')}", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("index"))
        mensaje = data.get("message", "Usuario o contraseña incorrectos") if isinstance(data, dict) else "Usuario o contraseña incorrectos"
        flash(mensaje, "error")
    return render_template("auth/login.html")

@app.route("/logout")
@login_required
def logout():
    session.pop("access_token", None)
    session.pop("user_info", None)
    logout_user()
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for("login"))

@app.route("/")
@login_required
def index():
    # Clientes
    try:
        res_clientes = cliente_api.obtener_todos()
        total_clientes = len(res_clientes["datos"]) if res_clientes["status"] == 200 else 0
    except Exception:
        total_clientes = 0

    # Productos
    try:
        res_productos = producto_api.obtener_todos()
        total_productos = len(res_productos["datos"]) if res_productos["status"] == 200 else 0
    except Exception:
        total_productos = 0

    # Vendedores (usuarios)
    try:
        res_vendedores = usuario_api.obtener_todos()
        total_vendedores = len(res_vendedores["datos"]) if res_vendedores["status"] == 200 else 0
    except Exception:
        total_vendedores = 0

    # Facturas
    try:
        total_facturas = len(factura_api.obtener_todas())
    except Exception:
        total_facturas = 0

    return render_template("index.html",
        nombre_usuario=current_user.username,
        total_clientes=total_clientes,
        total_productos=total_productos,
        total_vendedores=total_vendedores,
        total_facturas=total_facturas)


registrar_controladores(app)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

