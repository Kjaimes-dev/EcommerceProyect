from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.domain.services.detalle_pedido_service import DetallePedidoService
from app.adapters.repositories.detalle_pedido_mysql import DetallePedidoMySQLRepository
from app.api.schemas.sdetalle_pedido import DetallePedidoCreateSchema, DetallePedidoSchema
from app.domain.models.detalle_pedido import DetallePedido  # Importar el modelo
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def get_detalle_pedido_service(db: Session = Depends(get_db)):
    return DetallePedidoService(DetallePedidoMySQLRepository(db))

@router.get("/detalles_pedido", response_model=list[DetallePedidoSchema])
def listar_detalles(service: DetallePedidoService = Depends(get_detalle_pedido_service)):
    try:
        return service.listar()
    except Exception as e:
        logger.error(f"[listar_detalles] Error al listar detalles de pedido: {e}")
        raise HTTPException(status_code=500, detail="Error interno al listar detalles de pedido")

@router.get("/detalles_pedido/{id_detalle}", response_model=DetallePedidoSchema)
def obtener_detalle(id_detalle: int, service: DetallePedidoService = Depends(get_detalle_pedido_service)):
    try:
        return service.obtener(id_detalle)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[obtener_detalle] Error inesperado al obtener detalle de pedido {id_detalle}: {e}")
        raise HTTPException(status_code=500, detail="Error interno al obtener detalle de pedido")

@router.post("/detalles_pedido", response_model=DetallePedidoSchema, status_code=201)
def crear_detalle(detalle_data: DetallePedidoCreateSchema, service: DetallePedidoService = Depends(get_detalle_pedido_service)):
    try:
        detalle = DetallePedido(
            id_detalle=0,
            id_pedido=detalle_data.id_pedido,
            id_producto=detalle_data.id_producto,
            cantidad=detalle_data.cantidad,
            precio_unitario=detalle_data.precio_unitario
        )
        return service.crear(detalle)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[crear_detalle] Error inesperado al crear detalle de pedido: {e}")
        raise HTTPException(status_code=500, detail="Error interno al crear detalle de pedido")