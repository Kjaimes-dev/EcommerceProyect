from abc import ABC, abstractmethod
from app.domain.models.pago import Pago

class PagoPort(ABC):
    @abstractmethod
    def listar(self) -> list[Pago]:
        pass

    @abstractmethod
    def obtener(self, id_pago: int) -> Pago:
        pass

    @abstractmethod
    def crear(self, pago: Pago) -> Pago:
        pass