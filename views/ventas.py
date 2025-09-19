## Módulo de Ventas - Sistema Minimarket

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QLineEdit, QSpinBox, QMessageBox, QFrame)
from PyQt5.QtCore import Qt
from views.settings import *
from models.producto import ProductoModel
from models.venta import VentaModel
from models.helpers import formatear_precio
import pandas as pd

class VentasFrame(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.producto_model = ProductoModel()
        self.venta_model = VentaModel()
        self.carrito = []  # Lista de productos en el carrito
        self.total = 0.0
        
        self.crearInterfaz()
        self.cargarProductos()
    
    def crearInterfaz(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Panel izquierdo - Productos disponibles
        left_panel = self.crearPanelProductos()
        main_layout.addWidget(left_panel, 2)
        
        # Panel derecho - Carrito de compras
        right_panel = self.crearPanelCarrito()
        main_layout.addWidget(right_panel, 1)
    
    def crearPanelProductos(self):
        panel = QFrame()
        panel.setStyleSheet("border: 1px solid #ddd; border-radius: 5px; padding: 10px;")
        
        layout = QVBoxLayout(panel)
        
        # Título
        titulo = QLabel("📦 Productos Disponibles")
        titulo.setStyleSheet(f"color: {THEME_COLOR}; font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titulo)
        
        # Información de ventas del día
        info_layout = QHBoxLayout()
        self.crearInfoDia(info_layout)
        layout.addLayout(info_layout)
        
        # Búsqueda
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar producto...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
        """)
        self.search_input.textChanged.connect(self.buscarProducto)
        
        btn_limpiar = QPushButton("🗑️")
        btn_limpiar.setFixedSize(35, 35)
        btn_limpiar.clicked.connect(self.limpiarBusqueda)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(btn_limpiar)
        layout.addLayout(search_layout)
        
        # Tabla de productos
        self.tabla_productos = QTableWidget()
        self.tabla_productos.setColumnCount(5)
        self.tabla_productos.setHorizontalHeaderLabels(["ID", "Nombre", "Precio", "Stock", "Acción"])
        
        # Configurar tabla
        self.tabla_productos.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_productos.setAlternatingRowColors(True)
        self.tabla_productos.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                background-color: white;
                selection-background-color: #e3f2fd;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        # Ajustar columnas
        header = self.tabla_productos.horizontalHeader()
        header.setStretchLastSection(False)
        self.tabla_productos.setColumnWidth(0, 70)   # ID
        self.tabla_productos.setColumnWidth(1, 200)  # Nombre
        self.tabla_productos.setColumnWidth(2, 80)   # Precio
        self.tabla_productos.setColumnWidth(3, 60)   # Stock
        self.tabla_productos.setColumnWidth(4, 80)   # Acción
        
        layout.addWidget(self.tabla_productos)
        
        return panel
    
    def crearInfoDia(self, layout):
        resumen = self.venta_model.obtener_resumen_dia()
        
        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: #ecf0f1; border-radius: 5px; padding: 10px;")
        
        info_layout = QHBoxLayout(info_frame)
        
        # Ventas del día
        ventas_label = QLabel(f"📊 Ventas hoy: {resumen['total_ventas']}")
        ventas_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        
        # Total del día
        total_label = QLabel(f"💰 Total: {formatear_precio(resumen['monto_total'])}")
        total_label.setStyleSheet("font-weight: bold; color: #27ae60;")
        
        info_layout.addWidget(ventas_label)
        info_layout.addStretch()
        info_layout.addWidget(total_label)
        
        layout.addWidget(info_frame)
    
    def crearPanelCarrito(self):
        panel = QFrame()
        panel.setStyleSheet("border: 1px solid #ddd; border-radius: 5px; padding: 10px;")
        
        layout = QVBoxLayout(panel)
        
        # Título
        titulo = QLabel("🛒 Carrito de Compras")
        titulo.setStyleSheet(f"color: {THEME_COLOR}; font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titulo)
        
        # Tabla del carrito
        self.tabla_carrito = QTableWidget()
        self.tabla_carrito.setColumnCount(5)
        self.tabla_carrito.setHorizontalHeaderLabels(["Producto", "Cant.", "Precio", "Total", "Acción"])
        self.tabla_carrito.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                background-color: #f9f9f9;
            }
            QTableWidget::item {
                padding: 6px;
            }
        """)
        
        # Ajustar columnas del carrito
        self.tabla_carrito.setColumnWidth(0, 120)  # Producto
        self.tabla_carrito.setColumnWidth(1, 50)   # Cantidad
        self.tabla_carrito.setColumnWidth(2, 70)   # Precio
        self.tabla_carrito.setColumnWidth(3, 80)   # Total
        self.tabla_carrito.setColumnWidth(4, 50)   # Acción
        
        layout.addWidget(self.tabla_carrito)
        
        # Total
        self.label_total = QLabel("Total: S/ 0.00")
        self.label_total.setStyleSheet(f"""
            QLabel {{
                background-color: {THEME_COLOR};
                color: white;
                padding: 12px;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
            }}
        """)
        self.label_total.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_total)
        
        # Botones del carrito
        btn_layout = QVBoxLayout()
        
        btn_procesar = QPushButton("💳 Procesar Venta")
        btn_procesar.setStyleSheet(f"""
            QPushButton {{
                background-color: {SUCCESS_COLOR};
                color: white;
                border: none;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #27ae60;
            }}
        """)
        btn_procesar.clicked.connect(self.procesarVenta)
        
        btn_limpiar = QPushButton("🗑️ Limpiar Carrito")
        btn_limpiar.setStyleSheet(f"""
            QPushButton {{
                background-color: {WARNING_COLOR};
                color: white;
                border: none;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #e67e22;
            }}
        """)
        btn_limpiar.clicked.connect(self.limpiarCarrito)
        
        btn_layout.addWidget(btn_procesar)
        btn_layout.addWidget(btn_limpiar)
        layout.addLayout(btn_layout)
        
        return panel
    
    def cargarProductos(self):
        df = self.producto_model.obtener_todos()
        
        self.tabla_productos.setRowCount(len(df))
        
        for row_idx, (_, row) in enumerate(df.iterrows()):
            # Solo mostrar productos con stock
            stock = int(row["Stock"]) if pd.notna(row["Stock"]) else 0
            if stock > 0:
                # ID
                self.tabla_productos.setItem(row_idx, 0, QTableWidgetItem(str(row["ID"])))
                
                # Nombre
                self.tabla_productos.setItem(row_idx, 1, QTableWidgetItem(str(row["Nombre"])))
                
                # Precio
                precio_texto = formatear_precio(row["Precio"])
                self.tabla_productos.setItem(row_idx, 2, QTableWidgetItem(precio_texto))
                
                # Stock
                self.tabla_productos.setItem(row_idx, 3, QTableWidgetItem(str(stock)))
                
                # Botón agregar
                btn_agregar = QPushButton("➕")
                btn_agregar.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {INFO_COLOR};
                        color: white;
                        border: none;
                        border-radius: 3px;
                        font-weight: bold;
                    }}
                    QPushButton:hover {{
                        background-color: #2980b9;
                    }}
                """)
                btn_agregar.clicked.connect(lambda checked, r=row: self.agregarCarrito(r))
                self.tabla_productos.setCellWidget(row_idx, 4, btn_agregar)
    
    def buscarProducto(self, texto):
        if not texto.strip():
            self.cargarProductos()
            return
        
        df = self.producto_model.buscarProducto(texto)
        
        self.tabla_productos.setRowCount(len(df))
        
        for row_idx, (_, row) in enumerate(df.iterrows()):
            stock = int(row["Stock"]) if pd.notna(row["Stock"]) else 0
            if stock > 0:
                self.tabla_productos.setItem(row_idx, 0, QTableWidgetItem(str(row["ID"])))
                self.tabla_productos.setItem(row_idx, 1, QTableWidgetItem(str(row["Nombre"])))
                self.tabla_productos.setItem(row_idx, 2, QTableWidgetItem(formatear_precio(row["Precio"])))
                self.tabla_productos.setItem(row_idx, 3, QTableWidgetItem(str(stock)))
                
                btn_agregar = QPushButton("➕")
                btn_agregar.clicked.connect(lambda checked, r=row: self.agregarCarrito(r))
                self.tabla_productos.setCellWidget(row_idx, 4, btn_agregar)
    
    def limpiarBusqueda(self):
        self.search_input.clear()
        self.cargarProductos()
    
    def agregarCarrito(self, producto):
        producto_id = str(producto["ID"])
        nombre = str(producto["Nombre"])
        precio = float(producto["Precio"])
        
        # Verificar si el producto ya está en el carrito
        for item in self.carrito:
            if item["id"] == producto_id:
                item["cantidad"] += 1
                item["total"] = item["cantidad"] * item["precio"]
                break
        else:
            # Agregar nuevo producto al carrito
            self.carrito.append({
                "id": producto_id,
                "nombre": nombre,
                "cantidad": 1,
                "precio": precio,
                "total": precio
            })
        
        self.actualizarCarrito()
        QMessageBox.information(self, "Producto agregado", f"'{nombre}' agregado al carrito")
    
    def actualizarCarrito(self):
        self.tabla_carrito.setRowCount(len(self.carrito))
        self.total = 0.0
        
        for row_idx, item in enumerate(self.carrito):
            self.tabla_carrito.setItem(row_idx, 0, QTableWidgetItem(item["nombre"]))
            self.tabla_carrito.setItem(row_idx, 1, QTableWidgetItem(str(item["cantidad"])))
            self.tabla_carrito.setItem(row_idx, 2, QTableWidgetItem(formatear_precio(item["precio"])))
            self.tabla_carrito.setItem(row_idx, 3, QTableWidgetItem(formatear_precio(item["total"])))
            
            # Botón remover
            btn_remover = QPushButton("🗑️")
            btn_remover.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ERROR_COLOR};
                    color: white;
                    border: none;
                    border-radius: 3px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #c0392b;
                }}
            """)
            btn_remover.clicked.connect(lambda checked, idx=row_idx: self.removerCarrito(idx))
            self.tabla_carrito.setCellWidget(row_idx, 4, btn_remover)
            
            self.total += item["total"]
        
        self.label_total.setText(f"Total: {formatear_precio(self.total)}")
    
    def removerCarrito(self, indice):
        if 0 <= indice < len(self.carrito):
            producto_removido = self.carrito.pop(indice)
            self.actualizarCarrito()
            QMessageBox.information(self, "Producto removido", 
                                   f"'{producto_removido['nombre']}' removido del carrito")
    
    def limpiarCarrito(self):
        self.carrito.clear()
        self.actualizarCarrito()
        QMessageBox.information(self, "Carrito limpio", "Todos los productos han sido removidos del carrito")
    
    def procesarVenta(self):
        """Procesar la venta actual"""
        if not self.carrito:
            QMessageBox.warning(self, "Carrito vacío", "Agrega productos al carrito antes de procesar la venta")
            return
        
        # Confirmar venta
        reply = QMessageBox.question(self, "Procesar Venta", 
                                   f"¿Procesar venta por {formatear_precio(self.total)}?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Procesar la venta usando el modelo
            success, venta_id, mensaje = self.venta_model.procesar_venta(
                carrito=self.carrito,
                empleado="Admin",  # Por ahora usamos Admin por defecto
                metodo_pago="efectivo"
            )
            
            if success:
                QMessageBox.information(self, "Venta Exitosa", 
                                       f"✅ {mensaje}\nID: {venta_id}")
                self.limpiarCarrito()
                self.cargarProductos()  # Recargar para actualizar stock
            else:
                QMessageBox.critical(self, "Error en Venta", f"❌ {mensaje}")