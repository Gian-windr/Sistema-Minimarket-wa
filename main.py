# Sistema de Minimarket Don Manuelito - PyQt5 Version

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

def main():
    try:
        # Crear la aplicación PyQt5
        app = QApplication(sys.argv)
        
        # Configurar propiedades de la aplicación
        app.setApplicationName("Sistema Minimarket Don Manuelito")
        app.setApplicationVersion("2.0.0 - PyQt5 Migration")
        
        # Importar y crear la ventana principal de login
        from views.login import LoginVentana
        login_window = LoginVentana()
        login_window.show()
        
        # Ejecutar la aplicación
        sys.exit(app.exec_())
        
    except ImportError as e:
        print(f"❌ Error al importar módulos PyQt5: {e}")
        print("Verifica que PyQt5 esté instalado: pip install PyQt5")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
    