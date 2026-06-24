from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

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

clientes = [
    {"id": 1, "nombre": "Aldair", "email": "aldair@gmail.com"},
]
next_cliente_id = 2

vendedores = [
    {"id": 1, "nombre": "Juan Perez"}
]
next_vendedor_id = 2

productos = [
    {"id": 1, "nombre": "Laptop", "precio": 2500}
]
next_producto_id = 2

facturas = [
    {"id": 1, "cliente": "Aldair", "vendedor": "Juan Perez", "total": 2500}
]
next_factura_id = 2

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
    return render_template("index.html",
        nombre_usuario=current_user.username,
        clientes=clientes, vendedores=vendedores,
        productos=productos, facturas=facturas)

@app.route("/clientes")
@login_required
def clientes_list():
    return render_template("clientes/list.html", clientes=clientes)

@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def clientes_create():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        errores = []
        if not nombre:
            errores.append("El nombre es obligatorio")
        if not email:
            errores.append("El email es obligatorio")
        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("clientes/create.html", nombre=nombre, email=email)
        global next_cliente_id
        cliente = {"id": next_cliente_id, "nombre": nombre, "email": email}
        clientes.append(cliente)
        next_cliente_id += 1
        flash("Cliente creado exitosamente", "success")
        return redirect(url_for("clientes_list"))
    return render_template("clientes/create.html", nombre="", email="")

@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def clientes_edit(id):
    cliente = next((c for c in clientes if c["id"] == id), None)
    if not cliente:
        flash("Cliente no encontrado", "error")
        return redirect(url_for("clientes_list"))
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        errores = []
        if not nombre:
            errores.append("El nombre es obligatorio")
        if not email:
            errores.append("El email es obligatorio")
        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("clientes/edit.html", cliente=cliente)
        cliente["nombre"] = nombre
        cliente["email"] = email
        flash("Cliente actualizado exitosamente", "success")
        return redirect(url_for("clientes_list"))
    return render_template("clientes/edit.html", cliente=cliente)

@app.route("/clientes/eliminar/<int:id>")
@login_required
def clientes_delete(id):
    global clientes
    cliente = next((c for c in clientes if c["id"] == id), None)
    if not cliente:
        flash("Cliente no encontrado", "error")
    else:
        clientes = [c for c in clientes if c["id"] != id]
        flash("Cliente eliminado exitosamente", "success")
    return redirect(url_for("clientes_list"))


@app.route("/vendedores")
@login_required
def vendedores_list():
    return render_template("vendedores/list.html", vendedores=vendedores)

@app.route("/vendedores/nuevo", methods=["GET", "POST"])
@login_required
def vendedores_create():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        if not nombre:
            flash("El nombre es obligatorio", "error")
            return render_template("vendedores/create.html", nombre=nombre)
        global next_vendedor_id
        vendedor = {"id": next_vendedor_id, "nombre": nombre}
        vendedores.append(vendedor)
        next_vendedor_id += 1
        flash("Vendedor creado exitosamente", "success")
        return redirect(url_for("vendedores_list"))
    return render_template("vendedores/create.html", nombre="")

@app.route("/vendedores/editar/<int:id>", methods=["GET", "POST"])
@login_required
def vendedores_edit(id):
    vendedor = next((v for v in vendedores if v["id"] == id), None)
    if not vendedor:
        flash("Vendedor no encontrado", "error")
        return redirect(url_for("vendedores_list"))
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        if not nombre:
            flash("El nombre es obligatorio", "error")
            return render_template("vendedores/edit.html", vendedor=vendedor)
        vendedor["nombre"] = nombre
        flash("Vendedor actualizado exitosamente", "success")
        return redirect(url_for("vendedores_list"))
    return render_template("vendedores/edit.html", vendedor=vendedor)

@app.route("/vendedores/eliminar/<int:id>")
@login_required
def vendedores_delete(id):
    global vendedores
    vendedor = next((v for v in vendedores if v["id"] == id), None)
    if not vendedor:
        flash("Vendedor no encontrado", "error")
    else:
        vendedores = [v for v in vendedores if v["id"] != id]
        flash("Vendedor eliminado exitosamente", "success")
    return redirect(url_for("vendedores_list"))


@app.route("/productos")
@login_required
def productos_list():
    return render_template("productos/list.html", productos=productos)

