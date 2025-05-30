from fastapi import FastAPI
from app.api.routes import product_routes, cliente_routes, pedido_routes, detalle_pedido_routes, pago_routes
import logging

logger = logging.getLogger(__name__)

try:
    app = FastAPI(title="E-commerce API")
    app.include_router(product_routes.router)
    app.include_router(cliente_routes.router)
    app.include_router(pedido_routes.router)
    app.include_router(detalle_pedido_routes.router)
    app.include_router(pago_routes.router) 
except Exception as e:
    logger.error(f"[main.py] Error al inicializar la aplicación o incluir rutas: {e}")