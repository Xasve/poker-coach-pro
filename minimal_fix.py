# minimal_fix.py - Reparación mínima sin dependencias externas
import os
import sys

print("🔧 REPARACIÓN MÍNIMA DEL SISTEMA")
print("=" * 60)

def check_python():
    """Verificar Python básico"""
    print("\n1. VERIFICANDO PYTHON...")
    print(f"   Python: {sys.version}")
    print(f"   Directorio: {os.getcwd()}")
    return True

def create_minimal_structure():
    """Crear estructura mínima"""
    print("\n2. CREANDO ESTRUCTURA MÍNIMA...")
    
    # Directorios esenciales
    dirs = [
        "src",
        "src/platforms",
        "src/screen_capture", 
        "src/integration",
        "config",
        "debug",
        "logs"
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"   📁 Creado: {d}/")
    
    return True

def create_minimal_coach():
    """Crear coach mínimo funcional"""
    print("\n3. CREANDO COACH MÍNIMO...")
    
    coach_code = '''# coach_integrator_minimal.py - Coach mínimo funcional
class CoachIntegrator:
    def __init__(self, platform="pokerstars"):
        self.platform = platform
        print(f"🤖 Coach mínimo para {platform}")
    
    def analyze_hand(self, situation):
        # Análisis básico
        hole_cards = situation.get("hole_cards", [])
        
        if hole_cards and len(hole_cards) >= 2:
            # Evaluación simple
            card1 = hole_cards[0][0] if isinstance(hole_cards[0], tuple) else "?"
            card2 = hole_cards[1][0] if isinstance(hole_cards[1], tuple) else "?"
            
            # AA, KK, QQ, AK -> RAISE
            if card1 == "A" and card2 == "A":
                return {"primary_action": "RAISE", "confidence": 0.95, "reasoning": "Pocket Aces"}
            elif card1 == "K" and card2 == "K":
                return {"primary_action": "RAISE", "confidence": 0.90, "reasoning": "Pocket Kings"}
            elif card1 == "A" and card2 == "K":
                return {"primary_action": "RAISE", "confidence": 0.85, "reasoning": "Big Slick"}
            else:
                return {"primary_action": "FOLD", "confidence": 0.70, "reasoning": "Mano marginal"}
        
        return {"primary_action": "CHECK", "confidence": 0.5, "reasoning": "Sin información"}
    
    def set_strategy(self, name):
        return True
    
    def get_available_strategies(self):
        return ["minimal"]
    
    def get_session_stats(self):
        return {"hands_analyzed": 0}
    
    def save_session(self, filename=None):
        return True
'''
    
    try:
        with open("src/integration/coach_integrator_minimal.py", "w", encoding="utf-8") as f:
            f.write(coach_code)
        print("   ✅ Coach mínimo creado")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def create_minimal_adapter():
    """Crear adaptador mínimo"""
    print("\n4. CREANDO ADAPTADOR MÍNIMO...")
    
    adapter_code = '''# pokerstars_adapter_minimal.py - Adaptador mínimo
class PokerStarsAdapter:
    def __init__(self, stealth_level=1):
        self.platform = "pokerstars"
        self.stealth_level = stealth_level
        print(f"🎴 Adaptador mínimo para {self.platform}")
    
    def capture_table(self):
        print("📸 Captura simulada")
        return None
    
    def detect_table(self, screenshot):
        print("🔍 Detección simulada: SIEMPRE VERDADERO")
        return True
    
    def recognize_hole_cards(self, screenshot):
        # Cartas simuladas para pruebas
        return [("A", "hearts", 0.95), ("K", "spades", 0.90)]
    
    def recognize_community_cards(self, screenshot):
        return []
    
    def get_table_info(self, screenshot):
        return {"platform": self.platform, "table_detected": True}
'''
    
    try:
        with open("src/platforms/pokerstars_adapter_minimal.py", "w", encoding="utf-8") as f:
            f.write(adapter_code)
        print("   ✅ Adaptador mínimo creado")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def create_minimal_runner():
    """Crear ejecutor mínimo"""
    print("\n5. CREANDO EJECUTOR MÍNIMO...")
    
    runner_code = '''# run_minimal.py - Sistema mínimo funcional
import time
import sys
import os

print("🚀 POKER COACH PRO - VERSIÓN MÍNIMA")
print("=" * 60)

# Añadir src al path
sys.path.insert(0, 'src')

try:
    # Importar componentes mínimos
    from platforms.pokerstars_adapter_minimal import PokerStarsAdapter
    from integration.coach_integrator_minimal import CoachIntegrator
    
    print("✅ Componentes mínimos cargados")
    
    # Inicializar
    adapter = PokerStarsAdapter(stealth_level=1)
    coach = CoachIntegrator("pokerstars")
    
    print("\\n🎯 SISTEMA INICIALIZADO CORRECTAMENTE")
    print("\\n📡 MODO DE PRUEBA ACTIVADO")
    print("-" * 50)
    
    # Simular partida
    for i in range(5):
        print(f"\\n🔄 Mano #{i+1}")
        
        # Simular captura
        screenshot = adapter.capture_table()
        
        # Detectar mesa
        table_detected = adapter.detect_table(screenshot)
        
        if table_detected:
            # Obtener cartas
            hole_cards = adapter.recognize_hole_cards(screenshot)
            print(f"   👤 Tus cartas: {hole_cards}")
            
            # Analizar
            situation = {
                "hole_cards": hole_cards,
                "community_cards": [],
                "pot_size": 100,
                "bet_size": 20,
                "position": "BTN",
                "players": 6,
                "stage": "preflop"
            }
            
            recommendation = coach.analyze_hand(situation)
            print(f"   💡 Recomendación: {recommendation['primary_action']}")
            print(f"   📈 Confianza: {recommendation['confidence']:.0%}")
            print(f"   🧠 Razón: {recommendation['reasoning']}")
        
        time.sleep(1)
    
    print("\\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
    print("\\n🎯 El sistema base funciona correctamente")
    print("\\n🔧 Para la versión completa, instala:")
    print("   pip install numpy opencv-python mss")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
'''
    
    try:
        with open("run_minimal.py", "w", encoding="utf-8") as f:
            f.write(runner_code)
        print("   ✅ Ejecutor mínimo creado")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def create_config_files():
    """Crear archivos de configuración"""
    print("\n6. CREANDO CONFIGURACIÓN...")
    
    configs = {
        "config/settings.json": '{"stealth_level": 1, "capture_delay": 0.5}',
        "config/strategies.json": '{"default_strategy": "minimal"}'
    }
    
    for path, content in configs.items():
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(content)
            print(f"   📄 Creado: {path}")
        except Exception as e:
            print(f"   ⚠️  Error creando {path}: {e}")
    
    return True

