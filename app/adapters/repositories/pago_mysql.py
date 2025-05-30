from app.ports.repositories.pago_port import PagoPort
from app.domain.models.pago import Pago
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import HTTPException

class PagoMySQLRepository(PagoPort):
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[Pago]:
        try:
            result = self.db.execute(text("SELECT * FROM Pago"))
            return [Pago(**dict(row._mapping)) for row in result]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al listar pagos: {e}")

    def obtener(self, id_pago: int) -> Pago:
        try:
            result = self.db.execute(
                text("SELECT * FROM Pago WHERE id_pago = :id"),
                {"id": id_pago}
            ).fetchone()
            if not result:
                raise HTTPException(status_code=404, detail=f"Pago con id {id_pago} no encontrado.")
            return Pago(**dict(result._mapping))
        except HTTPException as e:

            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener pago con id {id_pago}: {e}")

    def crear(self, pago: Pago) -> Pago:
        
        pedido_existente = self.db.execute(
            text("SELECT id_pedido FROM Pedido WHERE id_pedido = :id_pedido"),
            {"id_pedido": pago.id_pedido}
        ).fetchone()

        if not pedido_existente:
            raise HTTPException(status_code=400, detail=f"El id_pedido {pago.id_pedido} no existe en la tabla Pedido.")

        query = text("""
            INSERT INTO Pago (id_pedido, monto, fecha_pago, metodo_pago, confirmado)
            VALUES (:id_pedido, :monto, :fecha_pago, :metodo_pago, :confirmado)
        """)
        try:
            self.db.execute(query, pago.__dict__)
            self.db.commit()
            last_id = self.db.execute(text("SELECT LAST_INSERT_ID()")).scalar()
            result = self.db.execute(
                text("SELECT * FROM Pago WHERE id_pago = :id"),
                {"id": last_id}
            ).fetchone()
            return Pago(**dict(result._mapping))
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear pago: {e}")