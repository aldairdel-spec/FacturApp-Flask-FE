from src.controladores.cliente_controller import clientes_bp
from src.controladores.categoria_controller import categorias_bp
from src.controladores.producto_controller import productos_bp
from src.controladores.vendedor_controller import vendedores_bp
from src.controladores.factura_controller import facturas_bp
from src.controladores.detalle_factura_controller import detalle_factura_bp
from src.controladores.metodo_pago_controller import metodos_pago_bp
from src.controladores.pdf_controller import pdf_bp


def registrar_controladores(app):
    """Registra todos los blueprints de controladores en la app Flask."""
    app.register_blueprint(clientes_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(vendedores_bp)
    app.register_blueprint(facturas_bp)
    app.register_blueprint(detalle_factura_bp)
    app.register_blueprint(metodos_pago_bp)
    app.register_blueprint(pdf_bp)

