from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.adapters.repositories.product_mysql import ProductMySQLRepository
from app.domain.services.product_service import ProductService
from app.api.schemas.sproduct import ProductoCreateUpdateSchema, ProductoSchema
from app.domain.models.product import Product
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

def get_product_service(db: Session = Depends(get_db)):
    try:
        service = ProductService(ProductMySQLRepository(db))
        return service
    except Exception as e:
        logger.error(f"[product_routes] Error al obtener ProductService: {e}")
        raise HTTPException(status_code=500, detail="Error interno al inicializar servicio de productos")

@router.get("/products", response_model=list[ProductoSchema])
def get_products(service: ProductService = Depends(get_product_service)):
    try:
        products = service.list_products()
        if products is None:
            logger.warning("[product_routes] list_products devolvió None")
            return []
        return products
    except Exception as e:
        logger.error(f"[product_routes] Error al listar productos: {e}")
        raise HTTPException(status_code=500, detail="Error interno al listar productos")

@router.post("/products", response_model=ProductoSchema)
def create_product(product_data: ProductoCreateUpdateSchema, service: ProductService = Depends(get_product_service)):
    try:
        product = Product(
            id_producto=0,
            nombre=product_data.nombre,
            descripcion=product_data.descripcion,
            precio=product_data.precio,
            stock=product_data.stock,
            categoria=product_data.categoria
        )
    except Exception as e:
        logger.error(f"[product_routes] Error al construir Product: {e}")
        raise HTTPException(status_code=400, detail="Datos de producto inválidos")

    try:
        created = service.create_product(product)
        if not created:
            logger.error("[product_routes] service.create_product devolvió un valor no esperado")
            raise HTTPException(status_code=500, detail="Error interno al crear producto")
        return created
    except Exception as e:
        logger.error(f"[product_routes] Error al crear producto: {e}")
        raise HTTPException(status_code=500, detail="Error interno al crear producto")
