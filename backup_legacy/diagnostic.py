# diagnostic.py - Diagnóstico completo del sistema (REPARADO)
import os
import sys
import json

def print_header(text):
    print("\n" + "=" * 70)
    print(f"🔍 {text}")
    print("=" * 70)

def check_python_environment():
    """Verificar entorno Python"""
    print_header("VERIFICANDO ENTORNO PYTHON")
    
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Working directory: {os.getcwd()}")

def check_project_structure():
    """Verificar estructura del proyecto"""
    print_header("VERIFICANDO ESTRUCTURA DEL PROYECTO")
    
    required_paths = [
        ("data/", True),
        ("data/card_templates/", True),
        ("data/card_templates/auto_captured/", True),
        ("data/card_templates/pokerstars_real/", True),
        ("config/", True),
        ("src/", True),
        ("src/screen_capture/", False),
        ("src/card_detector.py", False),
    ]
    
    all_ok = True
    for path, required in required_paths:
        exists = os.path.exists(path)
        status = "✅" if exists else ("⚠️ " if not required else "❌")
        
        if required and not exists:
            all_ok = False
        
        print(f"   {status} {path}")
    
    return all_ok

def check_dataset_balance():
    """Verificar balance del dataset"""
    print_header("VERIFICANDO BALANCE DEL DATASET")
    
    sessions_path = "data/card_templates/auto_captured"
    if not os.path.exists(sessions_path):
        print("❌ No hay directorio de sesiones")
        return False
    
    sessions = [d for d in os.listdir(sessions_path) 
               if os.path.isdir(os.path.join(sessions_path, d))]
    
    if not sessions:
        print(" No hay sesiones de captura")
        return False
    
    print(f" Sesiones encontradas: {len(sessions)}")
    
    total_cards = 0
    total_red = 0
    
    print("\n📊 ANÁLISIS POR SESIÓN:")
    for session in sessions[:5]:  # Analizar solo 5 más recientes
        results_file = os.path.join(sessions_path, session, "classification_results.json")
        
        if os.path.exists(results_file):
            try:
                with open(results_file, 'r') as f:
                    data = json.load(f)
                
                if 'distribution' in data:
                    dist = data['distribution']
                    cards = sum(dist.values())
                    red_cards = dist.get('hearts', 0) + dist.get('diamonds', 0)
                    red_percentage = (red_cards / cards * 100) if cards > 0 else 0
                    
                    total_cards += cards
                    total_red += red_cards
                    
                    if red_percentage >= 30:
                        status = "✅"
                    elif red_percentage >= 10:
                        status = "⚠️ "
                    else:
                        status = "❌"
                    
                    print(f"   {status} {session:30} {cards:4} cartas | {red_percentage:5.1f}% rojas")
            except Exception as e:
                print(f"     {session:30} Error leyendo archivo: {e}")
    
    if total_cards > 0:
        red_percentage = (total_red / total_cards * 100)
        
        print(f"\n📈 ESTADÍSTICAS GLOBALES:")
        print(f"   Total cartas: {total_cards}")
        print(f"   Cartas rojas: {total_red} ({red_percentage:.1f}%)")
        print(f"   Cartas negras: {total_cards - total_red} ({100 - red_percentage:.1f}%)")
        
        if red_percentage == 0:
            print(f"\n PROBLEMA CRÍTICO: 0% cartas rojas")
            print(" Estás capturando en mesa PokerStars incorrecta")
            print("💡 Cambia a mesa 'Classic' (no 'Dark')")
            return False
        elif red_percentage < 30:
            print(f"\n⚠️  ADVERTENCIA: Solo {red_percentage:.1f}% cartas rojas")
            print(" Necesitas al menos 30% para buen entrenamiento")
            return False
        else:
            print(f"\n Dataset bien balanceado")
            return True
    else:
        print(" No hay cartas en las sesiones")
        return False

def check_scripts():
    """Verificar scripts importantes"""
    print_header("VERIFICANDO SCRIPTS IMPORTANTES")
    
    scripts = [
        ("smart_capture_fixed.py", True),
        ("verify_balance.py", True),
        ("main_integrated.py", True),
        ("start_auto_simple.py", False),
        ("session_manager.py", False),
        ("detect_coords.py", False),
    ]
    
    for script, required in scripts:
        exists = os.path.exists(script)
        status = "✅" if exists else ("⚠️ " if not required else "")
        
        if exists:
            # Verificar sintaxis
            try:
                import subprocess
                result = subprocess.run([sys.executable, "-m", "py_compile", script], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    status += " (sintaxis OK)"
                else:
                    status += " ( error sintaxis)"
            except:
                status += " (  no verificado)"
        
        print(f"   {status} {script}")

def check_pokerstars_config():
    """Verificar configuración de PokerStars"""
    print_header("VERIFICANDO CONFIGURACIÓN POKERSTARS")
    
    config_file = "config/pokerstars_coords.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            print(" Configuración encontrada")
            
            if "pokerstars_regions" in config:
                regions = config["pokerstars_regions"]
                print(f"   Regiones configuradas: {len(regions)}")
                
                for region_name, coords in regions.items():
                    print(f"    {region_name}: {coords}")
            
            return True
        except Exception as e:
            print(f" Error leyendo configuración: {e}")
            return False
    else:
        print(" No hay configuración de PokerStars")
        print(" Ejecuta: python detect_coords.py")
        return False

def main():
    """Función principal"""
    print(" POKER COACH PRO - DIAGNÓSTICO COMPLETO")
    print("=" * 70)
    
    # Ejecutar todas las verificaciones
    check_python_environment()
    structure_ok = check_project_structure()
    balance_ok = check_dataset_balance()
    check_scripts()
    config_ok = check_pokerstars_config()
    
    # Resumen
    print_header("RESUMEN DEL DIAGNÓSTICO")
    
    issues = []
    
    if not structure_ok:
        issues.append(" Estructura del proyecto incompleta")
    
    if not balance_ok:
        issues.append(" Dataset desbalanceado (pocas cartas rojas)")
    
    if not config_ok:
        issues.append(" No hay configuración de PokerStars")
    
    if issues:
        print(" PROBLEMAS ENCONTRADOS:")
        for issue in issues:
            print(f"   {issue}")
        
        print("\n SOLUCIONES RECOMENDADAS:")
        print("1. Si tienes 0% cartas rojas: Cambia a mesa PokerStars 'Classic'")
        print("2. Si no hay configuración: Ejecuta python detect_coords.py")
        print("3. Si falta estructura: Reclona el repositorio")
    else:
        print(" SISTEMA EN BUEN ESTADO")
        print("\n Puedes ejecutar: python main_integrated.py")

if __name__ == "__main__":
    main()
