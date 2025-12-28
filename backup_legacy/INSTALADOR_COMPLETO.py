# INSTALADOR COMPLETO CON REPARACIÓN DE PATH
import os
import sys
import subprocess
import platform

def print_section(title):
    """Imprimir sección con formato"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def run_command(cmd, description):
    """Ejecutar comando con manejo de errores"""
    print(f"\n {description}...")
    print(f"   Comando: {cmd}")
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print(f"    Completado")
            if result.stdout.strip():
                print(f"   Salida: {result.stdout[:200]}")
            return True
        else:
            print(f"    Error: {result.stderr[:200]}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"     Timeout")
        return False
    except Exception as e:
        print(f"    Excepción: {str(e)}")
        return False

def fix_python_path():
    """Reparar PATH de Python"""
    print_section("REPARANDO PATH DE PYTHON")
    
    # Encontrar Python
    python_paths = []
    
    # Buscar en ubicaciones comunes
    common_paths = [
        r"C:\Python311",
        r"C:\Python311\Scripts",
        r"C:\Program Files\Python311",
        r"C:\Program Files\Python311\Scripts",
        r"%LOCALAPPDATA%\Programs\Python\Python311",
        r"%LOCALAPPDATA%\Programs\Python\Python311\Scripts",
        r"C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311",
        r"C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\Scripts"
    ]
    
    print(" Buscando instalaciones de Python...")
    
    for path_template in common_paths:
        path = os.path.expandvars(path_template)
        if os.path.exists(path):
            python_paths.append(path)
            print(f"    Encontrado: {path}")
    
    if not python_paths:
        print(" No se encontró Python 3.11")
        print(" Descarga Python 3.11 desde python.org")
        return False
    
    # Añadir al PATH temporalmente
    for path in python_paths:
        os.environ["PATH"] = path + ";" + os.environ["PATH"]
    
    print(" PATH actualizado temporalmente")
    return True

def install_dependencies():
    """Instalar todas las dependencias"""
    print_section("INSTALANDO DEPENDENCIAS")
    
    dependencies = [
        ("opencv-contrib-python", "OpenCV (visión por computadora)"),
        ("numpy", "NumPy (cálculos matemáticos)"),
        ("pyautogui", "PyAutoGUI (control de interfaz)"),
        ("psutil", "psutil (monitoreo de recursos)")
    ]
    
    success_count = 0
    
    for package, description in dependencies:
        # Intentar con diferentes métodos
        methods = [
            f'"{sys.executable}" -m pip install {package} --quiet --timeout 30',
            f'pip install {package} --quiet --timeout 30',
            f'py -m pip install {package} --quiet --timeout 30'
        ]
        
        installed = False
        for method in methods:
            if run_command(method, f"Instalando {package} ({description})"):
                installed = True
                success_count += 1
                break
        
        if not installed:
            print(f"     No se pudo instalar {package}")
    
    return success_count

def verify_installation():
    """Verificar que todo está instalado"""
    print_section("VERIFICANDO INSTALACIÓN")
    
    modules = ["cv2", "numpy", "pyautogui", "psutil"]
    success_count = 0
    
    for module in modules:
        try:
            __import__(module)
            version = sys.modules[module].__version__ if hasattr(sys.modules[module], '__version__') else "OK"
            print(f"   ✅ {module}: {version}")
            success_count += 1
        except ImportError:
            print(f"    {module}: NO INSTALADO")
        except Exception as e:
            print(f"     {module}: Error - {str(e)}")
    
    return success_count == len(modules)

def create_launcher():
    """Crear lanzador optimizado"""
    print_section("CREANDO LANZADOR")
    
    launcher_content = '''@echo off
chcp 65001 > nul
title  POKER BOT EXTREMO - LANZADOR
color 0A

echo ================================================
echo     POKER BOT EXTREMO - LANZADOR OPTIMIZADO
echo ================================================
echo Este lanzador configura automáticamente el entorno
echo ================================================
echo.

REM Configurar entorno
set PYTHONPATH=%~dp0
set PATH=%~dp0;%PATH%

REM Verificar dependencias
python -c "import cv2" 2>nul
if errorlevel 1 (
    echo   Dependencias faltantes. Ejecutando instalador...
    python "%~dp0INSTALADOR_COMPLETO.py"
    if errorlevel 1 (
        echo  Error en instalación
        pause
        exit /b 1
    )
)

REM Ejecutar bot
echo  Iniciando Poker Bot Extreme...
echo ⏱️  Tiempo objetivo: 50ms por decisión
echo ⚠️  Presiona Ctrl+C para salir
echo ================================================

python "%~dp0extreme_optimization\\extreme_bot_simple.py"

echo.
echo  Bot finalizado
pause
'''
    
    with open("LANZAR_BOT.bat", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    print(" Lanzador creado: LANZAR_BOT.bat")
    return True

def main():
    """Función principal"""
    print(" INSTALADOR COMPLETO - POKER BOT EXTREMO")
    print("="*60)
    print("Este instalador resolverá problemas de:")
    print("• 'pip is not recognized'")
    print("• 'No module named cv2'")
    print("• PATH de Python incorrecto")
    print("="*60)
    
    # 1. Reparar PATH
    if not fix_python_path():
        print("\n No se pudo reparar el PATH")
        print(" Instala Python 3.11 manualmente desde python.org")
        return False
    
    # 2. Verificar Python
    print(f"\n Información del sistema:")
    print(f"   Python: {sys.version}")
    print(f"   Sistema: {platform.system()} {platform.release()}")
    print(f"   Directorio: {os.getcwd()}")
    
    # 3. Actualizar pip
    run_command(f'"{sys.executable}" -m pip install --upgrade pip --quiet', "Actualizando pip")
    
    # 4. Instalar dependencias
    install_dependencies()
    
    # 5. Verificar instalación
    if not verify_installation():
        print("\n  Algunas dependencias no se instalaron correctamente")
        print(" Intenta instalarlas manualmente:")
        print("   python -m pip install opencv-contrib-python numpy pyautogui psutil")
    
    # 6. Crear lanzador
    create_launcher()
    
    print_section("INSTALACIÓN COMPLETADA")
    print(" Todo listo! Ahora puedes usar el bot.")
    print("\n PARA EJECUTAR EL BOT:")
    print("   1. Abre PowerShell/CMD en esta carpeta")
    print("   2. Ejecuta: .\\LANZAR_BOT.bat")
    print("   3. O ejecuta: python extreme_optimization\\extreme_bot_simple.py")
    print("\n Para guía completa, lee: GUIA_COMPLETA_USO.md")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            input("\n Presiona Enter para salir...")
        else:
            input("\n Hubo problemas. Presiona Enter para salir...")
    except KeyboardInterrupt:
        print("\n\n Instalación cancelada por el usuario")
    except Exception as e:
        print(f"\n Error inesperado: {e}")
        input("Presiona Enter para salir...")
