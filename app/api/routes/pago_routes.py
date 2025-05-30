from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.domain.services.pago_service import PagoService
from app.adapters.repositories.pago_mysql import PagoMySQLRepository
from app.api.schemas.spago import PagoCreateSchema, PagoSchema
from app.domain.models.pago import Pago
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def get_pago_service(db: Session = Depends(get_db)):
    return PagoService(PagoMySQLRepository(db))

@router.get("/pagos", response_model=list[PagoSchema])
def listar_pagos(service: PagoService = Depends(get_pago_service)):
    try:
        return service.listar()
    except Exception as e:
        logger.error(f"[listar_pagos] Error al listar pagos: {e}")
        raise HTTPException(status_code=500, detail="Error interno al listar pagos")

@router.get("/pagos/{id_pago}", response_model=PagoSchema)
def obtener_pago(id_pago: int, service: PagoService = Depends(get_pago_service)):
    try:
        return service.obtener(id_pago)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[obtener_pago] Error inesperado al obtener pago {id_pago}: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno al obtener pago {id_pago}: {e}")

@router.post("/pagos", response_model=PagoSchema, status_code=201)
def crear_pago(pago_data: PagoCreateSchema, service: PagoService = Depends(get_pago_service)):
    try:
        pago = Pago(
            id_pago=0,
            id_pedido=pago_data.id_pedido,
            monto=pago_data.monto,
            fecha_pago=pago_data.fecha_pago,
            metodo_pago=pago_data.metodo_pago,
            confirmado=pago_data.confirmado
        )
        return service.crear(pago)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[crear_pago] Error inesperado al crear pago: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno al crear pago: {e}")