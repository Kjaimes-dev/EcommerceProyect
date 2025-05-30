from dataclasses import dataclass, field
from enum import Enum
from decimal import Decimal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CategoriaProducto(str, Enum):
    ropa = 'ropa'
    collares = 'collares'

@dataclass
class Product:
    id_producto: int = field()
    nombre: str = field()
    descripcion: str = field()
    precio: float = field()
    stock: int = field()
    categoria: CategoriaProducto = field()

    def __post_init__(self):
        try:
            if not isinstance(self.id_producto, int) or self.id_producto <= 0:
                logger.warning(f"[Product] id_producto inválido: {self.id_producto}")
            if not isinstance(self.nombre, str) or not self.nombre.strip():
                logger.warning("[Product] nombre está vacío o no es string")
            if not isinstance(self.descripcion, str):
                logger.warning("[Product] descripcion no es string")
            if not isinstance(self.precio, (float, Decimal)) or self.precio <= 0:
                logger.warning(f"[Product] precio inválido: {self.precio}")
            else:
                logger.info(f"[Product] precio válido: {self.precio}")
            if not isinstance(self.stock, int) or self.stock < 0:
                logger.warning(f"[Product] stock inválido: {self.stock}")
            if isinstance(self.categoria, str):  # Convertir cadena a CategoriaProducto
                try:
                    self.categoria = CategoriaProducto(self.categoria)
                except ValueError:
                    logger.warning(f"[Product] categoria no válida: {self.categoria}")
            if not isinstance(self.categoria, CategoriaProducto):
                logger.warning(f"[Product] categoria inválida: {self.categoria}")
        except Exception as e:
            logger.error(f"[Product] Error en __post_init__: {e}")