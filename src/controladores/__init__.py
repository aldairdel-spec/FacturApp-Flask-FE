from controladores.cliente_controller import clientes_bp
from controladores.categoria_controller import categorias_bp
from controladores.producto_controller import productos_bp
from controladores.vendedor_controller import vendedores_bp
from controladores.factura_controller import facturas_bp
from controladores.detalle_factura_controller import detalle_factura_bp
from controladores.metodo_pago_controller import metodos_pago_bp


def registrar_controladores(app):
    """Registra todos los blueprints de controladores en la app Flask."""
    app.register_blueprint(clientes_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(vendedores_bp)
    app.register_blueprint(facturas_bp)
    app.register_blueprint(detalle_factura_bp)
    app.register_blueprint(metodos_pago_bp)
