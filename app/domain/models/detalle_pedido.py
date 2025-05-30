from dataclasses import dataclass, field
from decimal import Decimal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



@dataclass
class DetallePedido:
    id_detalle: int
    id_pedido: int
    id_producto: int
    cantidad: int
    precio_unitario: float

    def __post_init__(self):
        try:
            if not isinstance(self.id_detalle, int) or self.id_detalle < 0:
                logger.warning(f"[DetallePedido] id_detalle inválido: {self.id_detalle}")
            if not isinstance(self.id_pedido, int) or self.id_pedido <= 0:
                logger.warning(f"[DetallePedido] id_pedido inválido: {self.id_pedido}")
            if not isinstance(self.id_producto, int) or self.id_producto <= 0:
                logger.warning(f"[DetallePedido] id_producto inválido: {self.id_producto}")
            if not isinstance(self.cantidad, int) or self.cantidad <= 0:
                logger.warning(f"[DetallePedido] cantidad inválida: {self.cantidad}")
            if not isinstance(self.precio_unitario, (float, Decimal)) or self.precio_unitario <= 0:
                logger.warning(f"[DetallePedido] precio_unitario inválido: {self.precio_unitario}")
            else:
                logger.info(f"[DetallePedido] precio_unitario válido: {self.precio_unitario}")
        except Exception as e:
            logger.error(f"[DetallePedido] Error en __post_init__: {e}")