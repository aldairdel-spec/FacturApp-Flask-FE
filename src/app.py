from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from controladores import registrar_controladores
from apis import cliente_api, producto_api, usuario_api, factura_api

app = Flask(__name__)
app.secret_key = 'facturapp_secret_key_2024'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, username, password_hash):
        self.id = username
        self.username = username
        self.password_hash = password_hash

users = [
    User("admin", generate_password_hash("admin123"))
]

@login_manager.user_loader
def load_user(username):
    return next((u for u in users if u.username == username), None)

clientes = []

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = next((u for u in users if u.username == username), None)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash(f"Bienvenido, {username}", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("index"))
        flash("Usuario o contraseña incorrectos", "error")
    return render_template("auth/login.html")

@app.route("/logout")
@login_required
def logout():
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