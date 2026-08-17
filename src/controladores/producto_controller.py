from flask import Blueprint, render_template, request, redirect, url_for, flash
from apis.producto_api import obtener_todos, obtener_por_id, crear, actualizar, eliminar
from apis.categoria_api import obtener_todas

productos_bp = Blueprint('productos', __name__)


@productos_bp.route("/productos")
def productos_list():
    resultado = obtener_todos()
    res_categorias = obtener_todas()

    categorias = []
    if res_categorias["status"] == 200:
        categorias = res_categorias["datos"]

    mapa_categorias = {c["id"]: c["nombre"] for c in categorias}

    if resultado["status"] == 200:
        for p in resultado["datos"]:
            p["categoria_nombre"] = mapa_categorias.get(p["id_categoria"], "Sin categoría")
        return render_template("productos/list.html", productos=resultado["datos"])

    flash(resultado["datos"].get("message", "Error al obtener productos"), "error")
    return render_template("productos/list.html", productos=[])


@productos_bp.route("/productos/nuevo", methods=["GET", "POST"])
def productos_create():
    res_categorias = obtener_todas()
    categorias = []
    if res_categorias["status"] == 200:
        categorias = res_categorias["datos"]

    if request.method == "POST":
        codigo = request.form.get("codigo", "").strip()
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        unidad_medida = request.form.get("unidad_medida", "").strip()
        precio_str = request.form.get("precio", "").strip()
        stock_str = request.form.get("stock", "").strip()
        id_categoria_str = request.form.get("id_categoria", "").strip()

        errores = []
        if not codigo:
            errores.append("El código es obligatorio")
        if not nombre:
            errores.append("El nombre es obligatorio")
        if not descripcion:
            errores.append("La descripción es obligatoria")
        if not unidad_medida:
            errores.append("La unidad de medida es obligatoria")
        if not id_categoria_str:
            errores.append("La categoría es obligatoria")

        precio = 0.0
        if not precio_str:
            errores.append("El precio es obligatorio")
        else:
            try:
                precio = float(precio_str)
                if precio <= 0:
                    errores.append("El precio debe ser mayor a cero")
            except ValueError:
                errores.append("El precio debe ser un número válido")

        stock = 0
        if not stock_str:
            errores.append("El stock es obligatorio")
        else:
            try:
                stock = int(stock_str)
                if stock < 0:
                    errores.append("El stock no puede ser negativo")
            except ValueError:
                errores.append("El stock debe ser un número entero")

        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("productos/create.html",
                                   categorias=categorias,
                                   codigo=codigo, nombre=nombre,
                                   descripcion=descripcion, unidad_medida=unidad_medida,
                                   precio=precio_str, stock=stock_str,
                                   id_categoria=id_categoria_str)

        id_categoria = int(id_categoria_str)

        datos = {
            "codigo": codigo,
            "nombre": nombre,
            "descripcion": descripcion,
            "unidad_medida": unidad_medida,
            "precio": precio,
            "stock": stock,
            "id_categoria": id_categoria
        }

        resultado = crear(datos)

        if resultado["status"] == 201:
            flash("Producto creado exitosamente", "success")
            return redirect(url_for("productos.productos_list"))

        mensaje = resultado["datos"].get("message", "Error al crear el producto")
        flash(mensaje, "error")
        return render_template("productos/create.html",
                               categorias=categorias,
                               codigo=codigo, nombre=nombre,
                               descripcion=descripcion, unidad_medida=unidad_medida,
                               precio=precio_str, stock=stock_str,
                               id_categoria=id_categoria_str)

    return render_template("productos/create.html",
                           categorias=categorias,
                           codigo="", nombre="",
                           descripcion="", unidad_medida="",
                           precio="", stock="",
                           id_categoria="")


@productos_bp.route("/productos/editar/<int:id>", methods=["GET", "POST"])
def productos_edit(id):
    res_categorias = obtener_todas()
    categorias = []
    if res_categorias["status"] == 200:
        categorias = res_categorias["datos"]

    if request.method == "POST":
        codigo = request.form.get("codigo", "").strip()
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        unidad_medida = request.form.get("unidad_medida", "").strip()
        precio_str = request.form.get("precio", "").strip()
        stock_str = request.form.get("stock", "").strip()
        id_categoria_str = request.form.get("id_categoria", "").strip()

        errores = []
        if not codigo:
            errores.append("El código es obligatorio")
        if not nombre:
            errores.append("El nombre es obligatorio")
        if not descripcion:
            errores.append("La descripción es obligatoria")
        if not unidad_medida:
            errores.append("La unidad de medida es obligatoria")
        if not id_categoria_str:
            errores.append("La categoría es obligatoria")

        precio = 0.0
        if not precio_str:
            errores.append("El precio es obligatorio")
        else:
            try:
                precio = float(precio_str)
                if precio <= 0:
                    errores.append("El precio debe ser mayor a cero")
            except ValueError:
                errores.append("El precio debe ser un número válido")

        stock = 0
        if not stock_str:
            errores.append("El stock es obligatorio")
        else:
            try:
                stock = int(stock_str)
                if stock < 0:
                    errores.append("El stock no puede ser negativo")
            except ValueError:
                errores.append("El stock debe ser un número entero")

        if errores:
            for e in errores:
                flash(e, "error")
            producto = {"id": id, "codigo": codigo, "nombre": nombre,
                        "descripcion": descripcion, "unidad_medida": unidad_medida,
                        "precio": precio, "stock": stock,
                        "id_categoria": int(id_categoria_str) if id_categoria_str else None}
            return render_template("productos/edit.html", producto=producto, categorias=categorias)

        datos = {
            "codigo": codigo,
            "nombre": nombre,
            "descripcion": descripcion,
            "unidad_medida": unidad_medida,
            "precio": precio,
            "stock": stock,
            "id_categoria": int(id_categoria_str)
        }

        resultado = actualizar(id, datos)

        if resultado["status"] == 200:
            flash("Producto actualizado exitosamente", "success")
            return redirect(url_for("productos.productos_list"))

        mensaje = resultado["datos"].get("message", "Error al actualizar el producto")
        flash(mensaje, "error")
        producto = {"id": id, "codigo": codigo, "nombre": nombre,
                    "descripcion": descripcion, "unidad_medida": unidad_medida,
                    "precio": precio, "stock": stock,
                    "id_categoria": int(id_categoria_str) if id_categoria_str else None}
        return render_template("productos/edit.html", producto=producto, categorias=categorias)

    resultado = obtener_por_id(id)

    if resultado["status"] == 200:
        return render_template("productos/edit.html", producto=resultado["datos"], categorias=categorias)

    flash(resultado["datos"].get("message", "Producto no encontrado"), "error")
    return redirect(url_for("productos.productos_list"))


@productos_bp.route("/productos/eliminar/<int:id>")
def productos_delete(id):
    resultado = eliminar(id)

    if resultado["status"] == 200:
        flash("Producto eliminado exitosamente", "success")
    else:
        flash(resultado["datos"].get("message", "Error al eliminar el producto"), "error")

    return redirect(url_for("productos.productos_list"))
