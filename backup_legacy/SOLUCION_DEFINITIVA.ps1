# ====================================================
# BLOQUE COMPLETO: SOLUCIÓN DEFINITIVA DEL ERROR
# ====================================================

Write-Host " SOLUCIÓN DEFINITIVA PARA ERRORES DE INSTALACIÓN" -ForegroundColor Cyan
Write-Host "="*60

Write-Host "`n PROBLEMAS IDENTIFICADOS:" -ForegroundColor Yellow
Write-Host "   1. 'pip is not recognized'  PATH incorrecto" -ForegroundColor Gray
Write-Host "   2. 'No module named cv2'  OpenCV no instalado" -ForegroundColor Gray
Write-Host "   3. Permisos insuficientes" -ForegroundColor Gray
Write-Host "   4. Variables de entorno mal configuradas" -ForegroundColor Gray

Write-Host "`n SOLUCIÓN EN 3 PASOS:" -ForegroundColor Green

Write-Host "`nPASO 1: REPARAR CONFIGURACIÓN DE WINDOWS (Como Administrador)" -ForegroundColor Magenta
Write-Host "   Ejecuta PowerShell COMO ADMINISTRADOR y corre:" -ForegroundColor White
Write-Host "   python CONFIGURAR_WINDOWS.py" -ForegroundColor Cyan

Write-Host "`nPASO 2: INSTALAR DEPENDENCIAS COMPLETAMENTE" -ForegroundColor Magenta
Write-Host "   En PowerShell normal (NO administrador):" -ForegroundColor White
Write-Host "   python INSTALADOR_COMPLETO.py" -ForegroundColor Cyan

Write-Host "`nPASO 3: EJECUTAR EL BOT" -ForegroundColor Magenta
Write-Host "   .\LANZAR_BOT.bat" -ForegroundColor Cyan
Write-Host "   O: python extreme_optimization\extreme_bot_simple.py" -ForegroundColor Gray

Write-Host "`n COMANDOS ALTERNATIVOS SI HAY PROBLEMAS:" -ForegroundColor Yellow

Write-Host "`nA. INSTALACIÓN MANUAL DE DEPENDENCIAS:" -ForegroundColor White
Write-Host "python -m pip install opencv-contrib-python" -ForegroundColor Gray
Write-Host "python -m pip install numpy" -ForegroundColor Gray
Write-Host "python -m pip install pyautogui" -ForegroundColor Gray
Write-Host "python -m pip install psutil" -ForegroundColor Gray

Write-Host "`nB. VERIFICAR INSTALACIÓN:" -ForegroundColor White
Write-Host "python -c `"import cv2; print(f'OpenCV {cv2.__version__}')`"" -ForegroundColor Gray

Write-Host "`nC. EJECUTAR PRUEBA RÁPIDA:" -ForegroundColor White
Write-Host "python -c `"import cv2, numpy; print(' Sistema listo')`"" -ForegroundColor Gray

Write-Host "`n GUÍA VISUAL DE PASOS:" -ForegroundColor Cyan
Write-Host "   1.  Ejecutar PowerShell como Administrador (Click derecho)" -ForegroundColor Gray
Write-Host "   2.  Navegar: cd Desktop\poker-coach-pro" -ForegroundColor Gray
Write-Host "   3.   Reparar: python CONFIGURAR_WINDOWS.py" -ForegroundColor Gray
Write-Host "   4.  CERRAR PowerShell" -ForegroundColor Gray
Write-Host "   5.  Abrir PowerShell normal" -ForegroundColor Gray
Write-Host "   6.  Instalar: python INSTALADOR_COMPLETO.py" -ForegroundColor Gray
Write-Host "   7.  Ejecutar: .\LANZAR_BOT.bat" -ForegroundColor Gray

Write-Host "`n  SI PERSISTEN LOS ERRORES:" -ForegroundColor Red
Write-Host "   1. Descarga Python 3.11 manualmente: https://python.org" -ForegroundColor DarkYellow
Write-Host "   2. Durante instalación, MARCA 'Add Python to PATH'" -ForegroundColor DarkYellow
Write-Host "   3. Reinicia la computadora" -ForegroundColor DarkYellow
Write-Host "   4. Repite desde Paso 2" -ForegroundColor DarkYellow

Write-Host "`n VERIFICACIÓN FINAL (después de reparar):" -ForegroundColor Green
Write-Host "python -c `"import sys; print(f'Python: {sys.version}')`"" -ForegroundColor Gray
Write-Host "where python" -ForegroundColor Gray
Write-Host "where pip" -ForegroundColor Gray

Write-Host "`n Cuando todo esté configurado, tu bot funcionará con:" -ForegroundColor Magenta
Write-Host "    Tiempo de reacción: 50ms objetivo" -ForegroundColor Gray
Write-Host "    Sin restricciones de seguridad" -ForegroundColor Gray
Write-Host "    Optimización máxima de recursos" -ForegroundColor Gray
Write-Host "    Procesamiento paralelo completo" -ForegroundColor Gray

Write-Host "`n EMPEZAMOS! Primero ejecuta como Administrador:" -ForegroundColor Green
Write-Host "python CONFIGURAR_WINDOWS.py" -ForegroundColor Cyan
