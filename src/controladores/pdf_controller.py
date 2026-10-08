import os
from datetime import datetime

from flask import Blueprint, flash, redirect, send_file, url_for

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from src.apis import (
    cliente_api,
    detalle_factura_api,
    factura_api,
    metodo_pago_api,
    producto_api,
    usuario_api,
)

pdf_bp = Blueprint('pdf', __name__)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PDF_DIR = os.path.join(PROJECT_ROOT, "facturas_pdf")

COLOR_PRIMARY = colors.HexColor("#2563eb")
COLOR_PRIMARY_DARK = colors.HexColor("#1e293b")
COLOR_LIGHT = colors.HexColor("#f1f5f9")
COLOR_STRIPE = colors.HexColor("#f8faff")
COLOR_BORDER = colors.HexColor("#e2e8f0")


def _txt(valor):
    """Convierte a texto seguro para el PDF (latin-1)."""
    if valor is None:
        return ""
    texto = str(valor).strip()
    try:
        texto.encode("latin-1")
        return texto
    except UnicodeEncodeError:
        return texto.encode("latin-1", "replace").decode("latin-1")


def _dinero(valor):
    try:
        return "S/ " + format(float(valor), ",.2f").replace(",", " ")
    except (TypeError, ValueError):
        return "S/ 0.00"


def _lista(datos):
    """Normaliza la respuesta del backend a una lista."""
    if isinstance(datos, list):
        return datos
    if isinstance(datos, dict):
        inner = datos.get("datos")
        if isinstance(inner, list):
            return inner
    return []


def _fecha_legible(fecha):
    """Convierte una fecha del backend a formato DD/MM/YYYY si es posible."""
    if not fecha:
        return ""
    texto = str(fecha)
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(texto[:19], fmt).strftime("%d/%m/%Y")
        except ValueError:
            continue
    return texto


