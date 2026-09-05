from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.apis import factura_api, cliente_api, usuario_api
from src.apis import cerrar_sesion_por_401

facturas_bp = Blueprint('facturas', __name__)


def _obtener_clientes():
    resultado = cliente_api.obtener_todos()
    if resultado["status"] == 200:
        return resultado["datos"]
    return []


def _obtener_vendedores():
    resultado = usuario_api.obtener_todos()
    if resultado["status"] == 200:
        return resultado["datos"]
    return []


@facturas_bp.route('/facturas')
def facturas_list():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    resultado = factura_api.obtener_paginadas(page=page, per_page=per_page)

    if resultado["status"] == 401:
        return cerrar_sesion_por_401()

    if resultado["status"] != 200:
        message = "Error al obtener facturas"
        datos = resultado.get("datos")
        if isinstance(datos, dict):
            message = datos.get("message", message)
        flash(message, "error")
        return render_template("facturas/list.html", facturas=[], page=1, per_page=per_page,
                               total=0, total_pages=0, endpoint="facturas.facturas_list")

    facturas = resultado["datos"]

    clientes = _obtener_clientes()
    clientes_map = {c["id"]: c["nombre"] for c in clientes}

    vendedores = _obtener_vendedores()
    vendedores_map = {v["id"]: f"{v['nombre']} {v['apellido']}" for v in vendedores}

    for f in facturas:
        f["cliente_nombre"] = clientes_map.get(f["cliente_id"], "N/A")
        f["vendedor_nombre"] = vendedores_map.get(f["vendedor_id"], "N/A")

    return render_template("facturas/list.html", facturas=facturas,
                           page=resultado.get("page", page),
                           per_page=resultado.get("per_page", per_page),
                           total=resultado.get("total", 0),
                           total_pages=resultado.get("total_pages", 0),
                           endpoint="facturas.facturas_list")


@facturas_bp.route('/facturas/nuevo', methods=['GET', 'POST'])
def facturas_create():
    clientes = _obtener_clientes()
    vendedores = _obtener_vendedores()

    if request.method == 'POST':
        numero_factura = request.form.get("numero_factura", "").strip()
        cliente_id = request.form.get("cliente_id", "").strip()
        vendedor_id = request.form.get("vendedor_id", "").strip()
        subtotal_str = request.form.get("subtotal", "").strip()
        iva_str = request.form.get("iva", "").strip()
        total_str = request.form.get("total", "").strip()

        errores = []
        if not numero_factura:
            errores.append("El numero de factura es obligatorio")
        if not cliente_id:
            errores.append("Debe seleccionar un cliente")
        if not vendedor_id:
            errores.append("Debe seleccionar un vendedor")

        subtotal = 0.0
        iva = 0.0
        total = 0.0

        try:
            subtotal = float(subtotal_str) if subtotal_str else 0.0
        except ValueError:
            errores.append("El subtotal debe ser un numero valido")

        try:
            iva = float(iva_str) if iva_str else 0.0
        except ValueError:
            errores.append("El IVA debe ser un numero valido")

        try:
            total = float(total_str) if total_str else 0.0
        except ValueError:
            errores.append("El total debe ser un numero valido")

        if subtotal < 0:
            errores.append("El subtotal no puede ser negativo")
        if iva < 0:
            errores.append("El IVA no puede ser negativo")
        if total < 0:
            errores.append("El total no puede ser negativo")

        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("facturas/create.html", clientes=clientes, vendedores=vendedores)

        data = {
            "numero_factura": numero_factura,
            "cliente_id": int(cliente_id),
            "vendedor_id": int(vendedor_id),
            "subtotal": subtotal,
            "iva": iva,
            "total": total
        }

        status, response = factura_api.crear(data)
        if status == 201:
            flash("Factura creada exitosamente", "success")
            return redirect(url_for("facturas.facturas_list"))
        else:
            msg = response.get("message", "Error al crear la factura")
            flash(msg, "error")
            return render_template("facturas/create.html", clientes=clientes, vendedores=vendedores)

    return render_template("facturas/create.html", clientes=clientes, vendedores=vendedores)


@facturas_bp.route('/facturas/editar/<int:id>', methods=['GET', 'POST'])
def facturas_edit(id):
    factura = factura_api.obtener_por_id(id)
    if not factura:
        flash("Factura no encontrada", "error")
        return redirect(url_for("facturas.facturas_list"))

    clientes = _obtener_clientes()
    vendedores = _obtener_vendedores()

    if request.method == 'POST':
        numero_factura = request.form.get("numero_factura", "").strip()
        cliente_id = request.form.get("cliente_id", "").strip()
        vendedor_id = request.form.get("vendedor_id", "").strip()
        subtotal_str = request.form.get("subtotal", "").strip()
        iva_str = request.form.get("iva", "").strip()
        total_str = request.form.get("total", "").strip()

        errores = []
        if not numero_factura:
            errores.append("El numero de factura es obligatorio")
        if not cliente_id:
            errores.append("Debe seleccionar un cliente")
        if not vendedor_id:
            errores.append("Debe seleccionar un vendedor")

        subtotal = 0.0
        iva = 0.0
        total = 0.0

        try:
            subtotal = float(subtotal_str) if subtotal_str else 0.0
        except ValueError:
            errores.append("El subtotal debe ser un numero valido")

        try:
            iva = float(iva_str) if iva_str else 0.0
        except ValueError:
            errores.append("El IVA debe ser un numero valido")

        try:
            total = float(total_str) if total_str else 0.0
        except ValueError:
            errores.append("El total debe ser un numero valido")

        if subtotal < 0:
            errores.append("El subtotal no puede ser negativo")
        if iva < 0:
            errores.append("El IVA no puede ser negativo")
        if total < 0:
            errores.append("El total no puede ser negativo")

        if errores:
            for e in errores:
                flash(e, "error")
            factura["numero_factura"] = numero_factura
            factura["cliente_id"] = int(cliente_id) if cliente_id else factura["cliente_id"]
            factura["vendedor_id"] = int(vendedor_id) if vendedor_id else factura["vendedor_id"]
            factura["subtotal"] = subtotal
            factura["iva"] = iva
            factura["total"] = total
            return render_template("facturas/edit.html", factura=factura, clientes=clientes, vendedores=vendedores)

        data = {
            "numero_factura": numero_factura,
            "cliente_id": int(cliente_id),
            "vendedor_id": int(vendedor_id),
            "subtotal": subtotal,
            "iva": iva,
            "total": total
        }

        status, response = factura_api.actualizar(id, data)
        if status == 200:
            flash("Factura actualizada exitosamente", "success")
            return redirect(url_for("facturas.facturas_list"))
        else:
            msg = response.get("message", "Error al actualizar la factura")
            flash(msg, "error")
            factura["numero_factura"] = numero_factura
            factura["cliente_id"] = int(cliente_id) if cliente_id else factura["cliente_id"]
            factura["vendedor_id"] = int(vendedor_id) if vendedor_id else factura["vendedor_id"]
            factura["subtotal"] = subtotal
            factura["iva"] = iva
            factura["total"] = total
            return render_template("facturas/edit.html", factura=factura, clientes=clientes, vendedores=vendedores)

    return render_template("facturas/edit.html", factura=factura, clientes=clientes, vendedores=vendedores)


@facturas_bp.route('/facturas/eliminar/<int:id>')
def facturas_delete(id):
    status, response = factura_api.eliminar(id)
    if status == 200:
        flash("Factura eliminada exitosamente", "success")
    else:
        msg = response.get("message", "Error al eliminar la factura")
        flash(msg, "error")
    return redirect(url_for("facturas.facturas_list"))

