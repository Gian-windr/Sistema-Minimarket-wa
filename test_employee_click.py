#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.empleado import EmpleadoModel

def test_employee_password_click():
    """Simular el proceso que ocurre cuando se hace clic en el botón de contraseña"""
    
    print("Iniciando prueba de clic en botón de contraseña...")
    print("=" * 60)
    
    empleado_model = EmpleadoModel()
    
    # Obtener todos los empleados para probar
    try:
        empleados = empleado_model.get_all()
        print(f"Empleados encontrados: {len(empleados)}")
        
        for empleado in empleados:
            emp_id = empleado.get('id')
            print(f"\nProbando empleado ID: {emp_id}")
            
            try:
                # Simular el proceso de cambiar_contraseña
                empleado_data = empleado_model.get_by_id(emp_id)
                
                if empleado_data:
                    print(f"  Datos obtenidos: {empleado_data}")
                    
                    # Simular la verificación de encoding que hacemos en la UI
                    try:
                        usuario = str(empleado_data.get('usuario', ''))
                        nombre = str(empleado_data.get('nombre', ''))
                        apellido = str(empleado_data.get('apellido', ''))
                        
                        print(f"  Usuario: '{usuario}' (tipo: {type(usuario)})")
                        print(f"  Nombre: '{nombre}' (tipo: {type(nombre)})")
                        print(f"  Apellido: '{apellido}' (tipo: {type(apellido)})")
                        
                        # Simular la creación del texto del QLabel
                        info_text = f"Usuario: {usuario}\nNombre: {nombre} {apellido}"
                        print(f"  Texto del label: '{info_text}'")
                        
                        # Simular el encoding/decoding que hacemos
                        usuario_encoded = usuario.encode('utf-8', 'replace').decode('utf-8')
                        nombre_encoded = nombre.encode('utf-8', 'replace').decode('utf-8')
                        apellido_encoded = apellido.encode('utf-8', 'replace').decode('utf-8')
                        
                        print(f"  Después de encoding: Usuario='{usuario_encoded}', Nombre='{nombre_encoded}', Apellido='{apellido_encoded}'")
                        
                    except Exception as encoding_error:
                        print(f"  ERROR DE ENCODING: {encoding_error}")
                        print(f"  Tipo de error: {type(encoding_error)}")
                        
                else:
                    print(f"  No se encontraron datos para el empleado ID: {emp_id}")
                    
            except Exception as e:
                print(f"  ERROR GENERAL: {e}")
                print(f"  Tipo de error: {type(e)}")
                
    except Exception as e:
        print(f"Error obteniendo empleados: {e}")

if __name__ == "__main__":
    test_employee_password_click()