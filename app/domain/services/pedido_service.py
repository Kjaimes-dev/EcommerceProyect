from app.ports.repositories.pedido_port import PedidoPort
from app.domain.models.pedido import Pedido
from fastapi import HTTPException

class PedidoService:
    def __init__(self, repository: PedidoPort):
        self.repository = repository

    def listar(self) -> list[Pedido]:
        try:
            pedidos = self.repository.listar()
            if not pedidos:
                raise HTTPException(status_code=404, detail="No se encontraron pedidos.")
            return pedidos
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al listar pedidos: {e}")

    def obtener(self, pedido_id: int) -> Pedido:
        try:
            pedido = self.repository.obtener(pedido_id)
            if not pedido:
                raise HTTPException(status_code=404, detail="Pedido no encontrado.")
            return pedido
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener pedido: {e}")

    def crear(self, pedido: Pedido) -> Pedido:
        try:
            return self.repository.crear(pedido)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear pedido: {e}")

    def actualizar_estado(self, pedido_id: int, estado: str) -> Pedido:
        try:
            pedido_actualizado = self.repository.actualizar_estado(pedido_id, estado)
            if not pedido_actualizado:
                raise HTTPException(status_code=404, detail="Pedido no encontrado.")
            return pedido_actualizado
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar estado del pedido: {e}")