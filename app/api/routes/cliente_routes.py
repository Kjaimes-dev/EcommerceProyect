from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.adapters.repositories.cliente_mysql import ClienteMySQLRepository
from app.domain.services.cliente_service import ClienteService
from app.api.schemas.scliente import ClienteCreateUpdateSchema, ClienteSchema
from app.domain.models.cliente import Cliente
import logging
logger = logging.getLogger(__name__)

router = APIRouter()

def get_cliente_service(db: Session = Depends(get_db)):
    try:
        return ClienteService(ClienteMySQLRepository(db))
    except Exception as e:
        print(f"Error al inicializar ClienteService: {e}")
        raise HTTPException(status_code=500, detail="Error interno en el servicio de cliente")

@router.get("/clientes", response_model=list[ClienteSchema])
def get_clients(service: ClienteService = Depends(get_cliente_service)):
    try:
        clientes = service.list_clients()
        if clientes is None:
            print("Advertencia: list_clients() devolvió None.")
            raise HTTPException(status_code=404, detail="No se encontraron clientes")
        return clientes
    except Exception as e:
        print(f"Error en get_clients: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener la lista de clientes")

@router.get("/clientes/{cliente_id}", response_model=ClienteSchema)
def get_client(cliente_id: int, service: ClienteService = Depends(get_cliente_service)):
    try:
        cliente = service.get_client(cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail=f"Cliente con ID {cliente_id} no encontrado.")
        return cliente
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[get_client] Error inesperado al obtener cliente con ID {cliente_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno al obtener cliente con ID {cliente_id}: {e}")


@router.post("/clientes", response_model=ClienteSchema)
def create_client(cliente_data: ClienteCreateUpdateSchema, service: ClienteService = Depends(get_cliente_service)):
    try:
        cliente = Cliente(
            id_cliente=0,
            nombre=cliente_data.nombre,
            email=cliente_data.email,
            telefono=cliente_data.telefono,
            cedula=cliente_data.cedula,
            direccion=cliente_data.direccion,
            contrasena_hash=cliente_data.contrasena_hash
        )
        nuevo_cliente = service.create_client(cliente)
        return nuevo_cliente
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[create_client] Error inesperado al crear cliente: {e}")
        raise HTTPException(status_code=500, detail="Error interno al crear cliente")