# app/domain/services/product_service.py
from app.ports.repositories.product_port import ProductPort
from app.domain.models.product import Product

class ProductService:
    def __init__(self, repository: ProductPort):
        if repository is None:
            print("[ProductService] Advertencia: repositorio recibido es None.")
        self.repository = repository

    def list_products(self) -> list[Product]:
        try:
            products = self.repository.get_all()
            if not isinstance(products, list):
                print("[ProductService] Advertencia: get_all no retornó una lista.")
            return products
        except Exception as e:
            print(f"[ProductService] Error en list_products: {e}")
            return []

    def get_product(self, product_id: int) -> Product:
        if product_id is None or not isinstance(product_id, int) or product_id < 0:
            print(f"[ProductService] Advertencia: ID inválido en get_product: {product_id}")
        try:
            return self.repository.get_by_id(product_id)
        except Exception as e:
            print(f"[ProductService] Error en get_product con ID {product_id}: {e}")
            return None

    def create_product(self, product: Product):
        if product is None:
            print("[ProductService] Advertencia: Objeto product es None en create_product.")
        try:
            return self.repository.create(product)
        except Exception as e:
            print(f"[ProductService] Error en create_product: {e}")
            return None
