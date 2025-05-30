from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EstadoPedido(str, Enum):
    pendiente = 'pendiente'
    enviado = 'enviado'
    entregado = 'entregado'
    cancelado = 'cancelado'

@dataclass
class Pedido:
    id_pedido: int
    id_cliente: int
    fecha: datetime
    estado: EstadoPedido

    def __post_init__(self):
        try:
            if not isinstance(self.id_pedido, int) or self.id_pedido <= 0:
                logger.warning(f"[Pedido] id_pedido inválido: {self.id_pedido}")
            if not isinstance(self.id_cliente, int) or self.id_cliente <= 0:
                logger.warning(f"[Pedido] id_cliente inválido: {self.id_cliente}")
            if not isinstance(self.fecha, datetime):
                logger.warning(f"[Pedido] fecha inválida: {self.fecha}")
            if isinstance(self.estado, str):
                self.estado = EstadoPedido(self.estado)
            if not isinstance(self.estado, EstadoPedido):
                logger.warning(f"[Pedido] estado inválido: {self.estado}")
        except Exception as e:
            logger.error(f"[Pedido] Error en __post_init__: {e}")