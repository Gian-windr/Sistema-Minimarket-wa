## Modelo base con funciones CRUD para SQLite

import sqlite3
from datetime import datetime
from db.database import db

class BaseModel: # Clase base para modelos CRUD
    
    def __init__(self, table_name, columns):
        self.table_name = table_name
        self.columns = columns
    
    def get_all(self, where_clause=None, params=None):
        query = f"SELECT * FROM {self.table_name}"
        if where_clause:
            query += f" WHERE {where_clause}"
        
        conn = db.get_connection()
        conn.row_factory = sqlite3.Row  # Para acceder por nombre de columna
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        rows = cursor.fetchall()
        conn.close()
        
        # Convertir a lista de diccionarios
        return [dict(row) for row in rows]
    
    def obtenerRegistro(self, record_id, id_column='id'): 
        query = f"SELECT * FROM {self.table_name} WHERE {id_column} = ?"
        
        conn = db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, (record_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def crearRegistro(self, data): 
        # Filtrar solo las columnas válidas
        valid_data = {k: v for k, v in data.items() if k in self.columns}
        
        if not valid_data:
            raise ValueError("No hay datos válidos para insertar")
        
        columns = ', '.join(valid_data.keys())
        placeholders = ', '.join(['?' for _ in valid_data])
        values = list(valid_data.values())
        
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, values)
        
        last_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return last_id
    
    def actualizarRegistroID(self, record_id, data, id_column='id'): 
        # Filtrar solo las columnas válidas
        valid_data = {k: v for k, v in data.items() if k in self.columns and k != id_column}
        
        if not valid_data:
            raise ValueError("No hay datos válidos para actualizar")
        
        # Procesar valores para manejar caracteres especiales
        processed_data = {}
        for k, v in valid_data.items():
            if isinstance(v, str):
                # Normalizar caracteres especiales y asegurar codificación correcta
                import unicodedata
                try:
                    # Normalizar y convertir a UTF-8
                    normalized_value = unicodedata.normalize('NFC', v)
                    processed_data[k] = normalized_value
                except (UnicodeError, UnicodeEncodeError):
                    # Si hay problemas, usar el valor original
                    processed_data[k] = v
            else:
                processed_data[k] = v
        
        # Agregar fecha de actualización si existe la columna
        if 'fecha_actualizacion' in self.columns:
            processed_data['fecha_actualizacion'] = datetime.now().isoformat()
        
        set_clause = ', '.join([f"{k} = ?" for k in processed_data.keys()])
        values = list(processed_data.values()) + [record_id]
        
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {id_column} = ?"
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, values)
            rows_affected = cursor.rowcount
            conn.commit()
            return rows_affected > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def eliminarRegistroID(self, record_id, id_column='id'):
        query = f"DELETE FROM {self.table_name} WHERE {id_column} = ?"
        
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (record_id,))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0
    
    def buscarRegistro(self, search_term, search_columns):
        if not search_term.strip():
            return self.get_all()
        
        search_term = f"%{search_term.lower()}%"
        conditions = []
        params = []
        
        for column in search_columns:
            conditions.append(f"LOWER({column}) LIKE ?")
            params.append(search_term)
        
        where_clause = " OR ".join(conditions)
        
        return self.get_all(where_clause, params)
    
    def contarRegistro(self, where_clause=None, params=None):
        query = f"SELECT COUNT(*) FROM {self.table_name}"
        if where_clause:
            query += f" WHERE {where_clause}"
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def vericarRegistroID(self, record_id, id_column='id'):
        return self.contarRegistro(f"{id_column} = ?", (record_id,)) > 0
    
    def consultaPersonalizada(self, query, params=None):
        conn = db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]