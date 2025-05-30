# app/api/schemas/sdetalle_pedido.py
from pydantic import BaseModel, conint, confloat, field_validator, model_validator

from pydantic import BaseModel, conint, confloat, field_validator

class DetallePedidoBaseSchema(BaseModel):
    id_pedido: conint(gt=0)
    id_producto: conint(gt=0)
    cantidad: conint(gt=0)
    precio_unitario: confloat(gt=0)

    @field_validator('id_pedido', 'id_producto', 'cantidad', 'precio_unitario', mode='before')
    @classmethod
    def validate_fields(cls, v, info):
        if v is None:
            print(f"[DetallePedidoBaseSchema] Advertencia: '{info.field_name}' es requerido")
        return v

class DetallePedidoCreateSchema(DetallePedidoBaseSchema):
    pass

class DetallePedidoSchema(DetallePedidoBaseSchema):
    id_detalle: int

    class Config:
        from_attributes = True

    @field_validator('id_detalle', mode='before')
    @classmethod
    def validate_id_detalle(cls, v):
        if v is None or v <= 0:
            print("[DetallePedidoSchema] Advertencia: Campo 'id_detalle' faltante o inválido")
        return v