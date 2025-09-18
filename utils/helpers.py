## Funciones auxiliares y utilidades del sistema - PyQt5 Version

from datetime import datetime
from config.settings import *

def generar_id(prefijo):
    return f"{prefijo}{datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]}"

def cargar_categorias(): # Carga desde la BD o devuelve categorías por defecto
    try:
        from db.database import db
        query = "SELECT nombre FROM categorias ORDER BY nombre"
        result = db.execute_query(query)
        categorias = [row[0] for row in result]
        if categorias:
            return categorias
        else:
            # Si no hay categorías en BD, devolver las por defecto
            return ["Abarrotes", "Bebidas", "Lácteos", "Carnes", "Frutas y Verduras", "Limpieza", "Panadería"]
    except Exception as e:
        print(f"Error cargando categorías: {e}")
        return ["Abarrotes", "Bebidas", "Lácteos", "Carnes", "Frutas y Verduras", "Limpieza", "Panadería"]

def formatear_precio(precio):
    try:
        return f"S/ {float(precio):.2f}"
    except:
        return "S/ 0.00"

def validar_numero(valor, tipo="float"):
    try:
        return (int(valor), True) if tipo == "int" else (float(valor), True)
    except:
        return 0, False