def _guardar_y_enviar(factura, detalles, cliente, vendedor, metodo_pago_nombre):
    """Construye el PDF de la factura, lo guarda en facturas_pdf/ y lo devuelve."""
    if not os.path.isdir(PDF_DIR):
        os.makedirs(PDF_DIR, exist_ok=True)

    numero_factura = _txt(factura.get("numero_factura") or "")
    factura_id = str(factura.get("id") or "")
    filename = f"Factura_{factura_id:0>4}.pdf"
    pdf_path = os.path.join(PDF_DIR, filename)

    ancho = A4[0] - 36 * mm
    estilos = getSampleStyleSheet()

    st_titulo = ParagraphStyle("titulo", parent=estilos["Normal"], fontName="Helvetica-Bold",
                               fontSize=16, leading=19, textColor=colors.white, alignment=1)
    st_marca = ParagraphStyle("marca", parent=estilos["Normal"], fontName="Helvetica-Bold",
                              fontSize=15, leading=18, textColor=colors.white)
    st_etiqueta = ParagraphStyle("etiqueta", parent=estilos["Normal"], fontName="Helvetica-Bold",
                                 fontSize=8.5, leading=11, textColor=colors.HexColor("#64748b"))
    st_valor = ParagraphStyle("valor", parent=estilos["Normal"], fontName="Helvetica",
                              fontSize=10.5, leading=14, textColor=colors.HexColor("#1e293b"))
    st_seccion = ParagraphStyle("seccion", parent=estilos["Normal"], fontName="Helvetica-Bold",
                                fontSize=10, leading=13, textColor=COLOR_PRIMARY_DARK)
    st_cab = ParagraphStyle("cab", parent=estilos["Normal"], fontName="Helvetica-Bold",
                            fontSize=9, leading=12, textColor=colors.white)
    st_cel = ParagraphStyle("cel", parent=estilos["Normal"], fontName="Helvetica",
                            fontSize=9, leading=12, textColor=colors.HexColor("#1e293b"))
    st_total = ParagraphStyle("total", parent=estilos["Normal"], fontName="Helvetica-Bold",
                              fontSize=13, leading=16, textColor=colors.white)
    st_pie = ParagraphStyle("pie", parent=estilos["Normal"], fontName="Helvetica-Oblique",
                            fontSize=9.5, leading=12, textColor=colors.HexColor("#64748b"), alignment=1)

    def barra_seccion(texto):
        tabla = Table([[Paragraph(texto, st_seccion)]], colWidths=[ancho])
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), COLOR_LIGHT),
            ("LINEBELOW", (0, 0), (-1, -1), 0.75, COLOR_BORDER),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        return tabla

    story = []

    # Encabezado con la marca FacturAPP
    encabezado = Table(
        [[Paragraph("FACTURAPP", st_marca), Paragraph("FACTURA DE VENTA", st_titulo)]],
        colWidths=[ancho * 0.55, ancho * 0.45],
    )
    encabezado.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), COLOR_PRIMARY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(encabezado)
    story.append(Spacer(1, 8 * mm))

    # Metadatos de la factura
    fecha_emision = _fecha_legible(factura.get("fecha")) or "-"
    filas_meta = [
        [Paragraph("NUMERO DE FACTURA", st_etiqueta), Paragraph("FECHA DE EMISION", st_etiqueta)],
        [Paragraph(numero_factura or "-", st_valor), Paragraph(fecha_emision, st_valor)],
    ]
    if vendedor:
        filas_meta.append([Paragraph("VENDEDOR", st_etiqueta), Paragraph(vendedor, st_valor)])
    meta = Table(filas_meta, colWidths=[ancho * 0.5, ancho * 0.5])
    meta.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    story.append(meta)
    story.append(Spacer(1, 5 * mm))

    # Cliente
    cliente_nombre = _txt(cliente.get("nombre")) if cliente else "---"
    cliente_doc = _txt(cliente.get("documento")) if cliente else "---"
    filas_cliente = [[Paragraph("CLIENTE", st_seccion), ""]]
    filas_cliente.append([Paragraph("Nombre:", st_etiqueta), Paragraph(cliente_nombre, st_valor)])
    filas_cliente.append([Paragraph("Identificacion:", st_etiqueta), Paragraph(cliente_doc, st_valor)])
    if cliente:
        contacto = " / ".join(x for x in [_txt(cliente.get("email")), _txt(cliente.get("telefono"))] if x)
        if contacto:
            filas_cliente.append([Paragraph("Contacto:", st_etiqueta), Paragraph(contacto, st_valor)])
        if cliente.get("direccion"):
            filas_cliente.append([Paragraph("Direccion:", st_etiqueta), Paragraph(_txt(cliente.get("direccion")), st_valor)])
    tabla_cliente = Table(filas_cliente, colWidths=[ancho * 0.3, ancho * 0.7])
    tabla_cliente.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), COLOR_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.75, COLOR_BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, COLOR_BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(tabla_cliente)
    story.append(Spacer(1, 6 * mm))

    # Detalle de productos
    story.append(barra_seccion("DETALLE DE PRODUCTOS"))
    story.append(Spacer(1, 3 * mm))
    datos_tabla = [[
        Paragraph("CODIGO", st_cab),
        Paragraph("PRODUCTO", st_cab),
        Paragraph("CANTIDAD", st_cab),
        Paragraph("PRECIO", st_cab),
        Paragraph("SUBTOTAL", st_cab),
    ]]
    for d in detalles:
        cantidad = int(d.get("cantidad") or 0)
        precio = d.get("precio_unitario") or 0.0
        subtotal = d.get("subtotal")
        try:
            subtotal = float(subtotal) if subtotal is not None else float(cantidad) * float(precio)
        except (TypeError, ValueError):
            subtotal = 0.0
        datos_tabla.append([
            Paragraph(_txt(d.get("producto_codigo") or ""), st_cel),
            Paragraph(_txt(d.get("producto_nombre") or f"Producto {d.get('producto_id')}"), st_cel),
            Paragraph(str(cantidad), st_cel),
            Paragraph(_dinero(precio), st_cel),
            Paragraph(_dinero(subtotal), st_cel),
        ])
    if len(datos_tabla) == 1:
        datos_tabla.append([Paragraph("-", st_cel), Paragraph("Sin productos asociados", st_cel),
                            Paragraph("-", st_cel), Paragraph("-", st_cel), Paragraph("-", st_cel)])
    tabla_productos = Table(datos_tabla, colWidths=[ancho * 0.12, ancho * 0.38, ancho * 0.14, ancho * 0.18, ancho * 0.18])
    estilo_tabla = [
        ("BACKGROUND", (0, 0), (-1, 0), COLOR_PRIMARY_DARK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, COLOR_BORDER),
        ("BOX", (0, 0), (-1, -1), 0.75, COLOR_BORDER),
        ("ALIGN", (1, 0), (-1, -1), "LEFT"),
        ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
        ("ALIGN", (3, 0), (-1, -1), "RIGHT"),
        ("ALIGN", (4, 0), (-1, -1), "RIGHT"),
    ]
    for fila in range(1, len(datos_tabla)):
        if fila % 2 == 0:
            estilo_tabla.append(("BACKGROUND", (0, fila), (-1, fila), COLOR_STRIPE))
    tabla_productos.setStyle(TableStyle(estilo_tabla))
    story.append(tabla_productos)
    story.append(Spacer(1, 6 * mm))

    # Totales
    filas_totales = [
        [Paragraph("Subtotal:", st_valor), Paragraph(_dinero(factura.get("subtotal")), st_valor)],
    ]
    iva = factura.get("iva")
    if iva not in (None, 0, 0.0, "0", "0.00"):
        filas_totales.append([Paragraph("IVA (19%):", st_valor), Paragraph(_dinero(iva), st_valor)])
    total = factura.get("total") if factura.get("total") is not None else 0.0
    filas_totales.append([Paragraph("TOTAL:", st_total), Paragraph(_dinero(total), st_total)])
    tabla_totales = Table(filas_totales, colWidths=[ancho * 0.25, ancho * 0.25])
    tabla_totales.setStyle(TableStyle([
        ("BACKGROUND", (0, -1), (-1, -1), COLOR_PRIMARY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("BOX", (0, 0), (-1, -1), 0.75, COLOR_BORDER),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
    ]))
    alineacion = Table([[tabla_totales]], colWidths=[ancho])
    alineacion.setStyle(TableStyle([("ALIGN", (0, 0), (0, 0), "RIGHT"),
                                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                    ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    story.append(alineacion)

    if metodo_pago_nombre:
        story.append(Spacer(1, 3 * mm))
        fila_pago = Table(
            [[Paragraph("Metodo de pago:", st_etiqueta), Paragraph(_txt(metodo_pago_nombre), st_valor)]],
            colWidths=[ancho * 0.3, ancho * 0.7],
        )
        fila_pago.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 2),
            ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ]))
        story.append(fila_pago)

    story.append(Spacer(1, 10 * mm))
    pie = Table([[Paragraph("Gracias por su compra", st_pie)]], colWidths=[ancho])
    pie.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(pie)

    SimpleDocTemplate(pdf_path, pagesize=A4,
                      leftMargin=18 * mm, rightMargin=18 * mm,
                      topMargin=14 * mm, bottomMargin=16 * mm).build(story)
    return filename, pdf_path


