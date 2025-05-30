# app/api/schemas/spedido.py
from pydantic import BaseModel, conint, field_validator
from enum import Enum
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EstadoPedido(str, Enum):
    pendiente = 'pendiente'
    enviado = 'enviado'
    entregado = 'entregado'
    cancelado = 'cancelado'

class PedidoBaseSchema(BaseModel):
    id_cliente: conint(gt=0)
    estado: EstadoPedido

    @field_validator('id_cliente')
    @classmethod
    def validar_id_cliente(cls, v):
        if v <= 0:
            logger.warning("[PedidoBaseSchema] id_cliente debe ser mayor que cero")
        return v

class PedidoCreateSchema(PedidoBaseSchema):
    pass

class PedidoUpdateSchema(BaseModel):
    estado: EstadoPedido

    @field_validator('estado')
    @classmethod
    def validar_estado(cls, v):
        if v not in EstadoPedido:
            logger.warning(f"[PedidoUpdateSchema] Estado inválido: {v}")
        return v

class PedidoSchema(PedidoBaseSchema):
    id_pedido: int
    fecha: datetime

    @field_validator('id_pedido')
    @classmethod
    def validar_id_pedido(cls, v):
        if v <= 0:
            logger.warning("[PedidoSchema] id_pedido debe ser mayor que cero")
        return v

    @field_validator('fecha')
    @classmethod
    def validar_fecha(cls, v):
        if not isinstance(v, datetime):
            logger.warning("[PedidoSchema] fecha no es una instancia de datetime")
        return v

    class Config:
        from_attributes = True
