## Formularios y componentes reutilizables - PyQt5 Version

import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog, QMessageBox, QInputDialog, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PIL import Image
from config.settings import *
from utils.helpers import *

class ProductoForm(QDialog):    
    def __init__(self, parent, title="Producto", producto_data=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(520, 510)
        self.setModal(True)
        
        self.parent = parent
        self.producto_data = producto_data
        
        self.img_path = ""
        self.entries = {}
        
        self.crearInterfaz()
        if producto_data is not None:
            # Verificar si es pandas Series o dict y tiene datos
            if hasattr(producto_data, 'empty'):
                if not producto_data.empty:
                    self.llenarCampos()
            elif producto_data:  # Para dict u otros tipos
                self.llenarCampos()
    
    def crearInterfaz(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Título
        es_modificar = False
        if self.producto_data is not None:
            if hasattr(self.producto_data, 'empty'):
                es_modificar = not self.producto_data.empty
            else:
                es_modificar = bool(self.producto_data)
        
        titulo = "Modificar Producto" if es_modificar else "Registrar Producto"
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
        main_layout.addWidget(titulo_label)
        
        # Campos de entrada
        campos = [("Nombre", ""), ("Precio", "0"), ("Stock inicial", "0"), ("Stock Mínimo", "0")]
        for label, default in campos:
            campo_layout = QHBoxLayout()
            
            label_widget = QLabel(label + ":")
            label_widget.setFixedWidth(100)
            label_widget.setStyleSheet("font-weight: bold; color: #333;")
            
            entry = QLineEdit()
            entry.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    padding: 8px;
                    font-size: 12px;
                }
                QLineEdit:focus {
                    border: 2px solid #4285F4;
                }
            """)
            
            if self.producto_data is None or self.producto_data.empty:
                entry.setText(default)
            
            self.entries[label] = entry
            
            campo_layout.addWidget(label_widget)
            campo_layout.addWidget(entry)
            
            main_layout.addLayout(campo_layout)
        
        # Categoría
        categoria_layout = QHBoxLayout()
        categoria_label = QLabel("Categoría:")
        categoria_label.setFixedWidth(100)
        categoria_label.setStyleSheet("font-weight: bold; color: #333;")
        
        self.categoria_cb = QComboBox()
        self.categoria_cb.addItems(cargar_categorias())
        self.categoria_cb.setStyleSheet("""
            QComboBox {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                font-size: 12px;
            }
            QComboBox:focus {
                border: 2px solid #4285F4;
            }
        """)
        
        btn_nueva_categoria = QPushButton("Nueva...")
        btn_nueva_categoria.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        btn_nueva_categoria.clicked.connect(self.agregarCategoriasRapido)
        
        categoria_layout.addWidget(categoria_label)
        categoria_layout.addWidget(self.categoria_cb)
        categoria_layout.addWidget(btn_nueva_categoria)
        
        main_layout.addLayout(categoria_layout)
        
        # Tipo de corte
        corte_layout = QHBoxLayout()
        corte_label = QLabel("Tipo de Corte:")
        corte_label.setFixedWidth(100)
        corte_label.setStyleSheet("font-weight: bold; color: #333;")
        
        self.corte_cb = QComboBox()
        tipos_corte = ["", "Entero", "Bistec", "Molida", "Churrasco", "Costilla", 
                      "Filete", "Pechuga", "Pierna", "Alitas", "Trozos", "Otros"]
        self.corte_cb.addItems(tipos_corte)
        self.corte_cb.setStyleSheet("""
            QComboBox {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                font-size: 12px;
            }
            QComboBox:focus {
                border: 2px solid #4285F4;
            }
        """)
        
        corte_layout.addWidget(corte_label)
        corte_layout.addWidget(self.corte_cb)
        
        main_layout.addLayout(corte_layout)
        
        # Imagen
        imagen_layout = QHBoxLayout()
        imagen_label = QLabel("Imagen (opcional):")
        imagen_label.setFixedWidth(130)
        imagen_label.setStyleSheet("font-weight: bold; color: #333;")
        
        btn_seleccionar = QPushButton("Seleccionar")
        btn_seleccionar.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        btn_seleccionar.clicked.connect(self.seleccionarImagen)
        
        self.img_info_label = QLabel("")
        self.img_info_label.setStyleSheet("color: #6c757d; font-size: 11px;")
        
        imagen_layout.addWidget(imagen_label)
        imagen_layout.addWidget(btn_seleccionar)
        imagen_layout.addWidget(self.img_info_label)
        
        main_layout.addLayout(imagen_layout)
        
        # Espaciador
        main_layout.addStretch()
        
        # Botones
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(10)
        
        textoguardar = "💾 Guardar Cambios" if (self.producto_data is not None and not self.producto_data.empty) else "💾 Guardar"
        btnguardar = QPushButton(textoguardar)
        btnguardar.setStyleSheet(f"""
            QPushButton {{
                background-color: {INFO_COLOR};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 12px 20px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #2980b9;
            }}
        """)
        btnguardar.clicked.connect(self.guardar)
        
        btn_cancelar = QPushButton("❌ Cancelar")
        btn_cancelar.setStyleSheet(f"""
            QPushButton {{
                background-color: {ERROR_COLOR};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 12px 20px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #c0392b;
            }}
        """)
        btn_cancelar.clicked.connect(self.reject)
        
        botones_layout.addStretch()
        botones_layout.addWidget(btnguardar)
        botones_layout.addWidget(btn_cancelar)
        botones_layout.addStretch()
        
        main_layout.addLayout(botones_layout)
    
    def llenarCampos(self):
        if self.producto_data is None or self.producto_data.empty:
            return
        
        # Llenar campos de texto
        self.entries["Nombre"].setText(str(self.producto_data.get("Nombre", "")))
        self.entries["Precio"].setText(str(self.producto_data.get("Precio", 0)))
        self.entries["Stock inicial"].setText(str(self.producto_data.get("Stock", 0)))
        self.entries["Stock Mínimo"].setText(str(self.producto_data.get("Stock Mínimo", 0)))
        
        # Establecer categoría y tipo de corte
        categoria = str(self.producto_data.get("Categoría", ""))
        tipo_corte = str(self.producto_data.get("Tipo de Corte", ""))
        
        # Buscar y seleccionar categoría
        categoria_index = self.categoria_cb.findText(categoria)
        if categoria_index >= 0:
            self.categoria_cb.setCurrentIndex(categoria_index)
        
        # Buscar y seleccionar tipo de corte
        corte_index = self.corte_cb.findText(tipo_corte)
        if corte_index >= 0:
            self.corte_cb.setCurrentIndex(corte_index)
        
        # Establecer imagen
        imagen_actual = self.producto_data.get("Imagen", "")
        if imagen_actual and os.path.exists(imagen_actual):
            self.img_path = imagen_actual
            self.img_info_label.setText(os.path.basename(imagen_actual))
    
    def agregarCategoriasRapido(self):
        nueva_categoria, ok = QInputDialog.getText(self, "Nueva Categoría", 
                                                  "Ingrese el nombre de la nueva categoría:")
        
        if ok and nueva_categoria.strip():
            nueva_categoria = nueva_categoria.strip()
            try:
                # Agregar a la base de datos
                from db.database import db
                db.execute_query("INSERT OR IGNORE INTO categorias (nombre, descripcion) VALUES (?, ?)", 
                               (nueva_categoria, f"Categoría {nueva_categoria}"))
                
                # Recargar las categorías en el dropdown
                categorias_actualizadas = cargar_categorias()
                self.categoria_cb.clear()
                self.categoria_cb.addItems(categorias_actualizadas)
                
                # Seleccionar la nueva categoría
                categoria_index = self.categoria_cb.findText(nueva_categoria)
                if categoria_index >= 0:
                    self.categoria_cb.setCurrentIndex(categoria_index)
                
                QMessageBox.information(self, "Éxito", f"Categoría '{nueva_categoria}' agregada correctamente.")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo agregar la categoría: {e}")
    
    def seleccionarImagen(self):
        file_dialog = QFileDialog()
        path, _ = file_dialog.getOpenFileName(self, "Seleccionar imagen", "", 
                                            "Imágenes (*.png *.jpg *.jpeg *.gif *.bmp)")
        if path:
            self.img_path = path
            self.img_info_label.setText(os.path.basename(path))
    
    def validarDatos(self):
        nombre = self.entries["Nombre"].text().strip()
        categoria = self.categoria_cb.currentText().strip()
        
        if not nombre:
            QMessageBox.critical(self, "Error", "El nombre del producto es obligatorio.")
            return None
        
        if not categoria:
            QMessageBox.critical(self, "Error", "Debes seleccionar una categoría del dropdown.")
            return None
        
        # Validar campos numéricos
        precio, precio_valido = validar_numero(self.entries["Precio"].text())
        stock, stock_valido = validar_numero(self.entries["Stock inicial"].text(), "int")
        stock_min, stock_min_valido = validar_numero(self.entries["Stock Mínimo"].text(), "int")
        
        if not precio_valido:
            QMessageBox.critical(self, "Error", "El precio debe ser un número válido.")
            return None
        
        if not stock_valido:
            QMessageBox.critical(self, "Error", "El stock debe ser un número entero válido.")
            return None
        
        if not stock_min_valido:
            QMessageBox.critical(self, "Error", "El stock mínimo debe ser un número entero válido.")
            return None
        
        return {
            "Nombre": nombre,
            "Categoría": categoria,
            "Tipo de Corte": self.corte_cb.currentText().strip(),
            "Precio": precio,
            "Stock": stock,
            "Stock Mínimo": stock_min,
            "imagen_origen": self.img_path if self.img_path else None
        }

    def guardar(self):
        raise NotImplementedError("Debe implementarse en la clase hija")

class ImagenViewer(QLabel):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #ccc;
                border-radius: 8px;
                background-color: #f8f9fa;
                min-height: 200px;
                max-height: 200px;
                margin: 10px;
            }
        """)
        self.imagen_actual = None
    
    def mostrarImagen(self, ruta_imagen, tamaño=(200, 200)):
        try:
            # Limpiar imagen anterior primero
            self.limpiar()
            
            if ruta_imagen and os.path.exists(ruta_imagen):
                pixmap = QPixmap(ruta_imagen)
                scaled_pixmap = pixmap.scaled(tamaño[0], tamaño[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.setPixmap(scaled_pixmap)
                self.imagen_actual = scaled_pixmap
            else:
                self.limpiar()
        except Exception as e:
            # Solo imprimir si es un error real, no de imagen que no existe
            if "doesn't exist" not in str(e):
                print(f"Error al cargar imagen: {e}")
            self.limpiar()
    
    def limpiar(self):
        self.clear()
        self.setText("📷 Vista previa de imagen")
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #ccc;
                border-radius: 8px;
                background-color: #f8f9fa;
                min-height: 200px;
                max-height: 200px;
                margin: 10px;
                color: #6c757d;
                font-size: 14px;
            }
        """)
        self.imagen_actual = None