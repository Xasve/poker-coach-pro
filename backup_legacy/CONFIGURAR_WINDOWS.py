# CONFIGURADOR DE WINDOWS PARA POKER BOT
import os
import sys
import subprocess

def run_as_admin():
    """Verificar si se ejecuta como administrador"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def fix_environment():
    """Reparar variables de entorno de Windows"""
    
    print(" REPARANDO VARIABLES DE ENTORNO DE WINDOWS")
    print("="*60)
    
    if not run_as_admin():
        print("  Este script requiere permisos de administrador")
        print(" Ejecuta PowerShell como administrador y corre:")
        print("   python CONFIGURAR_WINDOWS.py")
        return False
    
    # Encontrar Python
    print("\n Buscando instalaciones de Python...")
    
    python_paths = []
    search_paths = [
        r"C:\Python311",
        r"C:\Program Files\Python311",
        r"%LOCALAPPDATA%\Programs\Python\Python311",
        r"C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311"
    ]
    
    for path_template in search_paths:
        path = os.path.expandvars(path_template)
        if os.path.exists(path):
            python_exe = os.path.join(path, "python.exe")
            pip_exe = os.path.join(path, "Scripts", "pip.exe")
            
            if os.path.exists(python_exe):
                python_paths.append({
                    'python': python_exe,
                    'pip': pip_exe if os.path.exists(pip_exe) else None,
                    'folder': path
                })
                print(f" Python encontrado: {path}")
    
    if not python_paths:
        print(" No se encontró Python 3.11")
        print(" Descarga desde: https://www.python.org/downloads/")
        print("   Versión recomendada: Python 3.11.9")
        return False
    
    # Usar la primera instalación encontrada
    python_info = python_paths[0]
    
    # Añadir al PATH del sistema
    print(f"\n Añadiendo al PATH del sistema: {python_info['folder']}")
    
    try:
        import winreg
        
        # Abrir la clave del PATH del sistema
        reg_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, 
                           winreg.KEY_ALL_ACCESS) as key:
            
            # Leer PATH actual
            try:
                current_path, _ = winreg.QueryValueEx(key, "Path")
            except:
                current_path = ""
            
            # Añadir Python y Scripts si no están
            python_dir = python_info['folder']
            scripts_dir = os.path.join(python_dir, "Scripts")
            
            if python_dir not in current_path:
                new_path = f"{python_dir};{scripts_dir};{current_path}"
                winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                print(f" PATH actualizado correctamente")
            else:
                print(f" Python ya está en el PATH")
                
    except Exception as e:
        print(f"  No se pudo modificar el PATH del sistema: {e}")
        print(" Añade manualmente al PATH:")
        print(f"   {python_info['folder']}")
        print(f"   {scripts_dir}")
    
    return True

def create_powershell_profile():
    """Crear perfil de PowerShell con aliases útiles"""
    
    print("\n CREANDO PERFIL DE POWERSHELL")
    
    profile_path = os.path.expanduser("~\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1")
    profile_dir = os.path.dirname(profile_path)
    
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)
    
    profile_content = '''
#  PERFIL POWERSHELL PARA POKER BOT EXTREMO

# Aliases para Poker Bot
function Start-PokerBot {
    Write-Host " Iniciando Poker Bot Extreme..." -ForegroundColor Cyan
    python "extreme_optimization\\extreme_bot_simple.py"
}

function Install-PokerDeps {
    Write-Host " Instalando dependencias del Poker Bot..." -ForegroundColor Yellow
    python -m pip install opencv-contrib-python numpy pyautogui psutil --quiet
    Write-Host " Dependencias instaladas" -ForegroundColor Green
}

function Test-PokerSetup {
    Write-Host " Verificando configuración del Poker Bot..." -ForegroundColor Cyan
    python -c "
try:
    import cv2, numpy, pyautogui, psutil
    print(' Sistema configurado correctamente')
    print(f'OpenCV: {cv2.__version__}')
    print(f'NumPy: {numpy.__version__}')
except ImportError as e:
    print(f' Error: {e}')
    print(' Ejecuta: Install-PokerDeps')
"
}

function Update-PokerBot {
    Write-Host " Actualizando Poker Bot..." -ForegroundColor Yellow
    git pull origin main
    python -m pip install --upgrade opencv-contrib-python numpy pyautogui psutil
    Write-Host " Poker Bot actualizado" -ForegroundColor Green
}

# Mostrar aliases disponibles
Write-Host " POKER BOT EXTREMO - ALIAS DISPONIBLES:" -ForegroundColor Magenta
Write-Host "   Start-PokerBot    : Inicia el bot" -ForegroundColor Gray
Write-Host "   Install-PokerDeps : Instala dependencias" -ForegroundColor Gray
Write-Host "   Test-PokerSetup   : Verifica configuración" -ForegroundColor Gray
Write-Host "   Update-PokerBot   : Actualiza el bot" -ForegroundColor Gray
'''
    
    with open(profile_path, "w", encoding="utf-8") as f:
        f.write(profile_content)
    
    print(f" Perfil creado: {profile_path}")
    print(" Reinicia PowerShell para cargar los nuevos aliases")
    
    return True

def main():
    """Función principal"""
    print(" CONFIGURADOR DE WINDOWS PARA POKER BOT")
    print("="*60)
    print("Este script solucionará problemas de:")
    print(" 'pip is not recognized'")
    print(" Variables de entorno incorrectas")
    print(" Permisos de instalación")
    print("="*60)
    
    # 1. Verificar permisos
    if not run_as_admin():
        print("\n  EJECUTA COMO ADMINISTRADOR:")
        print("   1. Cierra esta ventana")
        print("   2. Busca 'PowerShell'")
        print("   3. Haz click derecho  'Ejecutar como administrador'")
        print("   4. Navega a esta carpeta: cd Desktop\\poker-coach-pro")
        print("   5. Ejecuta: python CONFIGURAR_WINDOWS.py")
        input("\nPresiona Enter para salir...")
        return False
    
    print("\n Ejecutando como administrador")
    
    # 2. Reparar entorno
    fix_environment()
    
    # 3. Crear perfil de PowerShell
    create_powershell_profile()
    
    print("\n" + "="*60)
    print(" CONFIGURACIÓN COMPLETADA")
    print("="*60)
    print("\n PASOS SIGUIENTES:")
    print("   1. CIERRA TODAS LAS VENTANAS de PowerShell/CMD")
    print("   2. Abre NUEVA ventana de PowerShell")
    print("   3. Navega a la carpeta: cd Desktop\\poker-coach-pro")
    print("   4. Ejecuta: .\\LANZAR_BOT.bat")
    print("\n Para ayuda: python extreme_optimization\\extreme_bot_simple.py")
    print("   (Luego selecciona opción 4 para verificar sistema)")
    
    input("\n Presiona Enter para finalizar...")
    return True

if __name__ == "__main__":
    main()
