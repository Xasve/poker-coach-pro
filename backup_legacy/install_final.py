# install_final.py
import subprocess
import sys
import os

def run_command(cmd, description):
    print(f"\n🔧 {description}...")
    print(f"   $ {cmd}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("   ✅ Completado")
        return True
    else:
        print(f"   ❌ Error: {result.stderr[:200]}")
        return False

def main():
    print("🎴 INSTALACIÓN FINAL - POKER COACH PRO")
    print("=" * 60)
    
    print("Este script instalará todas las dependencias necesarias")
    print("y configurará el sistema para ejecución.")
    print("\nPython detectado:", sys.version)
    
    # 1. Actualizar pip
    run_command("python -m pip install --upgrade pip", "Actualizando pip")
    
    # 2. Instalar dependencias
    dependencies = [
        "numpy==1.24.4",
        "opencv-python==4.9.0.80",
        "pillow==10.3.0",
        "mss==9.0.1",
        "pyyaml==6.0.1",
        "pyautogui==0.9.54",
        "pytesseract==0.3.10"
    ]
    
    for dep in dependencies:
        run_command(f"pip install {dep}", f"Instalando {dep}")
    
    # 3. Verificar estructura
    print("\n📁 Verificando estructura...")
    
    required_dirs = ['logs', 'debug', 'data/card_templates/pokerstars']
    for dir_path in required_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"   ✅ {dir_path}/")
    
    # 4. Crear archivos de configuración si no existen
    if not os.path.exists("config/default_config.yaml"):
        config_content = """# Configuración Poker Coach Pro
capture:
  stealth_level: MEDIUM
  interval: 2.0
  debug: false

platforms:
  default: pokerstars
  pokerstars:
    card_templates_path: "data/card_templates/pokerstars/"

engine:
  aggression: 1.2
  tightness: 0.9
  update_cache: true

overlay:
  enabled: false
  position: top_right

logging:
  level: INFO
  file: "logs/poker_coach.log"
"""
        
        os.makedirs("config", exist_ok=True)
        with open("config/default_config.yaml", "w") as f:
            f.write(config_content)
        print("   ✅ config/default_config.yaml creado")
    
    # 5. Test final
    print("\n🧪 Ejecutando test final...")
    
    test_code = '''
import sys
sys.path.insert(0, "src")

try:
    from platforms.pokerstars_adapter import PokerStarsAdapter
    from core.poker_engine import PokerEngine
    
    print("✅ Importación exitosa")
    print("✅ Sistema listo para ejecución")
    
    print("\\n🎯 Para ejecutar:")
    print("   python run_poker_coach_pro.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
'''
    
    with open("test_final_check.py", "w") as f:
        f.write(test_code)
    
    os.system("python test_final_check.py")
    os.remove("test_final_check.py")
    
    print("\n" + "=" * 60)
    print("✅ INSTALACIÓN COMPLETADA")
    print("\n📋 COMANDOS DISPONIBLES:")
    print("   python run_poker_coach_pro.py           # Sistema completo")
    print("   python run_poker_coach_pro.py --help    # Ver opciones")
    print("   python run_poker_coach_simple.py        # Versión simple")
    print("\n💡 CONSEJOS:")
    print("   1. Abre PokerStars antes de ejecutar")
    print("   2. Para modo real, coloca templates en data/card_templates/pokerstars/")
    print("   3. Usa Ctrl+C para detener el sistema")

if __name__ == "__main__":
    main()