from flask import Blueprint, render_template, request, redirect, url_for, flash
from apis.cliente_api import obtener_todos, obtener_por_id, crear, actualizar, eliminar

clientes_bp = Blueprint('clientes', __name__)


@clientes_bp.route("/clientes")
def clientes_list():
    resultado = obtener_todos()

    if resultado["status"] == 200:
        return render_template("clientes/list.html", clientes=resultado["datos"])

    flash(resultado["datos"].get("message", "Error al obtener clientes"), "error")
    return render_template("clientes/list.html", clientes=[])


@clientes_bp.route("/clientes/nuevo", methods=["GET", "POST"])
def clientes_create():
    if request.method == "POST":
        documento = request.form.get("documento", "").strip()
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        telefono = request.form.get("telefono", "").strip()
        direccion = request.form.get("direccion", "").strip()

        errores = []
        if not documento:
            errores.append("El documento es obligatorio")
        if not nombre:
            errores.append("El nombre es obligatorio")
        if not email:
            errores.append("El email es obligatorio")

        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("clientes/create.html",
                                   documento=documento, nombre=nombre,
                                   email=email, telefono=telefono,
                                   direccion=direccion)

        datos = {
            "documento": documento,
            "nombre": nombre,
            "email": email,
            "telefono": telefono,
            "direccion": direccion
        }

        resultado = crear(datos)

        if resultado["status"] == 201:
            flash("Cliente creado exitosamente", "success")
            return redirect(url_for("clientes.clientes_list"))

        mensaje = resultado["datos"].get("message", "Error al crear el cliente")
        flash(mensaje, "error")
        return render_template("clientes/create.html",
                               documento=documento, nombre=nombre,
                               email=email, telefono=telefono,
                               direccion=direccion)

    return render_template("clientes/create.html",
                           documento="", nombre="",
                           email="", telefono="",
                           direccion="")


@clientes_bp.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
def clientes_edit(id):
    if request.method == "POST":
        documento = request.form.get("documento", "").strip()
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        telefono = request.form.get("telefono", "").strip()
        direccion = request.form.get("direccion", "").strip()

        errores = []
        if not documento:
            errores.append("El documento es obligatorio")
        if not nombre:
            errores.append("El nombre es obligatorio")
        if not email:
            errores.append("El email es obligatorio")

        if errores:
            for e in errores:
                flash(e, "error")
            cliente = {"id": id, "documento": documento, "nombre": nombre,
                       "email": email, "telefono": telefono,
                       "direccion": direccion}
            return render_template("clientes/edit.html", cliente=cliente)

        datos = {
            "documento": documento,
            "nombre": nombre,
            "email": email,
            "telefono": telefono,
            "direccion": direccion
        }

        resultado = actualizar(id, datos)

        if resultado["status"] == 200:
            flash("Cliente actualizado exitosamente", "success")
            return redirect(url_for("clientes.clientes_list"))

        mensaje = resultado["datos"].get("message", "Error al actualizar el cliente")
        flash(mensaje, "error")
        cliente = {"id": id, "documento": documento, "nombre": nombre,
                   "email": email, "telefono": telefono,
                   "direccion": direccion}
        return render_template("clientes/edit.html", cliente=cliente)

    resultado = obtener_por_id(id)

    if resultado["status"] == 200:
        return render_template("clientes/edit.html", cliente=resultado["datos"])

    flash(resultado["datos"].get("message", "Cliente no encontrado"), "error")
    return redirect(url_for("clientes.clientes_list"))


@clientes_bp.route("/clientes/eliminar/<int:id>")
def clientes_delete(id):
    resultado = eliminar(id)

    if resultado["status"] == 200:
        flash("Cliente eliminado exitosamente", "success")
    else:
        flash(resultado["datos"].get("message", "Error al eliminar el cliente"), "error")

    return redirect(url_for("clientes.clientes_list"))
