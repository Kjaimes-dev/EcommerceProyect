from dataclasses import dataclass

@dataclass
class Cliente:
    id_cliente: int
    nombre: str
    email: str
    telefono: str
    cedula: str
    direccion: str

    def __post_init__(self):
        if self.id_cliente is None or not isinstance(self.id_cliente, int):
            print(f"[Cliente] Advertencia: id_cliente inválido: {self.id_cliente}")
        if not self.nombre or not isinstance(self.nombre, str):
            print(f"[Cliente] Advertencia: nombre inválido: {self.nombre}")
        if not self.email or not isinstance(self.email, str):
            print(f"[Cliente] Advertencia: email inválido: {self.email}")
        if not self.telefono or not isinstance(self.telefono, str):
            print(f"[Cliente] Advertencia: telefono inválido: {self.telefono}")
        if not self.cedula or not isinstance(self.cedula, str):
            print(f"[Cliente] Advertencia: cedula inválida: {self.cedula}")
        if not self.direccion or not isinstance(self.direccion, str):
            print(f"[Cliente] Advertencia: direccion inválida: {self.direccion}")
