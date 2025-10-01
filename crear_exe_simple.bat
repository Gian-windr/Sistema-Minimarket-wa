@echo off
REM Script simple para crear ejecutable
echo "========================================"
echo "    CREANDO EJECUTABLE MINIMARKET"  
echo "========================================"
echo.

echo [1/3] Limpiando archivos anteriores...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del /q "*.spec"

echo [2/3] Creando ejecutable (Metodo Basico)...
echo NOTA: Este proceso puede tomar 5-10 minutos
echo.

"C:\Users\LENOVO LOQ\AppData\Local\Programs\Python\Python313\python.exe" -m PyInstaller ^
    --onefile ^
    --noconsole ^
    --icon="db\imagenes\LOGO.ico" ^
    --name="SistemaMinimarket" ^
    --add-data="db\imagenes;db\imagenes" ^
    --add-data="db\minimarket.db;db" ^
    --distpath="dist" ^
    main.py

echo.
if exist "dist\SistemaMinimarket.exe" (
    echo ======================================== 
    echo ✓ EJECUTABLE CREADO EXITOSAMENTE
    echo ========================================
    echo Ubicacion: dist\SistemaMinimarket.exe
    for %%I in ("dist\SistemaMinimarket.exe") do echo Tamano: %%~zI bytes
    echo.
    echo Para distribuir:
    echo   • Comparte solo el archivo SistemaMinimarket.exe  
    echo   • No necesita Python instalado
    echo   • Funciona en cualquier Windows 10/11
    echo ========================================
    explorer.exe dist
) else (
    echo ❌ ERROR: No se pudo crear el ejecutable
)

pause