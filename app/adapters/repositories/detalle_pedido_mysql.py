from app.ports.repositories.detalle_pedido_port import DetallePedidoPort
from app.domain.models.detalle_pedido import DetallePedido
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
import logging
logger = logging.getLogger(__name__)

class DetallePedidoMySQLRepository(DetallePedidoPort):
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[DetallePedido]:
        try:
            result = self.db.execute(text("SELECT * FROM DetallePedido"))
            return [DetallePedido(**dict(row._mapping)) for row in result]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al listar detalles de pedidos: {e}")

    def obtener(self, id_detalle: int) -> DetallePedido:
        try:
            result = self.db.execute(
                text("SELECT * FROM DetallePedido WHERE id_detalle = :id"),
                {"id": id_detalle}
            ).fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado.")
            return DetallePedido(**dict(result._mapping))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener detalle de pedido: {e}")

    def crear(self, detalle_pedido: DetallePedido) -> DetallePedido:
        pedido_existente = self.db.execute(
            text("SELECT id_pedido FROM Pedido WHERE id_pedido = :id_pedido"),
            {"id_pedido": detalle_pedido.id_pedido}
        ).fetchone()

        if not pedido_existente:
            raise HTTPException(status_code=400, detail=f"El id_pedido {detalle_pedido.id_pedido} no existe en la tabla Pedido.")

        producto_existente = self.db.execute(
            text("SELECT id_producto FROM Producto WHERE id_producto = :id_producto"),
            {"id_producto": detalle_pedido.id_producto}
        ).fetchone()

        if not producto_existente:
            raise HTTPException(status_code=400, detail=f"El id_producto {detalle_pedido.id_producto} no existe en la tabla Producto.")

        query = text("""
            INSERT INTO DetallePedido (id_pedido, id_producto, cantidad, precio_unitario)
            VALUES (:id_pedido, :id_producto, :cantidad, :precio_unitario)
        """)
        try:
            self.db.execute(query, detalle_pedido.__dict__)
            self.db.commit()
            last_id = self.db.execute(text("SELECT LAST_INSERT_ID()")).scalar()
            result = self.db.execute(
                text("SELECT * FROM DetallePedido WHERE id_detalle = :id"),
                {"id": last_id}
            ).fetchone()
            return DetallePedido(**dict(result._mapping))
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"[DetallePedidoMySQLRepository] Error de integridad al crear detalle de pedido: {e}")
            raise HTTPException(status_code=400, detail="Violación de clave foránea: asegúrate de que id_pedido e id_producto existan.")
        except Exception as e:
            self.db.rollback()
            logger.error(f"[DetallePedidoMySQLRepository] Error inesperado al crear detalle de pedido: {e}")
            raise HTTPException(status_code=500, detail="Error interno al crear detalle de pedido.")