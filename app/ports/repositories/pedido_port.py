from abc import ABC, abstractmethod
from app.domain.models.pedido import Pedido

class PedidoPort(ABC):
    @abstractmethod
    def listar(self) -> list[Pedido]:
        pass

    @abstractmethod
    def obtener(self, pedido_id: int) -> Pedido:
        pass

    @abstractmethod
    def crear(self, pedido: Pedido) -> Pedido:
        pass

    @abstractmethod
    def actualizar_estado(self, pedido_id: int, estado: str) -> Pedido:
        pass