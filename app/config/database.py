from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    logger.error("[database] Variable de entorno DATABASE_URL no definida.")
else:
    try:
        engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, pool_timeout=30)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    except Exception as e:
        logger.error(f"[database] Error al crear engine o sessionmaker: {e}")


def get_db():
    try:
        db = SessionLocal()
    except Exception as e:
        logger.error(f"[database] Error al crear sesión DB: {e}")
        raise
    try:
        yield db
    finally:
        try:
            db.close()
        except Exception as e:
            logger.error(f"[database] Error al cerrar sesión DB: {e}")

# Prueba de conexión al iniciar la aplicación
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DATABASE();"))
        db_name = result.fetchone()
        if db_name and len(db_name) > 0:
            logger.info("[database] Conexión exitosa a la base de datos.")
            logger.info(f"[database] Nombre de la base de datos: {db_name[0]}")
            print("Conectado a la base:", db_name[0])
        else:
            logger.error("[database] No se pudo obtener el nombre de la base de datos.")
except Exception as e:
    logger.error(f"[database] Error en prueba de conexión inicial: {e}")
