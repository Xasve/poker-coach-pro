#!/usr/bin/env python3
"""
VERIFICADOR SIMPLE - Poker Coach Pro
"""
import os
import sys

def check_file(filepath, description):
    """Verificar si un archivo existe"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - NO EXISTE")
        return False

def main():
    print("🔍 VERIFICACIÓN DEL SISTEMA")
    print("=" * 50)
    
    # Archivos críticos
    critical_files = [
        ("src/screen_capture/__init__.py", "Módulo screen_capture"),
        ("src/screen_capture/stealth_capture.py", "Capturador de pantalla"),
        ("src/screen_capture/table_detector.py", "Detector de mesa"),
        ("poker_coach.py", "Script principal"),
        ("requirements.txt", "Dependencias")
    ]
    
    all_ok = True
    for filepath, description in critical_files:
        if not check_file(filepath, description):
            all_ok = False
    
    # Verificar imports
    print("\n🔧 Probando importaciones...")
    sys.path.insert(0, 'src')
    
    try:
        import screen_capture
        print("✅ Importación de screen_capture - OK")
        
        from screen_capture.stealth_capture import StealthScreenCapture
        print("✅ Importación de StealthScreenCapture - OK")
        
        test = StealthScreenCapture()
        print("✅ Creación de instancia - OK")
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        all_ok = False
    except Exception as e:
        print(f"❌ Error: {e}")
        all_ok = False
    
    # Resultado
    print("\n" + "=" * 50)
    if all_ok:
        print("🎉 ¡SISTEMA VERIFICADO CORRECTAMENTE!")
        print("\n🚀 Ejecuta: python poker_coach.py")
    else:
        print("⚠️  HAY PROBLEMAS EN EL SISTEMA")
        print("\n💡 Solución: Ejecuta 'python fix_all.py'")
    print("=" * 50)

if __name__ == "__main__":
    main()