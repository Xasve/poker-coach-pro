# ====================================================
# BLOQUE DE EJECUCIÓN: BOT EXTREMO SIN RESTRICCIONES
# ====================================================

Write-Host " CONFIGURANDO BOT DE PÓKER EXTREMO..." -ForegroundColor Cyan
Write-Host " Objetivo: Tiempo de reacción mínimo + Consumo optimizado" -ForegroundColor Yellow

# 1. Instalar dependencias optimizadas
Write-Host "
 INSTALANDO DEPENDENCIAS OPTIMIZADAS..." -ForegroundColor Magenta
python "extreme_optimization\install_extreme.py"

# 2. Configurar sistema
Write-Host "
⚙️ OPTIMIZANDO CONFIGURACIÓN DEL SISTEMA..." -ForegroundColor Cyan
python "extreme_optimization\configure_system.py"

# 3. Verificar instalación
Write-Host "
 VERIFICANDO INSTALACIÓN..." -ForegroundColor Yellow
python -c "
try:
    import cv2, numpy, pyautogui, psutil, numba
    print('✅ TODAS LAS DEPENDENCIAS INSTALADAS:')
    print(f'   OpenCV: {cv2.__version__}')
    print(f'   NumPy: {numpy.__version__}')
    print(f'   PyAutoGUI: {pyautogui.__version__}')
    print(f'   psutil: {psutil.__version__}')
    print(f'   numba: {numba.__version__}')
    print(' Sistema listo para rendimiento extremo')
except ImportError as e:
    print(f' Error: {e}')
    print(' Ejecuta: pip install opencv-contrib-python numpy pyautogui psutil numba')
"

# 4. Crear acceso directo final
Write-Host "
🎮 CREANDO ACCESO DIRECTO EXTREMO..." -ForegroundColor Green
 = @'
@echo off
title  POKER BOT EXTREMO - SIN RESTRICCIONES
color 0A

echo ================================================
echo     BOT DE PÓKER EXTREMO - MODO MÁXIMO
echo ================================================
echo  CARACTERÍSTICAS ACTIVADAS:
echo     Tiempo de reacción: 50ms objetivo
echo     Restricciones: DESACTIVADAS
echo     Optimización de recursos: MÁXIMA
echo     Procesamiento paralelo: ACTIVADO
echo     Cache extremo: ACTIVADO
echo ================================================
echo.

REM Configurar prioridad máxima
powershell -Command "$p = Get-Process -Id $PID; $p.PriorityClass = 'RealTime'"

REM Ejecutar bot extremo
cd /d "%~dp0"
python "extreme_optimization\extreme_poker_bot.py"

pause
'@

 | Out-File -FilePath "RUN_EXTREME_BOT.bat" -Encoding ASCII

Write-Host " ACCESO DIRECTO CREADO: RUN_EXTREME_BOT.bat" -ForegroundColor Green

# 5. Mostrar instrucciones finales
Write-Host "
🏆 CONFIGURACIÓN COMPLETADA" -ForegroundColor Cyan
Write-Host "=" * 50
Write-Host "🚀 PARA INICIAR EL BOT EXTREMO:" -ForegroundColor Green
Write-Host "   Ejecuta: .\RUN_EXTREME_BOT.bat" -ForegroundColor White
Write-Host "   O: python "extreme_optimization\extreme_poker_bot.py"" -ForegroundColor Gray

Write-Host "
 CARACTERÍSTICAS DEL BOT EXTREMO:" -ForegroundColor Yellow
Write-Host "    Tiempo de reacción objetivo: 50ms" -ForegroundColor Gray
Write-Host "    Procesamiento paralelo máximo" -ForegroundColor Gray
Write-Host "    Cache extremo (10,000+ decisiones)" -ForegroundColor Gray
Write-Host "    Optimización automática de memoria/CPU" -ForegroundColor Gray
Write-Host "   • Aprendizaje ultra rápido (batch processing)" -ForegroundColor Gray
Write-Host "   • Sin verificaciones de seguridad" -ForegroundColor Gray
Write-Host "    Prioridad REAL-TIME del sistema" -ForegroundColor Gray

Write-Host "
⚠️  ADVERTENCIA: USO RESPONSABLE" -ForegroundColor Red
Write-Host "   Este bot está optimizado para velocidad máxima." -ForegroundColor DarkYellow
Write-Host "   Verifica los Términos de Servicio de PokerStars." -ForegroundColor DarkYellow
Write-Host "   Solo para fines educativos y de investigación." -ForegroundColor DarkYellow

Write-Host "
 EL BOT ESTÁ LISTO PARA DOMINAR LAS MESAS!" -ForegroundColor Magenta
