# Sistema de Minimarket Don Manuelito

def main():
    try:
        from views.login import LoginVentana
        app = LoginVentana()
        app.mainloop()
    except ImportError as e:
        print(f"❌ Error al importar módulos: {e}")
        print("Verifica que todos los archivos estén en su lugar correcto.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
