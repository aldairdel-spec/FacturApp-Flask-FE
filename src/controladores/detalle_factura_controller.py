from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.apis.detalle_factura_api import obtener_todos, obtener_por_id, crear, actualizar, eliminar
from src.apis import factura_api
from src.apis import producto_api

detalle_factura_bp = Blueprint('detalle_factura', __name__)


def _obtener_facturas():
    return factura_api.obtener_todas()


def _obtener_productos():
    resultado = producto_api.obtener_todos()
    if resultado["status"] == 200:
        return resultado["datos"]
    return []


@detalle_factura_bp.route('/detalle_factura')
def detalle_factura_list():
    resultado = obtener_todos()

    if resultado["status"] != 200:
        flash(resultado["datos"].get("message", "Error al obtener detalles"), "error")
        return render_template("detalle_factura/list.html", detalles=[])

    detalles = resultado["datos"]

    facturas = _obtener_facturas()
    facturas_map = {f["id"]: f["numero_factura"] for f in facturas}

    productos = _obtener_productos()
    productos_map = {p["id"]: p["nombre"] for p in productos}

    for d in detalles:
        d["factura_numero"] = facturas_map.get(d["factura_id"], "N/A")
        d["producto_nombre"] = productos_map.get(d["producto_id"], "N/A")

    return render_template("detalle_factura/list.html", detalles=detalles)


@detalle_factura_bp.route('/detalle_factura/nuevo', methods=['GET', 'POST'])
def detalle_factura_create():
    facturas = _obtener_facturas()
    productos = _obtener_productos()

    if request.method == 'POST':
        factura_id = request.form.get("factura_id", "").strip()
        producto_id = request.form.get("producto_id", "").strip()
        cantidad_str = request.form.get("cantidad", "").strip()
        precio_unitario_str = request.form.get("precio_unitario", "").strip()

        errores = []
        if not factura_id:
            errores.append("Debe seleccionar una factura")
        if not producto_id:
            errores.append("Debe seleccionar un producto")

        cantidad = 0
        precio_unitario = 0.0

        try:
            cantidad = int(cantidad_str) if cantidad_str else 0
        except ValueError:
            errores.append("La cantidad debe ser un numero valido")

        try:
            precio_unitario = float(precio_unitario_str) if precio_unitario_str else 0.0
        except ValueError:
            errores.append("El precio unitario debe ser un numero valido")

        if cantidad <= 0:
            errores.append("La cantidad debe ser mayor que cero")
        if precio_unitario < 0:
            errores.append("El precio unitario no puede ser negativo")

        subtotal = cantidad * precio_unitario

        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("detalle_factura/create.html",
                                   facturas=facturas, productos=productos)

        datos = {
            "factura_id": int(factura_id),
            "producto_id": int(producto_id),
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "subtotal": subtotal
        }

        resultado = crear(datos)

        if resultado["status"] == 201:
            flash("Detalle de factura creado exitosamente", "success")
            return redirect(url_for("detalle_factura.detalle_factura_list"))

        mensaje = resultado["datos"].get("message", "Error al crear el detalle")
        flash(mensaje, "error")
        return render_template("detalle_factura/create.html",
                               facturas=facturas, productos=productos)

    return render_template("detalle_factura/create.html",
                           facturas=facturas, productos=productos)


@detalle_factura_bp.route('/detalle_factura/editar/<int:id>', methods=['GET', 'POST'])
def detalle_factura_edit(id):
    resultado = obtener_por_id(id)

    if resultado["status"] != 200:
        flash(resultado["datos"].get("message", "Detalle no encontrado"), "error")
        return redirect(url_for("detalle_factura.detalle_factura_list"))

    detalle = resultado["datos"]
    facturas = _obtener_facturas()
    productos = _obtener_productos()

    if request.method == 'POST':
        factura_id = request.form.get("factura_id", "").strip()
        producto_id = request.form.get("producto_id", "").strip()
        cantidad_str = request.form.get("cantidad", "").strip()
        precio_unitario_str = request.form.get("precio_unitario", "").strip()

        errores = []
        if not factura_id:
            errores.append("Debe seleccionar una factura")
        if not producto_id:
            errores.append("Debe seleccionar un producto")

        cantidad = 0
        precio_unitario = 0.0

        try:
            cantidad = int(cantidad_str) if cantidad_str else 0
        except ValueError:
            errores.append("La cantidad debe ser un numero valido")

        try:
            precio_unitario = float(precio_unitario_str) if precio_unitario_str else 0.0
        except ValueError:
            errores.append("El precio unitario debe ser un numero valido")

        if cantidad <= 0:
            errores.append("La cantidad debe ser mayor que cero")
        if precio_unitario < 0:
            errores.append("El precio unitario no puede ser negativo")

        subtotal = cantidad * precio_unitario

        if errores:
            for e in errores:
                flash(e, "error")
            detalle["factura_id"] = int(factura_id) if factura_id else detalle["factura_id"]
            detalle["producto_id"] = int(producto_id) if producto_id else detalle["producto_id"]
            detalle["cantidad"] = cantidad
            detalle["precio_unitario"] = precio_unitario
            detalle["subtotal"] = subtotal
            return render_template("detalle_factura/edit.html",
                                   detalle=detalle, facturas=facturas, productos=productos)

        datos = {
            "factura_id": int(factura_id),
            "producto_id": int(producto_id),
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "subtotal": subtotal
        }

        resultado_update = actualizar(id, datos)

        if resultado_update["status"] == 200:
            flash("Detalle de factura actualizado exitosamente", "success")
            return redirect(url_for("detalle_factura.detalle_factura_list"))

        mensaje = resultado_update["datos"].get("message", "Error al actualizar el detalle")
        flash(mensaje, "error")
        detalle["factura_id"] = int(factura_id) if factura_id else detalle["factura_id"]
        detalle["producto_id"] = int(producto_id) if producto_id else detalle["producto_id"]
        detalle["cantidad"] = cantidad
        detalle["precio_unitario"] = precio_unitario
        detalle["subtotal"] = subtotal
        return render_template("detalle_factura/edit.html",
                               detalle=detalle, facturas=facturas, productos=productos)

    return render_template("detalle_factura/edit.html",
                           detalle=detalle, facturas=facturas, productos=productos)


@detalle_factura_bp.route('/detalle_factura/eliminar/<int:id>')
def detalle_factura_delete(id):
    resultado = eliminar(id)

    if resultado["status"] == 200:
        flash("Detalle de factura eliminado exitosamente", "success")
    else:
        flash(resultado["datos"].get("message", "Error al eliminar el detalle"), "error")

    return redirect(url_for("detalle_factura.detalle_factura_list"))