@pdf_bp.route('/facturas/pdf/<int:id>')
def facturas_pdf(id):
    """Genera, guarda y descarga el PDF de una factura real."""
    try:
        factura = factura_api.obtener_por_id(id)
    except Exception:
        factura = None

    if not factura:
        flash("Factura no encontrada", "error")
        return redirect(url_for("facturas.facturas_list"))

    cliente = None
    resultado_cliente = cliente_api.obtener_por_id(factura.get("cliente_id"))
    if resultado_cliente["status"] == 200:
        cliente = resultado_cliente["datos"]

    vendedor_nombre = None
    resultado_usuarios = usuario_api.obtener_todos()
    if resultado_usuarios["status"] == 200:
        for u in _lista(resultado_usuarios["datos"]):
            if str(u.get("id")) == str(factura.get("vendedor_id")):
                vendedor_nombre = f"{u.get('nombre', '')} {u.get('apellido', '')}".strip()
                break

    detalles = []
    resultado_detalles = detalle_factura_api.obtener_todos()
    if resultado_detalles["status"] == 200:
        lista = _lista(resultado_detalles["datos"])
        detalles = [d for d in lista if str(d.get("factura_id")) == str(id)]

    productos_map = {}
    resultado_productos = producto_api.obtener_todos()
    if resultado_productos["status"] == 200:
        for p in _lista(resultado_productos["datos"]):
            productos_map[str(p.get("id"))] = p

    for d in detalles:
        producto = productos_map.get(str(d.get("producto_id")), {})
        d["producto_nombre"] = producto.get("nombre")
        d["producto_codigo"] = producto.get("codigo")

    metodo_pago_nombre = None
    for clave in ("metodo_pago_id", "id_metodo_pago", "metodo_pago"):
        if factura.get(clave):
            resultado_metodos = metodo_pago_api.obtener_todos()
            if resultado_metodos["status"] == 200:
                for m in _lista(resultado_metodos["datos"]):
                    if str(m.get("id")) == str(factura.get(clave)):
                        metodo_pago_nombre = m.get("nombre")
                        break
            if metodo_pago_nombre:
                break

    try:
        filename, pdf_path = _guardar_y_enviar(
            factura, detalles, cliente, vendedor_nombre, metodo_pago_nombre
        )
    except Exception as e:
        flash(f"Error al generar el PDF: {str(e)}", "error")
        return redirect(url_for("facturas.facturas_list"))

    flash("PDF generado correctamente", "success")
    return send_file(pdf_path, as_attachment=True, download_name=filename)