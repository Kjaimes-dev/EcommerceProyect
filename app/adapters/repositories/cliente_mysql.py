from app.ports.repositories.cliente_port import ClientePort
from app.domain.models.cliente import Cliente
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException
import bcrypt
import logging
logger = logging.getLogger(__name__)

class ClienteMySQLRepository(ClientePort):
    def __init__(self, db: Session):
        if db is None:
            print("[ClienteMySQLRepository] Error: Sesión de base de datos es None.")
            raise ValueError("Sesión de base de datos no puede ser None.")
        self.db = db

    def get_all(self):
        try:
            result = self.db.execute(text("SELECT * FROM Cliente"))
            clientes = [Cliente(**dict(row._mapping)) for row in result]
            return clientes
        except SQLAlchemyError as e:
            print(f"[ClienteMySQLRepository] Error en get_all: {e}")
            raise HTTPException(status_code=500, detail="Error al obtener los clientes.")

    def get_by_id(self, cliente_id: int):
        try:
            result = self.db.execute(
                text("SELECT * FROM Cliente WHERE id_cliente = :id"),
                {"id": cliente_id}
            ).fetchone()
            if not result:
                raise HTTPException(status_code=404, detail=f"Cliente con ID {cliente_id} no encontrado.")
            return Cliente(**dict(result._mapping))
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"[ClienteMySQLRepository] Error inesperado al obtener cliente con ID {cliente_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Error interno al obtener cliente con ID {cliente_id}: {e}")



    def create(self, cliente: Cliente):
        if cliente is None:
            logger.warning("[ClienteMySQLRepository] cliente es None.")
            raise HTTPException(status_code=400, detail="Datos del cliente requeridos.")

        if cliente.contrasena_hash:
            cliente.contrasena_hash = bcrypt.hashpw(cliente.contrasena_hash.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        query = text("""
            INSERT INTO Cliente (nombre, email, telefono, cedula, direccion, contrasena_hash)
            VALUES (:nombre, :email, :telefono, :cedula, :direccion, :contrasena_hash)
        """)
        try:
            self.db.execute(query, cliente.__dict__)
            self.db.commit()

            last_id = self.db.execute(text("SELECT LAST_INSERT_ID()")).scalar()
            cliente_data = cliente.__dict__.copy()
            cliente_data.pop("id_cliente", None)
            return Cliente(id_cliente=last_id, **cliente_data)
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"[ClienteMySQLRepository] Error de integridad al crear cliente: {e}")
            if "Duplicate entry" in str(e.orig):
                raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado.")
            raise HTTPException(status_code=500, detail="Error al crear el cliente.")
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"[ClienteMySQLRepository] Error general al crear cliente: {e}")
            raise HTTPException(status_code=500, detail="Error inesperado al crear el cliente.")