#!/usr/bin/env python3
"""
Script de instalación para Poker Coach Pro - PokerStars Edition
"""
import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    """Imprimir encabezado"""
    print("\n" + "=" * 60)
    print(" POKER COACH PRO - INSTALADOR POKERSTARS")
    print("=" * 60)

def check_python_version():
    """Verificar versión de Python"""
    print("\n Verificando Python...")
    
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print(" Versión compatible")
        return True
    else:
        print(" Se requiere Python 3.8 o superior")
        return False

def install_dependencies():
    """Instalar dependencias"""
    print("\n Instalando dependencias...")
    
    requirements = [
        "opencv-python>=4.5.0",
        "numpy>=1.19.0",
        "pillow>=8.0.0",
        "pytesseract>=0.3.0",
        "mss>=6.0.0",
        "pywin32>=300; sys_platform == 'win32'",
        "pyautogui>=0.9.0",
        "keyboard>=0.13.0"
    ]
    
    try:
        for package in requirements:
            print(f"Instalando {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        
        print(" Dependencias instaladas")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f" Error instalando dependencias: {e}")
        return False

def setup_directories():
    """Configurar directorios"""
    print("\n Configurando directorios...")
    
    directories = [
        "data/card_templates/pokerstars",
        "data/table_templates/pokerstars",
        "logs",
        "hand_history",
        "screenshots"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f" {directory}")
    
    return True

def download_templates():
    """Descargar templates de cartas para PokerStars"""
    print("\n  Descargando templates para PokerStars...")
    
    # Crear script para descargar templates
    download_script = '''
import os
import requests
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_basic_templates():
    """Crear templates básicos para PokerStars"""
    print("Creando templates básicos...")
    
    template_dir = "data/card_templates/pokerstars"
    
    # Rangos y palos
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    suit_symbols = {'hearts': '', 'diamonds': '', 'clubs': '', 'spades': ''}
    suit_colors = {'hearts': 'red', 'diamonds': 'red', 'clubs': 'black', 'spades': 'black'}
    
    for suit in suits:
        suit_dir = os.path.join(template_dir, suit)
        os.makedirs(suit_dir, exist_ok=True)
        
        for rank in ranks:
            # Crear imagen de carta
            img = Image.new('RGB', (70, 95), color='white')
            draw = ImageDraw.Draw(img)
            
            # Dibujar borde
            draw.rectangle([2, 2, 68, 93], outline='black', width=2)
            
            # Dibujar esquina superior izquierda
            color = suit_colors[suit]
            symbol = suit_symbols[suit]
            
            # Texto del rank
            try:
                font = ImageFont.truetype("arial.ttf", 14)
            except:
                font = ImageFont.load_default()
            
            draw.text((8, 8), rank, fill=color, font=font)
            draw.text((8, 25), symbol, fill=color, font=font)
            
            # Guardar
            filename = f"{rank}_{suit}.png"
            filepath = os.path.join(suit_dir, filename)
            img.save(filepath)
            
    print(f" Templates creados en {template_dir}")

if __name__ == "__main__":
    create_basic_templates()
'''
    
    with open("download_templates.py", "w", encoding="utf-8") as f:
        f.write(download_script)
    
    # Ejecutar script
    try:
        subprocess.run([sys.executable, "download_templates.py"], check=True)
        print(" Templates creados exitosamente")
        os.remove("download_templates.py")
        return True
    except Exception as e:
        print(f" Error creando templates: {e}")
        return False

def configure_tesseract():
    """Configurar Tesseract OCR"""
    print("\n Configurando Tesseract OCR...")
    
    system = platform.system()
    
    if system == "Windows":
        print("Para Windows, necesitas instalar Tesseract OCR manualmente:")
        print("1. Descarga de: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Instala en: C:\\Program Files\\Tesseract-OCR")
        print("3. Añade al PATH")
        print("\n  Continuando sin OCR completo...")
        return True
    elif system == "Linux":
        print("Ejecuta: sudo apt-get install tesseract-ocr")
        return True
    elif system == "Darwin":  # macOS
        print("Ejecuta: brew install tesseract")
        return True
    else:
        print(f"  Sistema {system} no soportado completamente")
        return True

