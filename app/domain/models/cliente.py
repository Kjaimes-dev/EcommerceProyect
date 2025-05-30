import bcrypt
from dataclasses import dataclass

@dataclass
class Cliente:
    id_cliente: int
    nombre: str
    email: str
    telefono: str
    cedula: str
    direccion: str
    contrasena_hash: str

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
        if not self.contrasena_hash or not isinstance(self.contrasena_hash, str):
            print(f"[Cliente] Advertencia: contrasena_hash inválida: {self.contrasena_hash}")
        else:
            self.contrasena_hash = self.hash_password(self.contrasena_hash)

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
