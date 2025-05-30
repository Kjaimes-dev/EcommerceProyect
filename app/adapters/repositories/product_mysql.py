from app.ports.repositories.product_port import ProductPort
from app.domain.models.product import Product
from sqlalchemy import text
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

class ProductMySQLRepository(ProductPort):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        try:
            result = self.db.execute(text("SELECT * FROM Producto"))
            products = [Product(**dict(row._mapping)) for row in result]
            products = [p for p in products if p.precio > 0]
            return products
        except Exception as e:
            logger.error(f"[ProductMySQLRepository.get_all] Error al obtener productos: {e}")
            return []

    def get_by_id(self, product_id: int):
        try:
            result = self.db.execute(
                text("SELECT * FROM Producto WHERE id_producto = :id"),
                {"id": product_id}
            ).fetchone()
            if result:
                return Product(**dict(result._mapping))
            else:
                logger.info(f"[ProductMySQLRepository.get_by_id] Producto no encontrado con id: {product_id}")
                return None
        except Exception as e:
            logger.error(f"[ProductMySQLRepository.get_by_id] Error al obtener producto id {product_id}: {e}")
            return None

    def create(self, product: Product):
        try:
            query = text("""
                INSERT INTO Producto (nombre, descripcion, precio, stock, categoria)
                VALUES (:nombre, :descripcion, :precio, :stock, :categoria)
            """)
            self.db.execute(query, {
                "nombre": product.nombre,
                "descripcion": product.descripcion,
                "precio": product.precio,
                "stock": product.stock,
                "categoria": product.categoria,
            })
            self.db.commit()
        except Exception as e:
            logger.error(f"[ProductMySQLRepository.create] Error al insertar producto: {e}")
            self.db.rollback()
            return None

        try:
            last_id = self.db.execute(text("SELECT LAST_INSERT_ID()")).scalar()
            return Product(
                id_producto=last_id,
                nombre=product.nombre,
                descripcion=product.descripcion,
                precio=product.precio,
                stock=product.stock,
                categoria=product.categoria
            )
        except Exception as e:
            logger.error(f"[ProductMySQLRepository.create] Error al obtener id insertado: {e}")
            return None