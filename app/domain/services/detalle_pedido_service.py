from app.ports.repositories.detalle_pedido_port import DetallePedidoPort
from app.domain.models.detalle_pedido import DetallePedido
from fastapi import HTTPException

class DetallePedidoService:
    def __init__(self, repository: DetallePedidoPort):
        self.repository = repository

    def listar(self) -> list[DetallePedido]:
        try:
            detalles = self.repository.listar()
            if not detalles:
                raise HTTPException(status_code=404, detail="No se encontraron detalles de pedidos.")
            return detalles
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al listar detalles de pedidos: {e}")

    def obtener(self, id_detalle: int) -> DetallePedido:
        try:
            detalle = self.repository.obtener(id_detalle)
            if not detalle:
                raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado.")
            return detalle
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener detalle de pedido: {e}")

    def crear(self, detalle_pedido: DetallePedido) -> DetallePedido:
        try:
            return self.repository.crear(detalle_pedido)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear detalle de pedido: {e}")