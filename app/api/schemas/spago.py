# app/api/schemas/spago.py
from pydantic import BaseModel, condecimal, field_validator
from datetime import datetime
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetodoPago(str, Enum):
    tarjeta = 'tarjeta'
    transferencia = 'transferencia'
    efectivo = 'efectivo'

class PagoBaseSchema(BaseModel):
    id_pedido: int
    monto: condecimal(gt=0, max_digits=10, decimal_places=2)
    fecha_pago: datetime
    metodo_pago: MetodoPago
    confirmado: bool

    @field_validator('fecha_pago', mode='before')
    @classmethod
    def default_fecha_pago(cls, v):
        if not v:
            logger.info("[PagoBaseSchema] No se recibió fecha_pago, se asigna datetime.now()")
            return datetime.now()
        try:
            return v
        except Exception as e:
            logger.error(f"[PagoBaseSchema] Error procesando fecha_pago: {e}")
            raise ValueError("fecha_pago inválida")

class PagoCreateSchema(PagoBaseSchema):
    pass

class PagoSchema(PagoBaseSchema):
    id_pago: int

    class Config:
        from_attributes = True
