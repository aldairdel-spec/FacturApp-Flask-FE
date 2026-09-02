from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.apis.categoria_api import obtener_todas, obtener_por_id, crear, actualizar, eliminar

categorias_bp = Blueprint('categorias', __name__)


@categorias_bp.route("/categorias/")
def categorias_list():
    resultado = obtener_todas()

    if resultado["status"] == 200:
        return render_template("categorias/list.html", categorias=resultado["datos"])

    flash(resultado["datos"].get("message", "Error al obtener categorías"), "error")
    return render_template("categorias/list.html", categorias=[])


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

