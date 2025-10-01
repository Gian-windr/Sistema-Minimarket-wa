## Dashboard principal - PyQt5 Optimizado

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame, QStackedWidget)
from PyQt5.QtCore import Qt
from views.settings import *

class Dashboard(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.usuario_rol = self._obtener_rol_usuario()
        self.setWindowTitle(f"{APP_NAME} - {usuario}")
        self.showMaximized()
    
        self._crear_Robotofaz()
    
    def _obtener_rol_usuario(self):
        """Obtiene el rol del usuario actual"""
        try:
            from models.empleado import EmpleadoModel
            empleado_model = EmpleadoModel()
            empleado = empleado_model.obtenerUsuario(self.usuario)
            return empleado['rol'] if empleado else 'empleado'
        except Exception as e:
            print(f"Error obteniendo rol de usuario: {e}")
            return 'empleado'
    
    def _centrar_ventana(self):
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)
    
    def _crear_Robotofaz(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = self._crear_header()
        main_layout.addWidget(header)
        
        # Contenido
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Menú lateral
        menu = self._crear_menu()
        content_layout.addWidget(menu)
        
        # Área principal
        self.main_content = QStackedWidget()
        self.main_content.setStyleSheet("background-color: white;")
        content_layout.addWidget(self.main_content, 1)
        
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget, 1)
        
        self._mostrar_bienvenida()
    
    def _crear_header(self):
        header = QFrame()
        header.setStyleSheet(f"background-color: {THEME_COLOR}; color: white;")
        header.setFixedHeight(85)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 10, 20, 10)
        
        # Título
        titulo = QLabel(f"🏪 {APP_NAME}")
        titulo.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        layout.addWidget(titulo)
        
        layout.addStretch()
        
        # Usuario
        usuario = QLabel(f"👤 {self.usuario}")
        usuario.setStyleSheet("color: white; font-size: 20px;")
        layout.addWidget(usuario)
        
        return header
    
    def _crear_menu(self):
        menu = QFrame()
        menu.setStyleSheet("background-color: #b9c2c4;")
        menu.setFixedWidth(230)
        
        layout = QVBoxLayout(menu)
        layout.setContentsMargins(20, 20, 10, 10) # →, ↓, ←, ↑
        
        # Botones principales
        botones = [
            ("📦 Inventario", self.mostrar_inventario),
            ("💰 Ventas", self.mostrar_ventas),
            ("📊 Reportes", self.mostrar_reportes),
            ("🛒 Compras", self.mostrar_compras),
            ("🚛 Despachos", self.mostrar_despachos),
            ("⚙️ Configuración", self.mostrar_configuracion)
        ]
        
        # Agregar gestión de empleados solo para administradores
        if self.usuario_rol in ['admin']:
            botones.insert(3, ("👥 Empleados", self.mostrar_empleados))
        
        for texto, comando in botones:
            btn = QPushButton(texto)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #b9c2c4;
                    color: {NIGHT_COLOR};
                    border: none;
                    padding: 12px;
                    text-align: left;
                    font-size: 16px;
                    font-family: 'Roboto';
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #9ba5a7;
                }}
            """)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(comando)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Botón salir
        btn_salir = QPushButton("Cerrar Sesión")
        btn_salir.setStyleSheet(f"""
            QPushButton {{
                background-color: {ERROR_COLOR};
                color: white;
                border: none;
                padding: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #c0392b;
            }}
        """)
        btn_salir.clicked.connect(self.close)
        layout.addWidget(btn_salir)
        
        return menu
    
    def _mostrar_bienvenida(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        
        titulo = QLabel("🏪 Bienvenido al Sistema")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin: 20px;")
        
        subtitulo = QLabel("Selecciona un módulo del menú para comenzar")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        
        layout.addWidget(titulo)
        layout.addWidget(subtitulo)
        
        self.main_content.addWidget(widget)
        self.main_content.setCurrentWidget(widget)
    
    def _limpiar_contenido(self):
        while self.main_content.count():
            child = self.main_content.widget(0)
            self.main_content.removeWidget(child)
            child.setParent(None)
    
    def mostrar_inventario(self):
        self._limpiar_contenido()
        try:
            from views.inventario import InventarioFrame
            inventario = InventarioFrame(self)
            self.main_content.addWidget(inventario)
            self.main_content.setCurrentWidget(inventario)
        except Exception as e:
            self._mostrar_error("📦 Inventario", str(e))
    
    def mostrar_ventas(self):
        self._limpiar_contenido()
        try:
            from views.ventas import VentasFrame
            ventas = VentasFrame(self)
            self.main_content.addWidget(ventas)
            self.main_content.setCurrentWidget(ventas)
        except Exception as e:
            self._mostrar_error("💰 Ventas", f"Error al cargar módulo: {str(e)}")
    
    def mostrar_reportes(self):
        self._limpiar_contenido()
        self._mostrar_error("📊 Reportes", "Próximamente en Sprint 3")
    
    def mostrar_empleados(self):
        self._limpiar_contenido()
        try:
            from views.empleados import EmpleadosWidget
            empleados_widget = EmpleadosWidget(self.usuario_rol)
            self.main_content.addWidget(empleados_widget)
            self.main_content.setCurrentWidget(empleados_widget)
        except Exception as e:
            self._mostrar_error("👥 Empleados", f"Error al cargar módulo: {str(e)}")
    
    def mostrar_compras(self):
        self._limpiar_contenido()
        self._mostrar_error("🛒 Compras", "Próximamente en Sprint 4")
    
    def mostrar_despachos(self):
        self._limpiar_contenido()
        self._mostrar_error("🚛 Despachos", "Próximamente en Sprint 4")
    
    def mostrar_configuracion(self):
        self._limpiar_contenido()
        self._mostrar_error("⚙️ Configuración", "Próximamente en Sprint 4")
    
    def _mostrar_error(self, titulo, mensaje):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        
        emoji = QLabel("🚧")
        emoji.setAlignment(Qt.AlignCenter)
        emoji.setStyleSheet("font-size: 48px; margin: 20px;")
        
        title_label = QLabel(titulo)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; color: #95a5a6; margin: 10px;")
        
        msg_label = QLabel(mensaje)
        msg_label.setAlignment(Qt.AlignCenter)
        msg_label.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        
        layout.addWidget(emoji)
        layout.addWidget(title_label)
        layout.addWidget(msg_label)
        
        self.main_content.addWidget(widget)
        self.main_content.setCurrentWidget(widget)
    
    def closeEvent(self, event):
        from PyQt5.QtWidgets import QApplication
        QApplication.quit()
        event.accept()