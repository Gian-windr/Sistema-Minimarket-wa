## Modelo de Ventas - Sistema Minimarket

import pandas as pd
import sqlite3
from db.database import Database
from datetime import datetime

class VentaModel:
    def __init__(self):
        self.database = Database()
        self.crearTablas()
    
    def getConexion(self):
        return self.database.get_connection()
    
    def crearTablas(self):
        conexion = self.getConexion()
        cursor = conexion.cursor()
        
        # Verificar si la tabla ventas ya existe con estructura antigua
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ventas';")
        tabla_existe = cursor.fetchone()
        
        if not tabla_existe:
            # Tabla principal de ventas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ventas (
                    id TEXT PRIMARY KEY,
                    fecha_hora DATETIME,
                    total REAL,
                    empleado TEXT,
                    metodo_pago TEXT DEFAULT 'efectivo',
                    estado TEXT DEFAULT 'completada'
                )
            ''')
        else:
            # Verificar si tiene la columna fecha_hora
            cursor.execute("PRAGMA table_info(ventas);")
            columnas = [col[1] for col in cursor.fetchall()]
            
            if 'fecha_hora' not in columnas and 'fecha' in columnas:
                # Usar la estructura existente, no modificamos la tabla
                print("🔄 Usando tabla ventas existente con estructura original")
        
        # Tabla de detalle de ventas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS venta_detalles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id TEXT,
                producto_id TEXT,
                producto_nombre TEXT,
                cantidad INTEGER,
                precio_unitario REAL,
                subtotal REAL,
                FOREIGN KEY (venta_id) REFERENCES ventas (id),
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')
        
        conexion.commit()
        conexion.close()
    
    def generarIDVenta(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # Sin microsegundos completos
        return f"V{timestamp}"
    
    def procesar_venta(self, carrito, empleado="Admin", metodo_pago="efectivo"):
        """
        Procesar una venta completa
        
        Args:
            carrito (list): Lista de productos en el carrito
            empleado (str): Nombre del empleado que procesa la venta
            metodo_pago (str): Método de pago utilizado
            
        Returns:
            tuple: (success, venta_id, mensaje)
        """
        try:
            venta_id = self.generarIDVenta()
            fecha_hora = datetime.now()
            
            # Calcular total
            total = sum(item['total'] for item in carrito)
            
            conexion = self.getConexion()
            cursor = conexion.cursor()
            
            # Insertar venta principal (usando estructura existente)
            cursor.execute('''
                INSERT INTO ventas (id, fecha, empleado_id, total, metodo_pago, estado)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (venta_id, fecha_hora, 1, total, metodo_pago, 'completada'))  # empleado_id = 1 por defecto
            
            # Insertar detalles de venta y actualizar stock
            from models.producto import ProductoModel
            producto_model = ProductoModel()
            
            for item in carrito:
                # Insertar detalle de venta
                cursor.execute('''
                    INSERT INTO venta_detalles 
                    (venta_id, producto_id, producto_nombre, cantidad, precio_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (venta_id, item['id'], item['nombre'], item['cantidad'], 
                      item['precio'], item['total']))
                
                # Actualizar stock del producto
                producto_actual = producto_model.obtenerPorId(item['id'])
                if not producto_actual.empty:
                    nuevo_stock = int(producto_actual.iloc[0]['Stock']) - item['cantidad']
                    producto_model.actualizar(item['id'], {
                        'Stock': nuevo_stock
                    })
            
            conexion.commit()
            conexion.close()
            return True, venta_id, f"Venta {venta_id} procesada exitosamente"
            
        except Exception as e:
            if 'conexion' in locals():
                conexion.rollback()
                conexion.close()
            return False, None, f"Error al procesar venta: {str(e)}"
    
    def obtenerVenta(self, venta_id):
        try:
            # Información principal de la venta
            conexion = self.getConexion()
            venta = pd.read_sql_query('''
                SELECT * FROM ventas WHERE id = ?
            ''', conexion, params=[venta_id])
            
            # Detalles de la venta
            detalles = pd.read_sql_query('''
                SELECT * FROM venta_detalles WHERE venta_id = ?
            ''', conexion, params=[venta_id])
            
            conexion.close()
            return venta, detalles
            
        except Exception as e:
            print(f"Error al obtener venta: {e}")
            return pd.DataFrame(), pd.DataFrame()
    
    def obtenerVentaxDia(self, fecha=None):
        if fecha is None:
            fecha = datetime.now().date()
        
        try:
            conexion = self.getConexion()
            ventas = pd.read_sql_query('''
                SELECT v.*, COUNT(vd.id) as items_vendidos
                FROM ventas v
                LEFT JOIN venta_detalles vd ON v.id = vd.venta_id
                WHERE DATE(v.fecha) = ?
                GROUP BY v.id
                ORDER BY v.fecha DESC
            ''', conexion, params=[fecha])
            
            conexion.close()
            return ventas
            
        except Exception as e:
            print(f"Error al obtener ventas del día: {e}")
            return pd.DataFrame()
    
    def obtenerResumenDia(self, fecha=None):
        if fecha is None:
            fecha = datetime.now().date()
        
        try:
            conexion = self.getConexion()
            cursor = conexion.cursor()
            
            # Total de ventas
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_ventas,
                    COALESCE(SUM(total), 0) as monto_total,
                    COALESCE(AVG(total), 0) as venta_promedio
                FROM ventas 
                WHERE DATE(fecha) = ?
            ''', [fecha])
            
            resumen = cursor.fetchone()
            conexion.close()
            
            return {
                'fecha': fecha,
                'total_ventas': resumen[0] if resumen else 0,
                'monto_total': resumen[1] if resumen else 0.0,
                'venta_promedio': resumen[2] if resumen else 0.0
            }
            
        except Exception as e:
            print(f"Error al obtener resumen: {e}")
            return {
                'fecha': fecha,
                'total_ventas': 0,
                'monto_total': 0.0,
                'venta_promedio': 0.0
            }
    
    def obtenerProductosMasVendidos(self, limite=10, fecha=None):
        fecha_filtro = ""
        params = [limite]
        
        if fecha:
            fecha_filtro = "WHERE DATE(v.fecha) = ?"
            params.insert(0, fecha)
        
        try:
            conexion = self.getConexion()
            query = f'''
                SELECT 
                    vd.producto_nombre,
                    SUM(vd.cantidad) as total_vendido,
                    SUM(vd.subtotal) as ingresos_totales,
                    COUNT(DISTINCT vd.venta_id) as num_ventas
                FROM venta_detalles vd
                JOIN ventas v ON vd.venta_id = v.id
                {fecha_filtro}
                GROUP BY vd.producto_id, vd.producto_nombre
                ORDER BY total_vendido DESC
                LIMIT ?
            '''
            
            productos = pd.read_sql_query(query, conexion, params=params)
            conexion.close()
            return productos
            
        except Exception as e:
            print(f"Error al obtener productos más vendidos: {e}")
            return pd.DataFrame()
    
    # Alias para compatibilidad con views/ventas.py
    def obtener_resumen_dia(self, fecha=None):
        """Alias para obtenerResumenDia - mantiene compatibilidad"""
        return self.obtenerResumenDia(fecha)
    
    def cerrar_conexion(self):
        pass