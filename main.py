# Sistema de Minimarket Don Manuelito

def main():
    try:
        from views.login import LoginVentana
        
        print("🏪 Iniciando Sistema Minimarket Don Manuelito...")
        print("📦 Sprint 1 - Módulo de Inventario")
        print("=" * 50)
        
        app = LoginVentana()
        app.mainloop()
        
        print("\n✅ Aplicación cerrada correctamente.")
        
    except ImportError as e:
        print(f"❌ Error al importar módulos: {e}")
        print("Verifica que todos los archivos estén en su lugar correcto.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
