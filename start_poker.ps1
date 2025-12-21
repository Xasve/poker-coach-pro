# Acceso directo para PowerShell
Write-Host " POKER COACH PRO - INICIO RÁPIDO" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Yellow

 = @(
    @{Name="1.  Entorno virtual 3.11"; Command="poker_env_311\Scripts\python.exe quick_start.py"},
    @{Name="2.  Python 3.11 directo"; Command="python311_scripts\python311.bat quick_start.py"},
    @{Name="3.  Verificar instalación"; Command="python311_scripts\python311.bat -c "import cv2, numpy; print(f'OpenCV {cv2.__version__}, NumPy {numpy.__version__}')""},
    @{Name="4.  Instalar/actualizar paquetes"; Command="python311_scripts\python311.bat -m pip install --upgrade numpy opencv-contrib-python pyautogui"}
)

foreach ( in ) {
    Write-Host .Name -ForegroundColor Gray
}

 = Read-Host "
Selecciona opción (1-4)"
switch () {
    "1" {
        if (Test-Path "poker_env_311\Scripts\python.exe") {
            & "poker_env_311\Scripts\python.exe" quick_start.py
        } else {
            Write-Host " Entorno virtual no encontrado" -ForegroundColor Red
        }
    }
    "2" {
        if (Test-Path "python311_scripts\python311.bat") {
            & "python311_scripts\python311.bat" quick_start.py
        } else {
            Write-Host " Python 3.11 no configurado" -ForegroundColor Red
        }
    }
    "3" {
        if (Test-Path "python311_scripts\python311.bat") {
            & "python311_scripts\python311.bat" -c "import cv2, numpy; print(f' OpenCV {cv2.__version__}, NumPy {numpy.__version__}')"
        }
    }
    "4" {
        if (Test-Path "python311_scripts\python311.bat") {
            & "python311_scripts\python311.bat" -m pip install --upgrade numpy opencv-contrib-python pyautogui pandas PyYAML scikit-learn
        }
    }
    default {
        Write-Host " Opción no válida" -ForegroundColor Red
    }
}