def main():
    """Función principal"""
    print("\n" + "=" * 60)
    print("🎯 INICIANDO RECONSTRUCCIÓN MÍNIMA...")
    
    # Ejecutar pasos
    steps = [
        ("Verificar Python", check_python),
        ("Crear estructura", create_minimal_structure),
        ("Crear coach", create_minimal_coach),
        ("Crear adaptador", create_minimal_adapter),
        ("Crear ejecutor", create_minimal_runner),
        ("Crear configuración", create_config_files)
    ]
    
    for name, func in steps:
        print(f"\n▶️  {name.upper()}...")
        if not func():
            print(f"❌ Falló: {name}")
            return
    
    print("\n" + "=" * 60)
    print("✅ RECONSTRUCCIÓN COMPLETADA")
    print("\n📋 SISTEMA MÍNIMO CREADO:")
    print("• Coach básico funcional")
    print("• Adaptador simulado")
    print("• Ejecutor de prueba")
    print("• Estructura completa")
    
    print("\n🚀 EJECUTA AHORA:")
    print("   python run_minimal.py")
    
    print("\n🔧 PARA VERSIÓN COMPLETA:")
    print("   1. Asegúrate de tener Python 3.8+")
    print("   2. Ejecuta: pip install numpy opencv-python mss")
    print("   3. Copia los archivos originales de vuelta")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()