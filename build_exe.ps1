# Script PowerShell para crear ejecutable del Sistema Minimarket
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   SISTEMA MINIMARKET - BUILD EJECUTABLE" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host

# Variables
$pythonPath = "C:/Users/LENOVO LOQ/AppData/Local/Programs/Python/Python313/python.exe"
$iconPath = "db/imagenes/LOGO.ico"
$mainFile = "main.py"
$exeName = "SistemaMinimarket"

Write-Host "[1/4] Limpiando archivos anteriores..." -ForegroundColor Yellow
if (Test-Path "dist") { Remove-Item "dist" -Recurse -Force }
if (Test-Path "build") { Remove-Item "build" -Recurse -Force }
if (Test-Path "*.spec") { Remove-Item "*.spec" -Force }

Write-Host "[2/4] Verificando dependencias..." -ForegroundColor Yellow
try {
    & $pythonPath -c "import PyQt5; print('✓ PyQt5 OK')"
    & $pythonPath -c "import pandas; print('✓ Pandas OK')" 
    & $pythonPath -c "import sqlite3; print('✓ SQLite OK')"
    & $pythonPath -c "import PyInstaller; print('✓ PyInstaller OK')"
    Write-Host "✅ Todas las dependencias están instaladas" -ForegroundColor Green
} catch {
    Write-Host "❌ Error verificando dependencias: $_" -ForegroundColor Red
    pause
    exit
}

Write-Host "[3/4] Construyendo ejecutable..." -ForegroundColor Yellow
Write-Host "⏳ Esto puede tomar varios minutos, por favor espera..." -ForegroundColor Cyan

try {
    & $pythonPath -m PyInstaller --onefile --noconsole --icon=$iconPath --name=$exeName $mainFile
    
    if (Test-Path "dist\$exeName.exe") {
        Write-Host
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "✓ EJECUTABLE CREADO EXITOSAMENTE" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "📂 Ubicación: dist\$exeName.exe" -ForegroundColor White
        
        $fileInfo = Get-Item "dist\$exeName.exe"
        $sizeInMB = [Math]::Round($fileInfo.Length / 1MB, 2)
        Write-Host "📏 Tamaño: $sizeInMB MB" -ForegroundColor White
        Write-Host "📅 Creado: $($fileInfo.CreationTime)" -ForegroundColor White
        Write-Host
        Write-Host "🎯 Para distribuir:" -ForegroundColor Cyan
        Write-Host "   • Comparte solo el archivo SistemaMinimarket.exe" -ForegroundColor White
        Write-Host "   • No necesita Python instalado en PC destino" -ForegroundColor White
        Write-Host "   • Funciona en cualquier Windows 10/11" -ForegroundColor White
        Write-Host "========================================" -ForegroundColor Green
        
        # Opción para abrir carpeta
        $openFolder = Read-Host "¿Abrir carpeta dist? (s/n)"
        if ($openFolder -eq 's' -or $openFolder -eq 'S') {
            Start-Process "explorer.exe" -ArgumentList "dist"
        }
        
    } else {
        Write-Host
        Write-Host "❌ ERROR: No se pudo crear el ejecutable" -ForegroundColor Red
        Write-Host "Revisa los mensajes de error anteriores" -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ Error durante la construcción: $_" -ForegroundColor Red
}

Write-Host
Write-Host "Presiona cualquier tecla para continuar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")