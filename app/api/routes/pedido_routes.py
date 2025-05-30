from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.domain.services.pedido_service import PedidoService
from app.adapters.repositories.pedido_mysql import PedidoMySQLRepository
from app.api.schemas.spedido import PedidoCreateSchema, PedidoUpdateSchema, PedidoSchema
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def get_pedido_service(db: Session = Depends(get_db)):
    return PedidoService(PedidoMySQLRepository(db))

@router.get("/pedidos", response_model=list[PedidoSchema])
def listar_pedidos(service: PedidoService = Depends(get_pedido_service)):
    try:
        pedidos = service.listar()
        if pedidos is None:
            logger.warning("[listar_pedidos] service.listar() retornó None")
            return []
        return pedidos
    except Exception as e:
        logger.error(f"[listar_pedidos] Error al listar pedidos: {e}")
        raise HTTPException(status_code=500, detail="Error interno al listar pedidos")

@router.get("/pedidos/{pedido_id}", response_model=PedidoSchema)
def obtener_pedido(pedido_id: int, service: PedidoService = Depends(get_pedido_service)):
    try:
        pedido = service.obtener(pedido_id)
        if not pedido:
            logger.info(f"[obtener_pedido] Pedido no encontrado con id: {pedido_id}")
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return pedido
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[obtener_pedido] Error al obtener pedido {pedido_id}: {e}")
        raise HTTPException(status_code=500, detail="Error interno al obtener pedido")

@router.post("/pedidos", response_model=PedidoSchema, status_code=201)
def crear_pedido(pedido_data: PedidoCreateSchema, service: PedidoService = Depends(get_pedido_service)):
    try:
        resultado = service.crear(pedido_data)
        if resultado is None:
            raise HTTPException(status_code=500, detail="No se pudo crear el pedido.")
        return resultado
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[crear_pedido] Error inesperado al crear pedido: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno al crear pedido: {e}")

@router.put("/pedidos/{pedido_id}", response_model=PedidoSchema)
def actualizar_estado_pedido(pedido_id: int, datos_actualizados: PedidoUpdateSchema, service: PedidoService = Depends(get_pedido_service)):
    try:
        pedido_actualizado = service.actualizar_estado(pedido_id, datos_actualizados.estado)
        if not pedido_actualizado:
            logger.info(f"[actualizar_estado_pedido] Pedido no encontrado con id: {pedido_id}")
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return pedido_actualizado
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[actualizar_estado_pedido] Error al actualizar pedido {pedido_id}: {e}")
        raise HTTPException(status_code=500, detail="Error interno al actualizar pedido")