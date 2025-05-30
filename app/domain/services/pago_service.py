from app.ports.repositories.pago_port import PagoPort
from app.domain.models.pago import Pago
from fastapi import HTTPException

class PagoService:
    def __init__(self, repository: PagoPort):
        self.repository = repository

    def listar(self) -> list[Pago]:
        try:
            pagos = self.repository.listar()
            if not pagos:
                raise HTTPException(status_code=404, detail="No se encontraron pagos.")
            return pagos
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al listar pagos: {e}")

    def obtener(self, id_pago: int) -> Pago:
        try:
            pago = self.repository.obtener(id_pago)
            if not pago:
                raise HTTPException(status_code=404, detail="Pago no encontrado.")
            return pago
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener pago: {e}")

    def crear(self, pago: Pago) -> Pago:
        try:
            return self.repository.crear(pago)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear pago: {e}")