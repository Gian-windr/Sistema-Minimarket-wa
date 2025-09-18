## Dashboard principal del sistema - PyQt5 Version

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame, QMessageBox, QStackedWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
from config.settings import *

class Dashboard(QMainWindow):
    # Señal personalizada para cuando se cierra el dashboard
    finished = pyqtSignal()
    
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowIcon(QIcon("C:/Users/LENOVO LOQ/Documents/Sistema-Minimarket-wa/db/imagenes/LOGOO.ico"))
        self.setWindowTitle(f"{APP_NAME} - Usuario: {usuario}")
        self.setGeometry(100, 100, 1200, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.main_content = None
        self._crear_interfaz(main_layout)
        self._centrar_ventana()
    
    def _centrar_ventana(self):
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)
    
    def _crear_interfaz(self, main_layout):
        # Barra superior
        header_frame = QFrame()
        header_frame.setStyleSheet(f"background-color: {THEME_COLOR}; color: white;")
        header_frame.setFixedHeight(80)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Título de la aplicación
        titulo_label = QLabel(f"🏪 {APP_NAME}")
        titulo_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                font-family: Arial;
            }
        """)
        header_layout.addWidget(titulo_label)
        
        # Spacer
        header_layout.addStretch()
        
        # Usuario logueado
        usuario_label = QLabel(f"👤 {self.usuario}")
        usuario_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 12px;
                font-family: Arial;
            }
        """)
        header_layout.addWidget(usuario_label)
        
        # Contenido principal horizontal
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Menú lateral
        menu_frame = self._crear_menu_lateral()
        content_layout.addWidget(menu_frame)
        
        # Área de contenido principal
        self.main_content = QStackedWidget()
        self.main_content.setStyleSheet("background-color: white;")
        content_layout.addWidget(self.main_content, 1)  # Expandir para llenar el espacio
        
        # Añadir layouts al layout principal
        main_layout.addWidget(header_frame)
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget, 1)  # Expandir
        
        # Mostrar página por defecto
        self._mostrar_pagina_bienvenida()
    
    def _crear_menu_lateral(self):
        menu_frame = QFrame()
        menu_frame.setStyleSheet("background-color: #b9c2c4;")
        menu_frame.setFixedWidth(200)
        
        menu_layout = QVBoxLayout(menu_frame)
        menu_layout.setContentsMargins(10, 10, 10, 10)
        menu_layout.setSpacing(2)
        
        # Botones del menú
        botones = [
            ("📦 Inventario", self.mostrar_inventario),
            ("💰 Ventas", self.mostrar_ventas),
            ("📋 Despachos", self.mostrar_despachos),
            ("👥 Empleados", self.mostrar_empleados),
            ("📊 Reportes", self.mostrar_reportes),
            ("🛒 Compras", self.mostrar_compras),
            ("📁 Categorías", self.mostrar_categorias),
        ]
        
        for texto, comando in botones:
            btn = QPushButton(texto)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #b9c2c4;
                    color: {NIGHT_COLOR};
                    border: none;
                    padding: 12px;
                    text-align: left;
                    font-size: 11px;
                    font-weight: bold;
                    font-family: Arial;
                }}
                QPushButton:hover {{
                    background-color: #9ba5a7;
                }}
                QPushButton:pressed {{
                    background-color: #8a9497;
                }}
            """)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(comando)
            menu_layout.addWidget(btn)
        
        # Separador
        separador = QFrame()
        separador.setFrameShape(QFrame.HLine)
        separador.setStyleSheet("background-color: #5ccfeb; max-height: 2px; margin: 20px 0px;")
        menu_layout.addWidget(separador)
        
        # Botón de cerrar sesión
        btn_logout = QPushButton("❌ Cerrar Sesión")
        btn_logout.setStyleSheet(f"""
            QPushButton {{
                background-color: {ERROR_COLOR};
                color: white;
                border: none;
                padding: 12px;
                text-align: left;
                font-size: 11px;
                font-weight: bold;
                font-family: Arial;
            }}
            QPushButton:hover {{
                background-color: #c0392b;
            }}
            QPushButton:pressed {{
                background-color: #a93226;
            }}
        """)
        btn_logout.setCursor(Qt.PointingHandCursor)
        btn_logout.clicked.connect(self._cerrar_sesion)
        menu_layout.addWidget(btn_logout)
        
        # Spacer para empujar el botón de logout hacia abajo
        menu_layout.addStretch()
        
        return menu_frame
    
    def _mostrar_pagina_bienvenida(self):
        bienvenida_widget = QWidget()
        bienvenida_layout = QVBoxLayout(bienvenida_widget)
        bienvenida_layout.setAlignment(Qt.AlignCenter)
        
        titulo = QLabel("🏪 Bienvenido al Sistema")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 20px;
            }
        """)
        
        subtitulo = QLabel("Selecciona un módulo del menú lateral para comenzar")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #7f8c8d;
            }
        """)
        
        bienvenida_layout.addWidget(titulo)
        bienvenida_layout.addWidget(subtitulo)
        
        self.main_content.addWidget(bienvenida_widget)
        self.main_content.setCurrentWidget(bienvenida_widget)
    
    def limpiar_main(self):
        # Limpiar el contenido principal
        while self.main_content.count():
            child = self.main_content.widget(0)
            self.main_content.removeWidget(child)
            child.setParent(None)
    
    def mostrar_inventario(self):
        self.limpiar_main()
        try:
            from views.inventario import InventarioFrame
            inventario_widget = InventarioFrame(self)
            self.main_content.addWidget(inventario_widget)
            self.main_content.setCurrentWidget(inventario_widget)
        except Exception as e:
            self._mostrar_modulo_pendiente("📦 Módulo de Inventario", "Error al cargar el módulo", str(e))
    
    def mostrar_ventas(self):
        self._mostrar_modulo_pendiente("💰 Módulo de Ventas", "Próximamente en Sprint 2")
    
    def mostrar_despachos(self):
        self._mostrar_modulo_pendiente("📋 Módulo de Despachos", "Próximamente en Sprint 3")
    
    def mostrar_empleados(self):
        self._mostrar_modulo_pendiente("👥 Módulo de Empleados", "Próximamente en Sprint 4")
    
    def mostrar_reportes(self):
        self._mostrar_modulo_pendiente("📊 Módulo de Reportes", "Próximamente en Sprint 5")
    
    def mostrar_compras(self):
        self._mostrar_modulo_pendiente("🛒 Módulo de Compras", "Próximamente en Sprint 6")
    
    def mostrar_categorias(self):
        self._mostrar_modulo_pendiente("📁 Módulo de Categorías", "Próximamente en Sprint 2")
    
    def _mostrar_modulo_pendiente(self, titulo, subtitulo, error=None):
        self.limpiar_main()
        
        pendiente_widget = QWidget()
        pendiente_layout = QVBoxLayout(pendiente_widget)
        pendiente_layout.setAlignment(Qt.AlignCenter)
        
        emoji_label = QLabel("🚧")
        emoji_label.setAlignment(Qt.AlignCenter)
        emoji_label.setStyleSheet("""
            QLabel {
                font-size: 60px;
                margin-bottom: 20px;
            }
        """)
        
        titulo_label = QLabel(titulo)
        titulo_label.setAlignment(Qt.AlignCenter)
        titulo_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: #95a5a6;
                font-family: Arial;
                margin-bottom: 10px;
            }
        """)
        
        subtitulo_label = QLabel(subtitulo)
        subtitulo_label.setAlignment(Qt.AlignCenter)
        subtitulo_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #7f8c8d;
                font-family: Arial;
            }
        """)
        
        pendiente_layout.addWidget(emoji_label)
        pendiente_layout.addWidget(titulo_label)
        pendiente_layout.addWidget(subtitulo_label)
        
        if error:
            error_label = QLabel(f"Error: {error}")
            error_label.setAlignment(Qt.AlignCenter)
            error_label.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    color: #e74c3c;
                    font-family: Arial;
                    margin-top: 10px;
                    padding: 10px;
                    background-color: #fdf2f2;
                    border: 1px solid #e74c3c;
                    border-radius: 4px;
                }
            """)
            error_label.setWordWrap(True)
            pendiente_layout.addWidget(error_label)
        
        self.main_content.addWidget(pendiente_widget)
        self.main_content.setCurrentWidget(pendiente_widget)
    
    def _cerrar_sesion(self):
        reply = QMessageBox.question(self, "Cerrar Sesión", 
                                   "¿Estás seguro que deseas cerrar la sesión?",
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.finished.emit()  # Emitir señal antes de cerrar
            self.close()
    
    def closeEvent(self, event):
        # Emitir señal cuando se cierre la ventana
        self.finished.emit()
        event.accept()    