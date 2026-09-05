from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.apis.categoria_api import obtener_todas, obtener_paginado, obtener_por_id, crear, actualizar, eliminar
from src.apis import cerrar_sesion_por_401

categorias_bp = Blueprint('categorias', __name__)


@categorias_bp.route("/categorias/")
def categorias_list():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    resultado = obtener_paginado(page=page, per_page=per_page)

    if resultado["status"] == 200:
        return render_template("categorias/list.html",
                               categorias=resultado["datos"],
                               page=resultado.get("page", page),
                               per_page=resultado.get("per_page", per_page),
                               total=resultado.get("total", 0),
                               total_pages=resultado.get("total_pages", 0),
                               endpoint="categorias.categorias_list")

    if resultado["status"] == 401:
        return cerrar_sesion_por_401()

    flash(resultado["datos"].get("message", "Error al obtener categorías"), "error")
    return render_template("categorias/list.html", categorias=[], page=1, per_page=per_page,
                           total=0, total_pages=0, endpoint="categorias.categorias_list")


@categorias_bp.route("/categorias/nueva", methods=["GET", "POST"])
def categorias_create():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()

        if not nombre:
            flash("El nombre es obligatorio", "error")
            return render_template("categorias/create.html", nombre=nombre)

        datos = {"nombre": nombre}

        resultado = crear(datos)

        if resultado["status"] == 201:
            flash("Categoría creada exitosamente", "success")
            return redirect(url_for("categorias.categorias_list"))

        mensaje = resultado["datos"].get("message", "Error al crear la categoría")
        flash(mensaje, "error")
        return render_template("categorias/create.html", nombre=nombre)

    return render_template("categorias/create.html", nombre="")


@categorias_bp.route("/categorias/editar/<int:id>", methods=["GET", "POST"])
def categorias_edit(id):
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()

        if not nombre:
            flash("El nombre es obligatorio", "error")
            categoria = {"id": id, "nombre": nombre}
            return render_template("categorias/edit.html", categoria=categoria)

        datos = {"nombre": nombre}

        resultado = actualizar(id, datos)

        if resultado["status"] == 200:
            flash("Categoría actualizada exitosamente", "success")
            return redirect(url_for("categorias.categorias_list"))

        mensaje = resultado["datos"].get("message", "Error al actualizar la categoría")
        flash(mensaje, "error")
        categoria = {"id": id, "nombre": nombre}
        return render_template("categorias/edit.html", categoria=categoria)

    resultado = obtener_por_id(id)

    if resultado["status"] == 200:
        return render_template("categorias/edit.html", categoria=resultado["datos"])

    flash(resultado["datos"].get("message", "Categoría no encontrada"), "error")
    return redirect(url_for("categorias.categorias_list"))


@categorias_bp.route("/categorias/eliminar/<int:id>")
def categorias_delete(id):
    resultado = eliminar(id)

    if resultado["status"] == 200:
        flash("Categoría eliminada exitosamente", "success")
    else:
        flash(resultado["datos"].get("message", "Error al eliminar la categoría"), "error")

    return redirect(url_for("categorias.categorias_list"))

