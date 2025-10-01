# -*- coding: utf-8 -*-
## Configuración y manejo de la base de datos SQLite
## Sistema de IDs P0001 implementado con tabla de secuencias

import sqlite3
import os
from views.settings import DB_DIR

class Database:
    def __init__(self):
        self.db_path = os.path.join(DB_DIR, "minimarket.db")
        self.init_database()
    
    def get_connection(self): # Conecta a la BD - SQLite
        conn = sqlite3.connect(self.db_path)
        # Configurar la conexión para manejar UTF-8 correctamente
        conn.execute("PRAGMA encoding = 'UTF-8'")
        # Usar text_factory para manejar correctamente los strings
        conn.text_factory = lambda x: str(x, 'utf-8', 'replace') if isinstance(x, bytes) else x
        return conn
    
    def init_database(self): # Inicia la BD 
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de categorías
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                descripcion TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de secuencias para generar IDs personalizados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS secuencias (
                tabla TEXT PRIMARY KEY,
                ultimo_numero INTEGER DEFAULT 0
            )
        ''')
        
        # Insertar secuencia para productos si no existe
        cursor.execute('''
            INSERT OR IGNORE INTO secuencias (tabla, ultimo_numero) 
            VALUES ('productos', 0)
        ''')
        
        # Tabla de productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                tipo_corte TEXT,
                precio REAL NOT NULL DEFAULT 0,
                stock INTEGER NOT NULL DEFAULT 0,
                stock_minimo INTEGER NOT NULL DEFAULT 0,
                imagen TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de empleados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS empleados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                usuario TEXT NOT NULL UNIQUE,
                contraseña TEXT NOT NULL,
                rol TEXT NOT NULL DEFAULT 'empleado',
                activo INTEGER NOT NULL DEFAULT 1,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de ventas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id TEXT PRIMARY KEY,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                empleado_id INTEGER,
                total REAL NOT NULL DEFAULT 0,
                metodo_pago TEXT,
                estado TEXT DEFAULT 'completada',
                FOREIGN KEY (empleado_id) REFERENCES empleados (id)
            )
        ''')
        
        # Tabla de detalle de ventas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detalle_ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id TEXT NOT NULL,
                producto_id TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (venta_id) REFERENCES ventas (id),
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')
        
        # Tabla de compras
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compras (
                id TEXT PRIMARY KEY,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                proveedor TEXT,
                total REAL NOT NULL DEFAULT 0,
                estado TEXT DEFAULT 'completada'
            )
        ''')
        
        # Tabla de detalle de compras
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detalle_compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                compra_id TEXT NOT NULL,
                producto_id TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (compra_id) REFERENCES compras (id),
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')
        
        # Tabla de despachos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS despachos (
                id TEXT PRIMARY KEY,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                destino TEXT,
                estado TEXT DEFAULT 'pendiente',
                observaciones TEXT
            )
        ''')
        
        # Tabla de detalle de despachos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detalle_despachos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                despacho_id TEXT NOT NULL,
                producto_id TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                FOREIGN KEY (despacho_id) REFERENCES despachos (id),
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')
        
        # Tabla de configuración
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracion (
                clave TEXT PRIMARY KEY,
                valor TEXT NOT NULL,
                descripcion TEXT,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insertar datos iniciales si no existen
        self._insertar_datos_iniciales(cursor)
        
        conn.commit()
        conn.close()
    
    def _insertar_datos_iniciales(self, cursor):
        """Inserta datos iniciales en la base de datos"""
        
        # Insertar usuario administrador por defecto
        cursor.execute('''
            INSERT OR IGNORE INTO empleados (nombre, apellido, usuario, contraseña, rol)
            VALUES ('Administrador', 'Sistema', 'admin', 'admin', 'administrador')
        ''')
        
        # Insertar categorías básicas
        categorias_basicas = [
            ('Abarrotes', 'Productos de consumo básico'),
            ('Bebidas', 'Bebidas alcohólicas y no alcohólicas'),
            ('Lácteos', 'Productos lácteos y derivados'),
            ('Carnes', 'Carnes y embutidos'),
            ('Frutas y Verduras', 'Productos frescos'),
            ('Limpieza', 'Productos de limpieza e higiene'),
            ('Panadería', 'Pan y productos de panadería')
        ]
        
        for nombre, descripcion in categorias_basicas:
            cursor.execute('''
                INSERT OR IGNORE INTO categorias (nombre, descripcion)
                VALUES (?, ?)
            ''', (nombre, descripcion))
        
        # Insertar configuraciones básicas
        configuraciones = [
            ('nombre_empresa', 'Minimarket Don Manuelito', 'Nombre de la empresa'),
            ('ruc_empresa', '10730291529', 'RUC de la empresa'),
            ('direccion_empresa', 'Av. Principal 123', 'Dirección de la empresa'),
            ('telefono_empresa', '123-456-789', 'Teléfono de la empresa'),
            ('moneda', 'PEN', 'Moneda utilizada'),
            ('igv', '18', 'Porcentaje de IGV')
        ]
        
        for clave, valor, descripcion in configuraciones:
            cursor.execute('''
                INSERT OR IGNORE INTO configuracion (clave, valor, descripcion)
                VALUES (?, ?, ?)
            ''', (clave, valor, descripcion))
    
    def execute_query(self, query, params=None): # Ejecuta una consulta
        conn = self.get_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        
        return result
    
    def execute_insert(self, query, params=None): # Ejecuta un INSERT y retorna el ID último
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        last_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return last_id

# Instancia global de la base de datos
db = Database()