## Configuraciones del sistema Minimarket Don Manuelito - Sprint 1

import os

# Rutas de archivos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "db")
IMG_DIR = os.path.join(DB_DIR, "imagenes")

# Archivos de datos - Excel para Sprint 1
PRODUCTOS_FILE = os.path.join(DB_DIR, "productos.xlsx")
CATEGORIAS_FILE = os.path.join(DB_DIR, "categorias.xlsx")
EMPLEADOS_FILE = os.path.join(DB_DIR, "empleados.xlsx")

# Crear directorios si no existen
os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

# Configuraciones de la aplicación
APP_NAME = "Minimarket Don Manuelito"
APP_VERSION = "1.0.0 - Sprint 1"
WINDOW_SIZE = "1800x1200"

# Colores del tema
THEME_COLOR = "#256d85"
SUCCESS_COLOR = "#2ecc71"
WARNING_COLOR = "#f39c12"
ERROR_COLOR = "#e74c3c"
INFO_COLOR = "#3498db"
