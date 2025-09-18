## Vista del módulo de inventario - PyQt5 Version

import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QAbstractItemView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import pandas as pd
from PIL import Image
from models.producto import ProductoModel
from views.components.forms import ProductoForm, ImagenViewer
from utils.helpers import formatear_precio
from config.settings import *

class InventarioFrame(QWidget):      
    def __init__(self, parent):
        super().__init__(parent)
        
        self.producto_model = ProductoModel()
        self._crear_interfaz()
        self.mostrar_inventario()
    
    def _crear_interfaz(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Título
        titulo = QLabel("Inventario")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet(f"""
            QLabel {{
                color: {THEME_COLOR};
                font-size: 22px;
                font-weight: bold;
                font-family: Arial;
                margin-bottom: 10px;
            }}
        """)
        main_layout.addWidget(titulo)
        
        # Tabla de productos
        self.tabla = QTableWidget()
        self.tabla.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                selection-background-color: #d6eaf8;
                alternate-background-color: #f8f9fa;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                padding: 8px;
                font-weight: bold;
                font-size: 12px;
            }
        """)
        
        # Configurar tabla
        columnas = ["ID", "Nombre", "Categoría", "Tipo de Corte", "Precio", "Stock", "Stock Mínimo", "Imagen"]
        self.tabla.setColumnCount(len(columnas))
        self.tabla.setHorizontalHeaderLabels(columnas)
        
        # Configurar selección
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabla.setAlternatingRowColors(True)
        
        # Ajustar tamaños de columna
        header = self.tabla.horizontalHeader()
        header.setStretchLastSection(False)
        
        # Configurar anchos específicos
        anchos = [80, 180, 120, 130, 80, 80, 100, 110]
        for i, ancho in enumerate(anchos):
            self.tabla.setColumnWidth(i, ancho)
        
        # Conectar señal de selección
        self.tabla.itemSelectionChanged.connect(self._mostrar_imagen_producto)
        
        main_layout.addWidget(self.tabla)
        
        # Botones de acción
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(10)
        
        # Crear botones
        btn_agregar = self._crear_boton("➕ Agregar Producto", SUCCESS_COLOR, self._agregar_producto)
        btn_modificar = self._crear_boton("✏️ Modificar Producto", INFO_COLOR, self._modificar_producto)
        btn_eliminar = self._crear_boton("🗑️ Eliminar Producto", ERROR_COLOR, self._eliminar_producto)
        btn_refrescar = self._crear_boton("🔃 Refrescar", "#2980b9", self.mostrar_inventario)
        
        botones_layout.addWidget(btn_agregar)
        botones_layout.addWidget(btn_modificar)
        botones_layout.addWidget(btn_eliminar)
        botones_layout.addWidget(btn_refrescar)
        botones_layout.addStretch()  # Espaciador
        
        main_layout.addLayout(botones_layout)
        
        # Visor de imagen
        self.img_viewer = ImagenViewer(self)
        main_layout.addWidget(self.img_viewer)
    
    def _crear_boton(self, texto, color, comando):
        btn = QPushButton(texto)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
                font-family: Arial;
            }}
            QPushButton:hover {{
                background-color: {self._darken_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self._darken_color(color, 40)};
            }}
        """)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(comando)
        return btn
    
    def _darken_color(self, color, amount=20):
        """Oscurecer un color hexadecimal"""
        # Remover # si existe
        color = color.lstrip('#')
        
        # Convertir a RGB
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        
        # Oscurecer
        r = max(0, r - amount)
        g = max(0, g - amount)
        b = max(0, b - amount)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def mostrar_inventario(self):
        # Limpiar tabla
        self.tabla.setRowCount(0)
        
        # Obtener productos
        df = self.producto_model.obtener_todos()
        
        # Configurar número de filas
        self.tabla.setRowCount(len(df))
        
        # Llenar tabla
        for row_idx, (_, row) in enumerate(df.iterrows()):
            precio = formatear_precio(row.get("Precio", 0))
            stock_actual = int(row["Stock"]) if pd.notna(row["Stock"]) else 0
            stock_minimo = int(row["Stock Mínimo"]) if pd.notna(row["Stock Mínimo"]) else 0
            
            values = [
                str(row["ID"]), 
                str(row["Nombre"]), 
                str(row["Categoría"]), 
                str(row.get("Tipo de Corte", "")),
                precio, 
                str(stock_actual), 
                str(stock_minimo),
                os.path.basename(str(row["Imagen"])) if pd.notna(row["Imagen"]) and str(row["Imagen"]).strip() else ""
            ]
            
            for col_idx, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.tabla.setItem(row_idx, col_idx, item)
        
        # Limpiar visor de imagen
        self.img_viewer.limpiar()
    
    def _mostrar_imagen_producto(self):
        current_row = self.tabla.currentRow()
        if current_row < 0:
            return
        
        producto_id_item = self.tabla.item(current_row, 0)  # Primera columna es ID
        if producto_id_item:
            producto_id = producto_id_item.text()
            producto = self.producto_model.obtener_por_id(producto_id)
            
            if producto is not None and not producto.empty:
                imagen_path = producto.get("Imagen", "")
                self.img_viewer.mostrar_imagen(imagen_path)
    
    def _agregar_producto(self):
        AgregarProductoForm(self)
    
    def _modificar_producto(self):
        current_row = self.tabla.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Modificar producto", "Selecciona un producto para modificar.")
            return
        
        producto_id_item = self.tabla.item(current_row, 0)
        producto_id = producto_id_item.text()
        producto_data = self.producto_model.obtener_por_id(producto_id)
        
        if producto_data is not None and not producto_data.empty:
            ModificarProductoForm(self, producto_data)
    
    def _eliminar_producto(self):
        current_row = self.tabla.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Eliminar producto", "Selecciona un producto para eliminar.")
            return
        
        producto_id_item = self.tabla.item(current_row, 0)
        nombre_item = self.tabla.item(current_row, 1)
        
        producto_id = producto_id_item.text()
        nombre_producto = nombre_item.text()
        
        reply = QMessageBox.question(self, "Confirmar eliminación", 
                                   f"¿Seguro que deseas eliminar el producto '{nombre_producto}'?",
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            if self.producto_model.eliminarProducto(producto_id):
                self.mostrar_inventario()
                QMessageBox.information(self, "Producto eliminado", 
                                       f"Producto '{nombre_producto}' eliminado correctamente.")
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar el producto.")

class AgregarProductoForm(ProductoForm):    
    def __init__(self, parent):
        self.parent_frame = parent
        super().__init__(parent, "Registrar Producto")
    
    def _guardar(self):
        datos = self._validar_datos()
        if datos is None:
            return
        
        try:
            producto_model = ProductoModel()
            nuevo_id = producto_model.creaProducto(datos)
            QMessageBox.information(self, "Éxito", "Producto registrado correctamente.")
            self.parent_frame.mostrar_inventario()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error al guardar", f"Error: {e}")

class ModificarProductoForm(ProductoForm):
    def __init__(self, parent, producto_data):
        self.parent_frame = parent
        self.producto_id = producto_data["ID"]
        super().__init__(parent, "Modificar Producto", producto_data)
    
    def _guardar(self):
        datos = self._validar_datos()
        if datos is None:
            return
        
        try:
            producto_model = ProductoModel()
            producto_model.actualizarProducto(self.producto_id, datos)
            QMessageBox.information(self, "Éxito", "Producto modificado correctamente.")
            self.parent_frame.mostrar_inventario()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error al guardar", f"Error: {e}")