@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def productos_create():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        precio_str = request.form.get("precio", "").strip()
        errores = []
        if not nombre:
            errores.append("El nombre es obligatorio")
        if not precio_str:
            errores.append("El precio es obligatorio")
        else:
            try:
                precio = float(precio_str)
                if precio < 0:
                    errores.append("El precio no puede ser negativo")
            except ValueError:
                errores.append("El precio debe ser un número válido")
                precio = 0
        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("productos/create.html", nombre=nombre, precio=precio_str)
        global next_producto_id
        producto = {"id": next_producto_id, "nombre": nombre, "precio": precio}
        productos.append(producto)
        next_producto_id += 1
        flash("Producto creado exitosamente", "success")
        return redirect(url_for("productos_list"))
    return render_template("productos/create.html", nombre="", precio="")

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def productos_edit(id):
    producto = next((p for p in productos if p["id"] == id), None)
    if not producto:
        flash("Producto no encontrado", "error")
        return redirect(url_for("productos_list"))
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        precio_str = request.form.get("precio", "").strip()
        errores = []
        if not nombre:
            errores.append("El nombre es obligatorio")
        if not precio_str:
            errores.append("El precio es obligatorio")
        else:
            try:
                precio = float(precio_str)
                if precio < 0:
                    errores.append("El precio no puede ser negativo")
            except ValueError:
                errores.append("El precio debe ser un número válido")
                precio = producto["precio"]
        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("productos/edit.html", producto=producto)
        producto["nombre"] = nombre
        producto["precio"] = precio
        flash("Producto actualizado exitosamente", "success")
        return redirect(url_for("productos_list"))
    return render_template("productos/edit.html", producto=producto)

@app.route("/productos/eliminar/<int:id>")
@login_required
def productos_delete(id):
    global productos
    producto = next((p for p in productos if p["id"] == id), None)
    if not producto:
        flash("Producto no encontrado", "error")
    else:
        productos = [p for p in productos if p["id"] != id]
        flash("Producto eliminado exitosamente", "success")
    return redirect(url_for("productos_list"))


@app.route("/facturas")
@login_required
def facturas_list():
    return render_template("facturas/list.html", facturas=facturas)

@app.route("/facturas/nueva", methods=["GET", "POST"])
@login_required
def facturas_create():
    if request.method == "POST":
        cliente = request.form.get("cliente", "").strip()
        vendedor = request.form.get("vendedor", "").strip()
        total_str = request.form.get("total", "").strip()
        errores = []
        if not cliente:
            errores.append("Debe seleccionar un cliente")
        if not vendedor:
            errores.append("Debe seleccionar un vendedor")
        if not total_str:
            errores.append("Debe seleccionar un producto")
        else:
            try:
                total = float(total_str)
                if total < 0:
                    errores.append("El total no puede ser negativo")
            except ValueError:
                errores.append("El total debe ser un número válido")
                total = 0
        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("facturas/create.html", clientes=clientes, vendedores=vendedores, productos=productos)
        global next_factura_id
        factura = {"id": next_factura_id, "cliente": cliente, "vendedor": vendedor, "total": total}
        facturas.append(factura)
        next_factura_id += 1
        flash("Factura creada exitosamente", "success")
        return redirect(url_for("facturas_list"))
    return render_template("facturas/create.html", clientes=clientes, vendedores=vendedores, productos=productos)

@app.route("/facturas/editar/<int:id>", methods=["GET", "POST"])
@login_required
def facturas_edit(id):
    factura = next((f for f in facturas if f["id"] == id), None)
    if not factura:
        flash("Factura no encontrada", "error")
        return redirect(url_for("facturas_list"))
    if request.method == "POST":
        cliente = request.form.get("cliente", "").strip()
        vendedor = request.form.get("vendedor", "").strip()
        total_str = request.form.get("total", "").strip()
        errores = []
        if not cliente:
            errores.append("Debe seleccionar un cliente")
        if not vendedor:
            errores.append("Debe seleccionar un vendedor")
        if not total_str:
            errores.append("Debe seleccionar un producto")
        else:
            try:
                total = float(total_str)
                if total < 0:
                    errores.append("El total no puede ser negativo")
            except ValueError:
                errores.append("El total debe ser un número válido")
                total = factura["total"]
        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("facturas/edit.html", factura=factura, clientes=clientes, vendedores=vendedores, productos=productos)
        factura["cliente"] = cliente
        factura["vendedor"] = vendedor
        factura["total"] = total
        flash("Factura actualizada exitosamente", "success")
        return redirect(url_for("facturas_list"))
    return render_template("facturas/edit.html", factura=factura, clientes=clientes, vendedores=vendedores, productos=productos)

@app.route("/facturas/eliminar/<int:id>")
@login_required
def facturas_delete(id):
    global facturas
    factura = next((f for f in facturas if f["id"] == id), None)
    if not factura:
        flash("Factura no encontrada", "error")
    else:
        facturas = [f for f in facturas if f["id"] != id]
        flash("Factura eliminada exitosamente", "success")
    return redirect(url_for("facturas_list"))

if __name__ == '__main__':
    app.run(debug=True)