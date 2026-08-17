from flask import Blueprint, render_template, request, redirect, url_for, flash
from apis.metodo_pago_api import obtener_todos, obtener_por_id, crear, actualizar, eliminar

metodos_pago_bp = Blueprint('metodos_pago', __name__)


@metodos_pago_bp.route('/metodos_pago')
def metodos_pago_list():
    resultado = obtener_todos()

    if resultado["status"] == 200:
        return render_template("metodos_pago/list.html", metodos_pago=resultado["datos"])

    flash(resultado["datos"].get("message", "Error al obtener metodos de pago"), "error")
    return render_template("metodos_pago/list.html", metodos_pago=[])


@metodos_pago_bp.route('/metodos_pago/nuevo', methods=['GET', 'POST'])
def metodos_pago_create():
    if request.method == 'POST':
        nombre = request.form.get("nombre", "").strip()

        if not nombre:
            flash("El nombre del metodo de pago es obligatorio", "error")
            return render_template("metodos_pago/create.html", nombre=nombre)

        datos = {"nombre": nombre}

        resultado = crear(datos)

        if resultado["status"] == 201:
            flash("Metodo de pago creado exitosamente", "success")
            return redirect(url_for("metodos_pago.metodos_pago_list"))

        mensaje = resultado["datos"].get("message", "Error al crear el metodo de pago")
        flash(mensaje, "error")
        return render_template("metodos_pago/create.html", nombre=nombre)

    return render_template("metodos_pago/create.html", nombre="")


@metodos_pago_bp.route('/metodos_pago/editar/<int:id>', methods=['GET', 'POST'])
def metodos_pago_edit(id):
    if request.method == 'POST':
        nombre = request.form.get("nombre", "").strip()

        if not nombre:
            flash("El nombre del metodo de pago es obligatorio", "error")
            metodo = {"id": id, "nombre": nombre}
            return render_template("metodos_pago/edit.html", metodo=metodo)

        datos = {"nombre": nombre}

        resultado = actualizar(id, datos)

        if resultado["status"] == 200:
            flash("Metodo de pago actualizado exitosamente", "success")
            return redirect(url_for("metodos_pago.metodos_pago_list"))

        mensaje = resultado["datos"].get("message", "Error al actualizar el metodo de pago")
        flash(mensaje, "error")
        metodo = {"id": id, "nombre": nombre}
        return render_template("metodos_pago/edit.html", metodo=metodo)

    resultado = obtener_por_id(id)

    if resultado["status"] == 200:
        return render_template("metodos_pago/edit.html", metodo=resultado["datos"])

    flash(resultado["datos"].get("message", "Metodo de pago no encontrado"), "error")
    return redirect(url_for("metodos_pago.metodos_pago_list"))


@metodos_pago_bp.route('/metodos_pago/eliminar/<int:id>')
def metodos_pago_delete(id):
    resultado = eliminar(id)

    if resultado["status"] == 200:
        flash("Metodo de pago eliminado exitosamente", "success")
    else:
        flash(resultado["datos"].get("message", "Error al eliminar el metodo de pago"), "error")

    return redirect(url_for("metodos_pago.metodos_pago_list"))
