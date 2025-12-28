#!/usr/bin/env python3
"""
 INSTALLER_COMPLETE.py - Instalador Completo de Dependencias
Instala todo lo necesario para el sistema de detección de cartas
"""

import sys
import subprocess
import os
from pathlib import Path

def run_command(cmd, description):
    """Ejecutar comando con manejo de errores"""
    print(f" {description}...", end="", flush=True)
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            print(" ")
            return True
        else:
            print(" ")
            print(f"   Error: {result.stderr[:100]}")
            return False
            
    except Exception as e:
        print(f"  (Error: {str(e)[:50]})")
        return False

def main():
    """Función principal"""
    print(" INSTALADOR COMPLETO DE DEPENDENCIAS")
    print("=" * 60)
    print()
    print("Este instalador configurará todo para el sistema de")
    print("detección de cartas y análisis IA en tiempo real.")
    print()
    
    # Verificar Python
    print(" Verificando Python...")
    if sys.version_info < (3, 8):
        print(" Python 3.8+ requerido")
        print(" Descargue desde: https://www.python.org/downloads/")
        input("Presione Enter para salir...")
        return
    
    print(f" Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print()
    
    # Actualizar pip
    run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "Actualizando pip"
    )
    
    # Instalar dependencias CORE (críticas)
    print()
    print(" INSTALANDO DEPENDENCIAS CORE:")
    print("-" * 40)
    
    core_packages = [
        "opencv-python==4.8.1.78",
        "opencv-contrib-python==4.8.1.78",
        "numpy==1.24.3",
        "pandas==2.0.3",
        "pyautogui==0.9.54"
    ]
    
    for package in core_packages:
        run_command(
            f"{sys.executable} -m pip install {package}",
            f"Instalando {package.split('==')[0]}"
        )
    
    # Instalar dependencias OCR
    print()
    print("🎴 INSTALANDO DEPENDENCIAS OCR:")
    print("-" * 40)
    
    ocr_packages = [
        "pytesseract",
        "pillow==10.0.0",
        "scikit-image==0.21.0"
    ]
    
    for package in ocr_packages:
        run_command(
            f"{sys.executable} -m pip install {package}",
            f"Instalando {package.split('==')[0]}"
        )
    
    # Instalar dependencias de captura
    print()
    print(" INSTALANDO DEPENDENCIAS CAPTURA:")
    print("-" * 40)
    
    capture_packages = [
        "mss==9.0.1",
        "pygetwindow==0.0.9",
        "pyrect==0.2.0"
    ]
    
    for package in capture_packages:
        run_command(
            f"{sys.executable} -m pip install {package}",
            f"Instalando {package.split('==')[0]}"
        )
    
    # Instalar dependencias IA/Analysis
    print()
    print(" INSTALANDO DEPENDENCIAS IA:")
    print("-" * 40)
    
    ai_packages = [
        "scikit-learn==1.3.0",
        "scipy==1.11.3",
        "joblib==1.3.2"
    ]
    
    for package in ai_packages:
        run_command(
            f"{sys.executable} -m pip install {package}",
            f"Instalando {package.split('==')[0]}"
        )
    
    # Instalar dependencias de sistema
    print()
    print("⚙️  INSTALANDO DEPENDENCIAS SISTEMA:")
    print("-" * 40)
    
    system_packages = [
        "PyYAML==6.0",
        "psutil==5.9.5",
        "colorama==0.4.6",
        "keyboard==0.13.5",
        "pynput==1.7.6"
    ]
    
    for package in system_packages:
        run_command(
            f"{sys.executable} -m pip install {package}",
            f"Instalando {package.split('==')[0]}"
        )
    
    # Instalar Tesseract OCR (Windows)
    if sys.platform == "win32":
        print()
        print(" INSTALANDO TESSERACT OCR (Windows):")
        print("-" * 40)
        
        tesseract_url = "https://github.com/UB-Mannheim/tesseract/wiki"
        print(f" Para mejor precisión OCR, instale Tesseract manualmente:")
        print(f"   {tesseract_url}")
        print("   Descargue el instalador y siga las instrucciones")
        print("   Asegúrese de añadir Tesseract al PATH")
    
    # Crear estructura de directorios
    print()
    print("📁 CREANDO ESTRUCTURA:")
    print("-" * 40)
    
    directories = [
        "data",
        "logs", 
        "config",
        "screenshots",
        "models",
        "card_templates",
        "backups"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f" Creado: {directory}")
        else:
            print(f" Existe: {directory}")
    
    # Crear archivos de configuración si no existen
    print()
    print("  CONFIGURANDO SISTEMA:")
    print("-" * 40)
    
    config_files = {
        "config/detection_config.yaml": """# Configuración de detección
ocr:
  enabled: true
  confidence_threshold: 0.75
""",
        "config/system_config.yaml": """# Configuración del sistema
system:
  version: "2.2.0"
  mode: "professional"
"""
    }
    
    for filepath, content in config_files.items():
        config_path = Path(filepath)
        if not config_path.exists():
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(content, encoding='utf-8')
            print(f" Creado: {filepath}")
    
    # Verificar instalación
    print()
    print(" VERIFICANDO INSTALACIÓN:")
    print("-" * 40)
    
    test_imports = [
        ("OpenCV", "cv2"),
        ("NumPy", "numpy"),
        ("PyAutoGUI", "pyautogui"),
        ("Pandas", "pandas"),
        ("Pillow", "PIL"),
        ("MSS", "mss")
    ]
    
    all_ok = True
    for name, module in test_imports:
        print(f" {name}...", end="", flush=True)
        try:
            __import__(module)
            print(" ")
        except ImportError:
            print(" ")
            all_ok = False
    
    print()
    print("=" * 60)
    
    if all_ok:
        print(" INSTALACIÓN COMPLETADA EXITOSAMENTE!")
        print()
        print(" PARA INICIAR EL SISTEMA:")
        print("1. Ejecute: python quick_start.py")
        print("2. Seleccione opción 1 (Sistema completo)")
        print("3. Elija ' IA Integrada'")
        print()
        print(" CONSEJOS:")
        print(" Para mejor precisión OCR, instale Tesseract")
        print(" Calibre el sistema primero (opción 4)")
        print(" Use PokerStars en tema 'Classic'")
    else:
        print("  INSTALACIÓN PARCIALMENTE COMPLETADA")
        print()
        print(" ALGUNAS DEPENDENCIAS FALTAN:")
        print(" Reinstale manualmente: pip install opencv-python numpy")
        print(" Verifique conexión a internet")
        print(" Ejecute este instalador nuevamente")
    
    print()
    input("Presione Enter para salir...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Instalación cancelada por el usuario")
    except Exception as e:
        print(f"\n Error en instalador: {e}")
        input("Presione Enter para salir...")
