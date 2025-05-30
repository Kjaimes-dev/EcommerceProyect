from decimal import Decimal
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetodoPago(str, Enum):
    tarjeta = 'tarjeta'
    transferencia = 'transferencia'
    efectivo = 'efectivo'

@dataclass
class Pago:
    id_pago: int
    id_pedido: int
    monto: float
    fecha_pago: datetime
    metodo_pago: MetodoPago
    confirmado: bool

    def __post_init__(self):
        try:
            if not isinstance(self.id_pago, int) or self.id_pago < 0:
                logger.warning("[Pago] id_pago inválido: debe ser >= 0")
            if not isinstance(self.id_pedido, int) or self.id_pedido <= 0:
                logger.warning("[Pago] id_pedido inválido: debe ser > 0")
            if not isinstance(self.monto, (float, Decimal)) or self.monto <= 0:
                logger.warning(f"[Pago] monto inválido: {self.monto}")
            if not isinstance(self.fecha_pago, datetime):
                logger.warning("[Pago] fecha_pago no es una instancia de datetime")
            if isinstance(self.metodo_pago, str):
                try:
                    self.metodo_pago = MetodoPago(self.metodo_pago)
                except ValueError:
                    logger.warning(f"[Pago] metodo_pago no válido: {self.metodo_pago}")
            if not isinstance(self.metodo_pago, MetodoPago):
                logger.warning(f"[Pago] metodo_pago no válido: {self.metodo_pago}")
            # Validar el campo confirmado
            if isinstance(self.confirmado, int):
                self.confirmado = bool(self.confirmado)
            if not isinstance(self.confirmado, bool):
                logger.warning(f"[Pago] confirmado debe ser booleano: {self.confirmado}")
            else:
                logger.info(f"[Pago] Validación exitosa: {self}")
        except Exception as e:
            logger.error(f"[Pago] Error en validación inicial: {e}")