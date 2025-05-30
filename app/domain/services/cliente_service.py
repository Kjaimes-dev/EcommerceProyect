from app.ports.repositories.cliente_port import ClientePort
from app.domain.models.cliente import Cliente
from sqlalchemy.orm import Session
from fastapi import HTTPException
import logging
logger = logging.getLogger(__name__)

class ClienteService:
    def __init__(self, repository: ClientePort):
        self.repository = repository

    def list_clients(self) -> list[Cliente]:
        try:
            clients = self.repository.get_all()
            if not clients:
                print("Advertencia: No se encontraron clientes en la base de datos.")
            return clients
        except Exception as e:
            print(f"Error al listar clientes: {e}")
            return []

    def get_client(self, client_id: int) -> Cliente:
        try:
            cliente = self.repository.get_by_id(client_id)
            if not cliente:
                raise HTTPException(status_code=404, detail=f"Cliente con ID {client_id} no encontrado.")
            return cliente
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"[ClienteService] Error inesperado al obtener cliente con ID {client_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Error interno al obtener cliente con ID {client_id}: {e}")



    def create_client(self, client: Cliente) -> Cliente:
        try:
            if not isinstance(client, Cliente):
                logger.warning("[ClienteService] El objeto proporcionado no es una instancia válida de Cliente.")
                raise HTTPException(status_code=400, detail="Datos del cliente no válidos.")
            return self.repository.create(client)
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"[ClienteService] Error inesperado al crear cliente: {e}")
            raise HTTPException(status_code=500, detail=f"Error interno al crear cliente: {e}")