def create_shortcut():
    """Crear acceso directo"""
    print("\n Creando scripts de ejecución...")
    
    # Script principal
    main_script = '''#!/usr/bin/env python3
"""
Poker Coach Pro - Script principal para PokerStars
"""
import os
import sys
from pathlib import Path

# Añadir src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    print("=" * 60)
    print(" POKER COACH PRO - POKERSTARS EDITION")
    print("=" * 60)
    
    print("\\n Iniciando sistema...")
    
    try:
        # Verificar si PokerStars está disponible
        from platforms.pokerstars_adapter import PokerStarsAdapter
        
        adapter = PokerStarsAdapter()
        
        print("\\n Verificando PokerStars...")
        if adapter.is_pokerstars_active():
            print(" PokerStars detectado - Modo tiempo real")
            
            # Importar y ejecutar coach
            from integration.improved_integrator import ImprovedPokerCoach
            coach = ImprovedPokerCoach()
            coach.start()
            
        else:
            print("  PokerStars no detectado")
            print("\\n Activando modo demo...")
            
            from integration.improved_integrator import ImprovedPokerCoach
            coach = ImprovedPokerCoach()
            coach.start()
            
    except ImportError as e:
        print(f"\\n Error: {e}")
        print("\\n Ejecuta el instalador primero: python install_pokerstars.py")
    except Exception as e:
        print(f"\\n Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
'''
    
    with open("start_pokerstars.py", "w", encoding="utf-8") as f:
        f.write(main_script)
    
    # Script de prueba
    test_script = '''#!/usr/bin/env python3
"""
Script de prueba para PokerStars
"""
import sys
import os
sys.path.insert(0, 'src')

print(" Probando PokerStars Adapter...")

try:
    from platforms.pokerstars_adapter import PokerStarsAdapter
    
    adapter = PokerStarsAdapter()
    print(" PokerStarsAdapter creado")
    
    # Verificar PokerStars
    is_active = adapter.is_pokerstars_active()
    print(f" PokerStars activo: {is_active}")
    
    # Probar captura
    if is_active:
        print("\\n Probando captura...")
        state = adapter.capture_and_analyze()
        if state:
            print(f" Estado capturado:")
            print(f"   Cartas: {state.hero_cards}")
            print(f"   Calle: {state.street}")
            print(f"   Pot: {state.pot}")
        else:
            print(" No se pudo capturar estado")
    else:
        print("  Ejecuta este script con PokerStars abierto")
        
except ImportError as e:
    print(f" Error de importación: {e}")
except Exception as e:
    print(f" Error: {e}")
    import traceback
    traceback.print_exc()
'''
    
    with open("test_pokerstars.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    print(" Scripts creados:")
    print("    start_pokerstars.py - Para iniciar el sistema")
    print("    test_pokerstars.py - Para probar la conexión")
    
    return True

def main():
    """Función principal de instalación"""
    print_header()
    
    steps = [
        ("Verificar Python", check_python_version),
        ("Instalar dependencias", install_dependencies),
        ("Configurar directorios", setup_directories),
        ("Crear templates", download_templates),
        ("Configurar OCR", configure_tesseract),
        ("Crear scripts", create_shortcut)
    ]
    
    all_success = True
    
    for step_name, step_func in steps:
        print(f"\n{'='*40}")
        print(f"PASO: {step_name}")
        print(f"{'='*40}")
        
        if not step_func():
            print(f" Falló: {step_name}")
            all_success = False
            break
    
    print("\n" + "=" * 60)
    
    if all_success:
        print(" INSTALACIÓN COMPLETADA EXITOSAMENTE!")
        print("\n PRÓXIMOS PASOS:")
        print("1. Asegúrate de tener PokerStars instalado y abierto")
        print("2. Ejecuta: python test_pokerstars.py")
        print("3. Si funciona, ejecuta: python start_pokerstars.py")
        print("\n Para modo demo (sin PokerStars):")
        print("   python run_coach.py")
    else:
        print(" INSTALACIÓN FALLÓ")
        print("\n Solución: Ejecuta cada paso manualmente")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
