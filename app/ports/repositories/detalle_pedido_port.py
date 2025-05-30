from abc import ABC, abstractmethod
from app.domain.models.detalle_pedido import DetallePedido

class DetallePedidoPort(ABC):
    @abstractmethod
    def listar(self) -> list[DetallePedido]:
        pass

    @abstractmethod
    def obtener(self, id_detalle: int) -> DetallePedido:
        pass

    @abstractmethod
    def crear(self, detalle_pedido: DetallePedido) -> DetallePedido:
        pass