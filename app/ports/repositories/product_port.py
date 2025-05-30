from abc import ABC, abstractmethod
from app.domain.models.product import Product

class ProductPort(ABC):
    @abstractmethod
    def get_all(self) -> list[Product]:
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Product:
        pass

    @abstractmethod
    def create(self, product: Product) -> Product:
        pass
