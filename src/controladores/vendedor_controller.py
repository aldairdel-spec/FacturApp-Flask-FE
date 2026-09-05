from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.apis.usuario_api import obtener_todos, obtener_paginado, obtener_por_id, crear, actualizar, eliminar
from src.apis import cerrar_sesion_por_401

vendedores_bp = Blueprint('vendedores', __name__)


@vendedores_bp.route("/vendedores")
def vendedores_list():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    resultado = obtener_paginado(page=page, per_page=per_page)

    if resultado["status"] == 200:
        return render_template("vendedores/list.html",
                               vendedores=resultado["datos"],
                               page=resultado.get("page", page),
                               per_page=resultado.get("per_page", per_page),
                               total=resultado.get("total", 0),
                               total_pages=resultado.get("total_pages", 0),
                               endpoint="vendedores.vendedores_list")

    if resultado["status"] == 401:
        return cerrar_sesion_por_401()

    flash(resultado["datos"].get("message", "Error al obtener vendedores"), "error")
    return render_template("vendedores/list.html", vendedores=[], page=1, per_page=per_page,
                           total=0, total_pages=0, endpoint="vendedores.vendedores_list")


@vendedores_bp.route("/vendedores/nuevo", methods=["GET", "POST"])
def vendedores_create():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        usuario = request.form.get("usuario", "").strip()
        correo = request.form.get("correo", "").strip()
        password = request.form.get("password", "").strip()
        rol = request.form.get("rol", "").strip()
        telefono = request.form.get("telefono", "").strip()

        errores = []
        if not nombre:
            errores.append("El nombre es obligatorio")
        if not apellido:
            errores.append("El apellido es obligatorio")
        if not usuario:
            errores.append("El usuario es obligatorio")
        if not correo:
            errores.append("El correo es obligatorio")
        if not password:
            errores.append("La contraseña es obligatoria")
        if not rol:
            errores.append("El rol es obligatorio")

        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("vendedores/create.html",
                                   nombre=nombre, apellido=apellido,
                                   usuario=usuario, correo=correo,
                                   rol=rol, telefono=telefono)

        datos = {
            "nombre": nombre,
            "apellido": apellido,
            "usuario": usuario,
            "correo": correo,
            "password": password,
            "rol": rol,
            "telefono": telefono
        }

        resultado = crear(datos)

        if resultado["status"] == 201:
            flash("Vendedor creado exitosamente", "success")
            return redirect(url_for("vendedores.vendedores_list"))

        mensaje = resultado["datos"].get("message", "Error al crear el vendedor")
        flash(mensaje, "error")
        return render_template("vendedores/create.html",
                               nombre=nombre, apellido=apellido,
                               usuario=usuario, correo=correo,
                               rol=rol, telefono=telefono)

    return render_template("vendedores/create.html",
                           nombre="", apellido="",
                           usuario="", correo="",
                           rol="", telefono="")


@vendedores_bp.route("/vendedores/editar/<int:id>", methods=["GET", "POST"])
def vendedores_edit(id):
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        usuario = request.form.get("usuario", "").strip()
        correo = request.form.get("correo", "").strip()
        password = request.form.get("password", "").strip()
        rol = request.form.get("rol", "").strip()
        telefono = request.form.get("telefono", "").strip()

        errores = []
        if not nombre:
            errores.append("El nombre es obligatorio")
        if not apellido:
            errores.append("El apellido es obligatorio")
        if not usuario:
            errores.append("El usuario es obligatorio")
        if not correo:
            errores.append("El correo es obligatorio")
        if not rol:
            errores.append("El rol es obligatorio")

        if errores:
            for e in errores:
                flash(e, "error")
            vendedor = {"id": id, "nombre": nombre, "apellido": apellido,
                        "usuario": usuario, "correo": correo,
                        "rol": rol, "telefono": telefono}
            return render_template("vendedores/edit.html", vendedor=vendedor)

        datos = {
            "nombre": nombre,
            "apellido": apellido,
            "usuario": usuario,
            "correo": correo,
            "rol": rol,
            "telefono": telefono
        }

        if password:
            datos["password"] = password

        resultado = actualizar(id, datos)

        if resultado["status"] == 200:
            flash("Vendedor actualizado exitosamente", "success")
            return redirect(url_for("vendedores.vendedores_list"))

        mensaje = resultado["datos"].get("message", "Error al actualizar el vendedor")
        flash(mensaje, "error")
        vendedor = {"id": id, "nombre": nombre, "apellido": apellido,
                    "usuario": usuario, "correo": correo,
                    "rol": rol, "telefono": telefono}
        return render_template("vendedores/edit.html", vendedor=vendedor)

    resultado = obtener_por_id(id)

    if resultado["status"] == 200:
        return render_template("vendedores/edit.html", vendedor=resultado["datos"])

    flash(resultado["datos"].get("message", "Vendedor no encontrado"), "error")
    return redirect(url_for("vendedores.vendedores_list"))


@vendedores_bp.route("/vendedores/eliminar/<int:id>")
def vendedores_delete(id):
    resultado = eliminar(id)

    if resultado["status"] == 200:
        flash("Vendedor eliminado exitosamente", "success")
    else:
        flash(resultado["datos"].get("message", "Error al eliminar el vendedor"), "error")

    return redirect(url_for("vendedores.vendedores_list"))

