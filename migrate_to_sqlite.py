## Script de migración de Excel a SQLite

import pandas as pd
import os
import sqlite3
from datetime import datetime
from config.settings import *
from db.database import db

def migrate_excel_to_sqlite():
    """Migra todos los datos de Excel a SQLite"""
    print("🔄 Iniciando migración de Excel a SQLite...")
    
    try:
        # Migrar productos
        migrate_productos()
        
        # Migrar categorías (si existe el archivo)
        migrate_categorias()
        
        # Migrar empleados
        migrate_empleados()
        
        # Migrar ventas (si existe el archivo)
        migrate_ventas()
        
        # Migrar compras (si existe el archivo)
        migrate_compras()
        
        # Migrar despachos (si existe el archivo)
        migrate_despachos()
        
        print("✅ Migración completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        raise

def migrate_productos():
    """Migra productos de Excel a SQLite"""
    if not os.path.exists(PRODUCTOS_FILE):
        print("⚠️  Archivo productos.xlsx no encontrado")
        return
    
    print("📦 Migrando productos...")
    
    try:
        df = pd.read_excel(PRODUCTOS_FILE)
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        for _, row in df.iterrows():
            # Mapear columnas de Excel a SQLite
            producto_data = {
                'id': str(row.get('ID', '')),
                'nombre': str(row.get('Nombre', '')),
                'categoria': str(row.get('Categoría', '')),
                'tipo_corte': str(row.get('Tipo de Corte', '')),
                'precio': float(row.get('Precio', 0)),
                'stock': int(row.get('Stock', 0)),
                'stock_minimo': int(row.get('Stock Mínimo', 0)),
                'imagen': str(row.get('Imagen', ''))
            }
            
            # Insertar producto
            cursor.execute('''
                INSERT OR REPLACE INTO productos 
                (id, nombre, categoria, tipo_corte, precio, stock, stock_minimo, imagen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                producto_data['id'],
                producto_data['nombre'],
                producto_data['categoria'],
                producto_data['tipo_corte'],
                producto_data['precio'],
                producto_data['stock'],
                producto_data['stock_minimo'],
                producto_data['imagen']
            ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ {len(df)} productos migrados")
        
    except Exception as e:
        print(f"❌ Error migrando productos: {e}")

def migrate_categorias():
    """Migra categorías de Excel a SQLite"""
    if not os.path.exists(CATEGORIAS_FILE):
        print("⚠️  Archivo categorias.xlsx no encontrado")
        return
    
    print("📂 Migrando categorías...")
    
    try:
        df = pd.read_excel(CATEGORIAS_FILE)
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT OR IGNORE INTO categorias (nombre, descripcion)
                VALUES (?, ?)
            ''', (
                str(row.get('Nombre', '')),
                str(row.get('Descripción', ''))
            ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ {len(df)} categorías migradas")
        
    except Exception as e:
        print(f"❌ Error migrando categorías: {e}")

def migrate_empleados():
    """Migra empleados de Excel a SQLite"""
    if not os.path.exists(EMPLEADOS_FILE):
        print("⚠️  Archivo empleados.xlsx no encontrado")
        return
    
    print("👥 Migrando empleados...")
    
    try:
        df = pd.read_excel(EMPLEADOS_FILE)
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT OR REPLACE INTO empleados 
                (nombre, apellido, usuario, contraseña, rol, activo)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                str(row.get('Nombre', '')),
                str(row.get('Apellido', '')),
                str(row.get('Usuario', '')),
                str(row.get('Contraseña', '')),
                str(row.get('Rol', 'empleado')),
                1 if row.get('Activo', True) else 0
            ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ {len(df)} empleados migrados")
        
    except Exception as e:
        print(f"❌ Error migrando empleados: {e}")

def migrate_ventas():
    """Migra ventas de Excel a SQLite"""
    ventas_file = os.path.join(DB_DIR, "ventas.xlsx")
    if not os.path.exists(ventas_file):
        print("⚠️  Archivo ventas.xlsx no encontrado")
        return
    
    print("💰 Migrando ventas...")
    
    try:
        df = pd.read_excel(ventas_file)
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT OR REPLACE INTO ventas 
                (id, fecha, total, metodo_pago, estado)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                str(row.get('ID', '')),
                str(row.get('Fecha', datetime.now().isoformat())),
                float(row.get('Total', 0)),
                str(row.get('Método de Pago', '')),
                str(row.get('Estado', 'completada'))
            ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ {len(df)} ventas migradas")
        
    except Exception as e:
        print(f"❌ Error migrando ventas: {e}")

def migrate_compras():
    """Migra compras de Excel a SQLite"""
    compras_file = os.path.join(DB_DIR, "compras.xlsx")
    if not os.path.exists(compras_file):
        print("⚠️  Archivo compras.xlsx no encontrado")
        return
    
    print("🛒 Migrando compras...")
    
    try:
        df = pd.read_excel(compras_file)
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT OR REPLACE INTO compras 
                (id, fecha, proveedor, total, estado)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                str(row.get('ID', '')),
                str(row.get('Fecha', datetime.now().isoformat())),
                str(row.get('Proveedor', '')),
                float(row.get('Total', 0)),
                str(row.get('Estado', 'completada'))
            ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ {len(df)} compras migradas")
        
    except Exception as e:
        print(f"❌ Error migrando compras: {e}")

def migrate_despachos():
    """Migra despachos de Excel a SQLite"""
    despachos_file = os.path.join(DB_DIR, "despachos.xlsx")
    if not os.path.exists(despachos_file):
        print("⚠️  Archivo despachos.xlsx no encontrado")
        return
    
    print("🚚 Migrando despachos...")
    
    try:
        df = pd.read_excel(despachos_file)
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT OR REPLACE INTO despachos 
                (id, fecha, destino, estado, observaciones)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                str(row.get('ID', '')),
                str(row.get('Fecha', datetime.now().isoformat())),
                str(row.get('Destino', '')),
                str(row.get('Estado', 'pendiente')),
                str(row.get('Observaciones', ''))
            ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ {len(df)} despachos migrados")
        
    except Exception as e:
        print(f"❌ Error migrando despachos: {e}")

def backup_excel_files():
    """Crea un respaldo de los archivos Excel antes de la migración"""
    backup_dir = os.path.join(DB_DIR, "backup_excel")
    os.makedirs(backup_dir, exist_ok=True)
    
    excel_files = [
        PRODUCTOS_FILE,
        CATEGORIAS_FILE,
        EMPLEADOS_FILE,
        os.path.join(DB_DIR, "ventas.xlsx"),
        os.path.join(DB_DIR, "compras.xlsx"),
        os.path.join(DB_DIR, "despachos.xlsx")
    ]
    
    for file_path in excel_files:
        if os.path.exists(file_path):
            filename = os.path.basename(file_path)
            backup_path = os.path.join(backup_dir, f"backup_{filename}")
            
            import shutil
            shutil.copy2(file_path, backup_path)
            print(f"📋 Respaldo creado: {backup_path}")

if __name__ == "__main__":
    print("🔄 Iniciando proceso de migración...")
    
    # Crear respaldo de archivos Excel
    backup_excel_files()
    
    # Ejecutar migración
    migrate_excel_to_sqlite()
    
    print("🎉 Proceso de migración completado")