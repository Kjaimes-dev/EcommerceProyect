from app.ports.repositories.pedido_port import PedidoPort
from app.domain.models.pedido import Pedido
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import HTTPException

class PedidoMySQLRepository(PedidoPort):
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[Pedido]:
        try:
            result = self.db.execute(text("SELECT * FROM Pedido"))
            return [Pedido(**dict(row._mapping)) for row in result]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al listar pedidos: {e}")

    def obtener(self, pedido_id: int) -> Pedido:
        try:
            result = self.db.execute(
                text("SELECT * FROM Pedido WHERE id_pedido = :id"),
                {"id": pedido_id}
            ).fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Pedido no encontrado.")
            return Pedido(**dict(result._mapping))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener pedido: {e}")

    def crear(self, pedido: Pedido) -> Pedido:
        query = text("""
            INSERT INTO Pedido (id_cliente, estado)
            VALUES (:id_cliente, :estado)
        """)
        try:
            self.db.execute(query, {"id_cliente": pedido.id_cliente, "estado": pedido.estado.value})
            self.db.commit()
            last_id = self.db.execute(text("SELECT LAST_INSERT_ID()")).scalar()
            result = self.db.execute(
                text("SELECT * FROM Pedido WHERE id_pedido = :id"),
                {"id": last_id}
            ).fetchone()
            return Pedido(**dict(result._mapping))
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear pedido: {e}")

            
    def actualizar_estado(self, pedido_id: int, estado: str) -> Pedido:
        query = text("""
            UPDATE Pedido
            SET estado = :estado
            WHERE id_pedido = :id
        """)
        try:
            self.db.execute(query, {"estado": estado, "id": pedido_id})
            self.db.commit()
            return self.obtener(pedido_id)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar estado del pedido: {e}")