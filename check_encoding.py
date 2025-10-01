#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys

def check_employee_encoding():
    try:
        conn = sqlite3.connect('db/minimarket.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, nombre, apellido, usuario FROM empleados')
        rows = cursor.fetchall()
        
        print("Verificando encoding de empleados:")
        print("=" * 50)
        
        for row in rows:
            emp_id, nombre, apellido, usuario = row
            print(f"ID: {emp_id}")
            
            # Verificar cada campo
            try:
                print(f"  Nombre: '{nombre}' (tipo: {type(nombre)})")
                if isinstance(nombre, str):
                    nombre_bytes = nombre.encode('utf-8', 'replace')
                    print(f"    UTF-8 bytes: {nombre_bytes}")
                    
            except Exception as e:
                print(f"    ERROR en nombre: {e}")
            
            try:
                print(f"  Apellido: '{apellido}' (tipo: {type(apellido)})")
                if isinstance(apellido, str):
                    apellido_bytes = apellido.encode('utf-8', 'replace')
                    print(f"    UTF-8 bytes: {apellido_bytes}")
                    
            except Exception as e:
                print(f"    ERROR en apellido: {e}")
            
            try:
                print(f"  Usuario: '{usuario}' (tipo: {type(usuario)})")
                if isinstance(usuario, str):
                    usuario_bytes = usuario.encode('utf-8', 'replace')
                    print(f"    UTF-8 bytes: {usuario_bytes}")
                    
            except Exception as e:
                print(f"    ERROR en usuario: {e}")
            
            print("-" * 30)
        
        conn.close()
        
    except Exception as e:
        print(f"Error general: {e}")

if __name__ == "__main__":
    check_employee_encoding()