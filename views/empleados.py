
# -*- coding: utf-8 -*-
## Vista para gestión de empleados

import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QAbstractItemView,
                             QDialog, QLineEdit, QComboBox, QFormLayout,
                             QDialogButtonBox, QGroupBox, QCheckBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from models.empleado import EmpleadoModel
from views.settings import *

class EmpleadosWidget(QWidget):
    def __init__(self, usuario_rol='empleado'):
        super().__init__()
        self.empleado_model = EmpleadoModel()
        self.usuario_rol = usuario_rol
        self.init_ui()
        self.cargar_empleados()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Título
        titulo = QLabel("👥 Gestión de Empleados")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet(f"""
            QLabel {{
                color: {THEME_COLOR};
                font-size: 24px;
                font-weight: bold;
                font-family: Arial;
                margin-bottom: 20px;
            }}
        """)
        layout.addWidget(titulo)
        
        # Botón para crear empleado (solo para admin)
        if self.usuario_rol == 'admin':
            btn_crear = QPushButton("➕ Crear Empleado")
            btn_crear.setStyleSheet(f"""
                QPushButton {{
                    background-color: {THEME_COLOR};
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 14px;
                    margin-bottom: 15px;
                }}
                QPushButton:hover {{
                    background-color: {THEME_COLOR_HOVER};
                }}
            """)
            btn_crear.clicked.connect(self.crear_empleado)
            layout.addWidget(btn_crear)
        
        # Tabla de empleados
        self.tabla_empleados = QTableWidget()
        self.tabla_empleados.setColumnCount(7)
        self.tabla_empleados.setHorizontalHeaderLabels([
            "ID", "Nombre", "Apellido", "Usuario", "Rol", "Estado", "Acciones"
        ])
        
        # Configurar tabla
        header = self.tabla_empleados.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Interactive)
        
        # Ajustar anchos de columnas
        self.tabla_empleados.setColumnWidth(0, 50)   # ID
        self.tabla_empleados.setColumnWidth(1, 120)  # Nombre
        self.tabla_empleados.setColumnWidth(2, 120)  # Apellido
        self.tabla_empleados.setColumnWidth(3, 100)  # Usuario
        self.tabla_empleados.setColumnWidth(4, 80)   # Rol
        self.tabla_empleados.setColumnWidth(5, 80)   # Estado
        self.tabla_empleados.setColumnWidth(6, 280)  # Acciones
        
        self.tabla_empleados.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_empleados.setAlternatingRowColors(True)
        self.tabla_empleados.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                background-color: white;
                alternate-background-color: #f8f9fa;
                selection-background-color: #e3f2fd;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #ddd;
                font-weight: bold;
                color: #333;
            }
        """)
        
        layout.addWidget(self.tabla_empleados)
    
    def cargar_empleados(self):
        try:
            empleados = self.empleado_model.obtenerEmpleadosActivos()
            self.tabla_empleados.setRowCount(len(empleados))
            
            for row, empleado in enumerate(empleados):
                # ID
                self.tabla_empleados.setItem(row, 0, QTableWidgetItem(str(empleado['id'])))
                
                # Nombre
                self.tabla_empleados.setItem(row, 1, QTableWidgetItem(empleado['nombre']))
                
                # Apellido
                self.tabla_empleados.setItem(row, 2, QTableWidgetItem(empleado['apellido']))
                
                # Usuario
                self.tabla_empleados.setItem(row, 3, QTableWidgetItem(empleado['usuario']))
                
                # Rol
                rol_item = QTableWidgetItem(empleado['rol'].title())
                if empleado['rol'] == 'admin':
                    rol_item.setForeground(Qt.red)
                    rol_item.setFont(QFont("Arial", 9, QFont.Bold))
                else:
                    rol_item.setForeground(Qt.darkGreen)
                    rol_item.setFont(QFont("Arial", 9, QFont.Bold))
                self.tabla_empleados.setItem(row, 4, rol_item)
                
                # Estado
                estado_item = QTableWidgetItem("Activo" if empleado['activo'] else "Inactivo")
                if empleado['activo']:
                    estado_item.setForeground(Qt.darkGreen)
                    estado_item.setFont(QFont("Arial", 9, QFont.Bold))
                else:
                    estado_item.setForeground(Qt.red)
                    estado_item.setFont(QFont("Arial", 9, QFont.Bold))
                self.tabla_empleados.setItem(row, 5, estado_item)
                
                # Botones de acción
                btn_widget = QWidget()
                btn_layout = QHBoxLayout(btn_widget)
                btn_layout.setContentsMargins(5, 2, 5, 2)
                btn_layout.setSpacing(5)
                
                # Botón Editar
                btn_editar = QPushButton("✏️ Editar")
                btn_editar.setToolTip("Editar empleado")
                btn_editar.setFixedHeight(28)
                btn_editar.setMinimumWidth(80)
                btn_editar.setStyleSheet("""
                    QPushButton {
                        background-color: #f39c12;
                        color: white;
                        border: none;
                        padding: 4px 8px;
                        border-radius: 4px;
                        font-weight: bold;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #e67e22;
                    }
                """)
                btn_editar.clicked.connect(lambda checked, emp_id=empleado['id']: self.editar_empleado(emp_id))
                
                # Botón Cambiar Contraseña
                btn_password = QPushButton("🔑 Contraseña")
                btn_password.setToolTip("Cambiar contraseña")
                btn_password.setFixedHeight(28)
                btn_password.setMinimumWidth(100)
                btn_password.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        border: none;
                        padding: 4px 8px;
                        border-radius: 4px;
                        font-weight: bold;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                """)
                btn_password.clicked.connect(lambda checked, emp_id=empleado['id']: self.cambiar_contraseña(emp_id))
                
                # Botón Desactivar
                btn_desactivar = QPushButton("🚫 Desactivar")
                btn_desactivar.setToolTip("Desactivar empleado")
                btn_desactivar.setFixedHeight(28)
                btn_desactivar.setMinimumWidth(90)
                btn_desactivar.setStyleSheet("""
                    QPushButton {
                        background-color: #e74c3c;
                        color: white;
                        border: none;
                        padding: 4px 8px;
                        border-radius: 4px;
                        font-weight: bold;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #c0392b;
                    }
                """)
                btn_desactivar.clicked.connect(lambda checked, emp_id=empleado['id']: self.desactivar_empleado(emp_id))
                
                btn_layout.addWidget(btn_editar)
                btn_layout.addWidget(btn_password)
                btn_layout.addWidget(btn_desactivar)
                btn_layout.addStretch()
                
                self.tabla_empleados.setCellWidget(row, 6, btn_widget)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar empleados: {str(e)}")
    
    def crear_empleado(self):
        dialog = CrearEmpleadoDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.cargar_empleados()
    
    def editar_empleado(self, empleado_id):
        try:
            empleado = self.empleado_model.get_by_id(empleado_id)
            if empleado:
                dialog = CrearEmpleadoDialog(self, empleado)
                if dialog.exec_() == QDialog.Accepted:
                    self.cargar_empleados()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al editar empleado: {str(e)}")
    
    def desactivar_empleado(self, empleado_id):
        try:
            reply = QMessageBox.question(
                self, 
                "Confirmar", 
                "¿Está seguro de que desea desactivar este empleado?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                if self.empleado_model.desactivarEmpleado(empleado_id):
                    QMessageBox.information(self, "Éxito", "Empleado desactivado correctamente.")
                    self.cargar_empleados()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo desactivar el empleado.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al desactivar empleado: {str(e)}")
    
    def cambiar_contraseña(self, empleado_id):
        try:
            empleado = self.empleado_model.get_by_id(empleado_id)
            if empleado:
                # Verificar que los datos del empleado no tengan problemas de encoding
                try:
                    # Intentar acceder a los campos para detectar problemas de encoding temprano
                    _ = str(empleado.get('usuario', ''))
                    _ = str(empleado.get('nombre', ''))
                    _ = str(empleado.get('apellido', ''))
                except (UnicodeError, UnicodeEncodeError, UnicodeDecodeError):
                    QMessageBox.critical(self, "Error de Codificación", 
                                       "Los datos del empleado contienen caracteres especiales que no se pueden procesar.\n"
                                       "Contacte al administrador del sistema.")
                    return
                
                dialog = CambiarContrasenaDialog(self, empleado)
                if dialog.exec_() == QDialog.Accepted:
                    QMessageBox.information(self, "Éxito", "Contraseña cambiada correctamente.")
        except Exception as e:
            error_msg = str(e)
            if 'ascii' in error_msg.lower() or 'encode' in error_msg.lower() or 'unicode' in error_msg.lower():
                QMessageBox.critical(self, "Error de Codificación", 
                                   "Error de codificación al procesar los datos del empleado.\n"
                                   "Esto puede deberse a caracteres especiales en el nombre o usuario.\n"
                                   "Contacte al administrador del sistema.")
            else:
                QMessageBox.critical(self, "Error", f"Error al cambiar contraseña: {error_msg}")


class CambiarContrasenaDialog(QDialog):
    def __init__(self, parent=None, empleado=None):
        super().__init__(parent)
        self.empleado = empleado
        self.empleado_model = EmpleadoModel()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Cambiar Contraseña")
        self.setFixedSize(400, 250)
        self.setModal(True)
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Título
        titulo = QLabel("🔑 Cambiar Contraseña")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 18px;
                font-weight: bold;
                font-family: Arial;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(titulo)
        
        # Información del empleado
        try:
            # Manejar caracteres especiales en los datos del empleado
            usuario = str(self.empleado.get('usuario', '')).encode('utf-8', 'replace').decode('utf-8')
            nombre = str(self.empleado.get('nombre', '')).encode('utf-8', 'replace').decode('utf-8')
            apellido = str(self.empleado.get('apellido', '')).encode('utf-8', 'replace').decode('utf-8')
            
            info_text = f"Usuario: {usuario}\nNombre: {nombre} {apellido}"
            info_empleado = QLabel(info_text)
        except (UnicodeError, UnicodeEncodeError, UnicodeDecodeError) as e:
            # Si hay problemas de encoding, usar información básica
            info_empleado = QLabel("Usuario: [Error de codificación]\nNombre: [Error de codificación]")
        except Exception as e:
            # Fallback para cualquier otro error
            info_empleado = QLabel("Información del empleado no disponible")
            
        info_empleado.setAlignment(Qt.AlignCenter)
        info_empleado.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 14px;
                margin-bottom: 15px;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 5px;
            }
        """)
        layout.addWidget(info_empleado)
        
        # Campo nueva contraseña
        password_layout = QHBoxLayout()
        password_label = QLabel("Nueva Contraseña:")
        password_label.setFixedWidth(120)
        password_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #333;
                font-size: 14px;
            }
        """)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #4285F4;
            }
        """)
        
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)
        
        # Campo confirmar contraseña
        confirm_layout = QHBoxLayout()
        confirm_label = QLabel("Confirmar:")
        confirm_label.setFixedWidth(120)
        confirm_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #333;
                font-size: 14px;
            }
        """)
        
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #4285F4;
            }
        """)
        
        confirm_layout.addWidget(confirm_label)
        confirm_layout.addWidget(self.confirm_input)
        layout.addLayout(confirm_layout)
        
        # Botones
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        btn_cancelar.clicked.connect(self.reject)
        
        btn_guardar = QPushButton("Cambiar")
        btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        btn_guardar.clicked.connect(self.cambiar_contraseña)
        
        button_layout.addWidget(btn_cancelar)
        button_layout.addWidget(btn_guardar)
        layout.addLayout(button_layout)
        
        # Focus en el primer campo
        self.password_input.setFocus()
    
    def cambiar_contraseña(self):
        nueva_password = self.password_input.text().strip()
        confirmar_password = self.confirm_input.text().strip()
        
        # Validaciones
        if not nueva_password:
            QMessageBox.warning(self, "Error", "La contraseña no puede estar vacía.")
            return
        
        if len(nueva_password) < 4:
            QMessageBox.warning(self, "Error", "La contraseña debe tener al menos 4 caracteres.")
            return
        
        if nueva_password != confirmar_password:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden.")
            return
        
        try:
            # Actualizar contraseña en la base de datos
            # El procesamiento de caracteres especiales se maneja en el modelo base
            if self.empleado_model.actualizarEmpleado(self.empleado['id'], {'contraseña': nueva_password}):
                QMessageBox.information(self, "Éxito", "Contraseña actualizada correctamente.")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "No se pudo actualizar la contraseña.")
        except Exception as e:
            error_msg = str(e)
            if 'ascii' in error_msg.lower() or 'encode' in error_msg.lower():
                QMessageBox.critical(self, "Error de Codificación", 
                                   "Error al procesar caracteres especiales en la contraseña.\n"
                                   "Intente usar una contraseña sin caracteres especiales como ñ, á, é, etc.")
            else:
                QMessageBox.critical(self, "Error", f"Error al cambiar contraseña: {error_msg}")


class CrearEmpleadoDialog(QDialog):
    def __init__(self, parent=None, empleado_data=None):
        super().__init__(parent)
        self.empleado_model = EmpleadoModel()
        self.empleado_data = empleado_data
        self.es_edicion = empleado_data is not None
        
        self.setWindowTitle("Editar Empleado" if self.es_edicion else "Crear Nuevo Empleado")
        self.setModal(True)
        self.setFixedSize(520, 450)
        
        self.crear_interfaz()
        
        if self.es_edicion:
            self.cargar_datos_empleado()
    
    def crear_interfaz(self):
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Título
        titulo = "Modificar Empleado" if self.es_edicion else "Registrar Empleado"
        titulo_label = QLabel(titulo)
        titulo_label.setAlignment(Qt.AlignCenter)
        titulo_label.setStyleSheet(f"""
            QLabel {{
                color: {THEME_COLOR};
                font-size: 18px;
                font-weight: bold;
                font-family: Arial;
                margin-bottom: 10px;
            }}
        """)
        layout.addWidget(titulo_label)
        
        # Campos de entrada
        campos = [("Nombre", ""), ("Apellido", ""), ("Usuario", ""), ("Contraseña", "")]
        self.entries = {}
        
        for label, default in campos:
            campo_layout = QHBoxLayout()
            
            # Label
            label_widget = QLabel(f"{label}:")
            label_widget.setFixedWidth(100)
            label_widget.setStyleSheet(self.get_label_style())
            
            # Input
            if label == "Contraseña":
                input_widget = QLineEdit()
                input_widget.setEchoMode(QLineEdit.Password)
            else:
                input_widget = QLineEdit()
            
            input_widget.setStyleSheet(self.get_input_style())
            input_widget.setText(default)
            
            self.entries[label] = input_widget
            
            campo_layout.addWidget(label_widget)
            campo_layout.addWidget(input_widget)
            layout.addLayout(campo_layout)
        
        # Campo de rol
        rol_layout = QHBoxLayout()
        rol_label = QLabel("Rol:")
        rol_label.setFixedWidth(100)
        rol_label.setStyleSheet(self.get_label_style())
        
        self.rol_combo = QComboBox()
        self.rol_combo.addItems(["empleado", "admin"])
        self.rol_combo.setStyleSheet(self.get_input_style())
        
        rol_layout.addWidget(rol_label)
        rol_layout.addWidget(self.rol_combo)
        layout.addLayout(rol_layout)
        
        # Guardar referencia al campo de contraseña
        self.password_input = self.entries["Contraseña"]
        
        # Botones
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        btn_cancelar.clicked.connect(self.reject)
        
        btn_guardar = QPushButton("Actualizar" if self.es_edicion else "Crear")
        btn_guardar.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME_COLOR};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {THEME_COLOR_HOVER};
            }}
        """)
        btn_guardar.clicked.connect(self.guardar_empleado)
        
        button_layout.addWidget(btn_cancelar)
        button_layout.addWidget(btn_guardar)
        layout.addLayout(button_layout)
    
    def get_input_style(self):
        return """
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #4285F4;
            }
        """
    
    def get_label_style(self):
        return """
            QLabel {
                font-weight: bold;
                color: #333;
                font-size: 14px;
            }
        """
    
    def cargar_datos_empleado(self):
        if self.empleado_data:
            self.entries["Nombre"].setText(self.empleado_data.get('nombre', ''))
            self.entries["Apellido"].setText(self.empleado_data.get('apellido', ''))
            self.entries["Usuario"].setText(self.empleado_data.get('usuario', ''))
            self.password_input.setText("")  # No mostrar contraseña por seguridad
            
            # Configurar rol
            rol_actual = self.empleado_data.get('rol', 'empleado')
            index = self.rol_combo.findText(rol_actual)
            if index >= 0:
                self.rol_combo.setCurrentIndex(index)
    
    def validar_datos(self):
        # Validar campos obligatorios
        for campo, entry in self.entries.items():
            if not entry.text().strip():
                if campo == "Contraseña" and self.es_edicion:
                    continue  # En edición, la contraseña es opcional
                QMessageBox.warning(self, "Error", f"El campo {campo} es obligatorio.")
                entry.setFocus()
                return False
        
        # Validar contraseña solo si es nuevo empleado o se está cambiando
        password = self.password_input.text().strip()
        if not self.es_edicion and not password:
            QMessageBox.warning(self, "Error", "La contraseña es obligatoria para nuevos usuarios.")
            self.password_input.setFocus()
            return False
        
        # Si hay contraseña, validar longitud
        if password and len(password) < 4:
            QMessageBox.warning(self, "Error", "La contraseña debe tener al menos 4 caracteres.")
            self.password_input.setFocus()
            return False
        
        return True
    
    def guardar_empleado(self):
        if not self.validar_datos():
            return
        
        try:
            nombre = self.entries["Nombre"].text().strip()
            apellido = self.entries["Apellido"].text().strip()
            usuario = self.entries["Usuario"].text().strip()
            password = self.password_input.text().strip()
            rol = self.rol_combo.currentText()
            
            if self.es_edicion:
                # Actualizar empleado existente
                datos_actualizacion = {
                    'nombre': nombre,
                    'apellido': apellido,
                    'usuario': usuario,
                    'rol': rol
                }
                
                # Solo actualizar contraseña si se proporcionó una nueva
                if password:
                    datos_actualizacion['contraseña'] = password
                
                if self.empleado_model.actualizarEmpleado(self.empleado_data['id'], datos_actualizacion):
                    QMessageBox.information(self, "Éxito", "Empleado actualizado correctamente.")
                    self.accept()
                else:
                    QMessageBox.critical(self, "Error", "No se pudo actualizar el empleado.")
            else:
                # Crear nuevo empleado
                if self.empleado_model.crear_empleado(nombre, apellido, usuario, password, rol):
                    QMessageBox.information(self, "Éxito", "Empleado creado correctamente.")
                    self.accept()
                else:
                    QMessageBox.critical(self, "Error", "No se pudo crear el empleado.")
                    
        except ValueError as ve:
            QMessageBox.warning(self, "Error", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")