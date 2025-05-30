#app/ports/repositories/cliente_port.py
from abc import ABC, abstractmethod
from app.domain.models.cliente import Cliente

class ClientePort(ABC):
    @abstractmethod
    def get_all(self) -> list[Cliente]:
        pass

    @abstractmethod
    def get_by_id(self, cliente_id: int) -> Cliente:
        pass

    @abstractmethod
    def create(self, cliente: Cliente) -> Cliente:
        pass
