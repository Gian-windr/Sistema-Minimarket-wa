## Modelo para manejar los datos de empleados - SQLite

from models.base_model import BaseModel
from db.database import db

class EmpleadoModel(BaseModel):
    def __init__(self):
        # Definir columnas de la tabla empleados
        columns = ['id', 'nombre', 'apellido', 'usuario', 'contraseña', 'rol', 'activo']
        super().__init__('empleados', columns)
    
    def validar_credenciales(self, usuario, password):
        """Valida las credenciales de un empleado"""
        try:
            empleados = self.get_all(
                "usuario = ? AND contraseña = ? AND activo = 1",
                (usuario, password)
            )
            return len(empleados) > 0
        except Exception as e:
            print(f"Error validando credenciales: {e}")
            # Credenciales por defecto si hay error
            return usuario == "admin" and password == "admin"
    
    def obtener_por_usuario(self, usuario):
        """Obtiene un empleado por su nombre de usuario"""
        try:
            empleados = self.get_all("usuario = ? AND activo = 1", (usuario,))
            return empleados[0] if empleados else None
        except Exception as e:
            print(f"Error obteniendo empleado por usuario: {e}")
            return None
    
    def crear_empleado(self, nombre, apellido, usuario, contraseña, rol='empleado'):
        """Crea un nuevo empleado"""
        try:
            # Verificar que el usuario no exista
            if self.obtener_por_usuario(usuario):
                raise ValueError(f"El usuario '{usuario}' ya existe")
            
            empleado_data = {
                'nombre': nombre,
                'apellido': apellido,
                'usuario': usuario,
                'contraseña': contraseña,
                'rol': rol,
                'activo': 1
            }
            
            return self.create(empleado_data)
        except Exception as e:
            print(f"Error creando empleado: {e}")
            raise
    
    def actualizar_empleado(self, empleado_id, datos):
        """Actualiza un empleado existente"""
        try:
            return self.update(empleado_id, datos)
        except Exception as e:
            print(f"Error actualizando empleado: {e}")
            raise
    
    def desactivar_empleado(self, empleado_id):
        """Desactiva un empleado (no lo elimina)"""
        try:
            return self.update(empleado_id, {'activo': 0})
        except Exception as e:
            print(f"Error desactivando empleado: {e}")
            return False
    
    def obtener_empleados_activos(self):
        """Obtiene todos los empleados activos"""
        try:
            return self.get_all("activo = 1")
        except Exception as e:
            print(f"Error obteniendo empleados activos: {e}")
            return []