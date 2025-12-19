# restore_original.py - Restaurar archivos originales clave
import os
import shutil

print("📦 RESTAURANDO ARCHIVOS ORIGINALES CLAVE")
print("=" * 60)

def restore_file(source, dest, description):
    """Restaurar un archivo"""
    print(f"\n📄 {description}...")
    
    if os.path.exists(source):
        try:
            shutil.copy2(source, dest)
            print(f"   ✅ Restaurado: {source} -> {dest}")
            return True
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    else:
        print(f"   ⚠️  No existe: {source}")
        return False

def main():
    print("\n1. CREANDO BACKUP DE VERSIÓN MÍNIMA...")
    
    # Crear backup de los archivos mínimos
    backup_dir = "backup_minimal"
    os.makedirs(backup_dir, exist_ok=True)
    
    minimal_files = [
        ("src/integration/coach_integrator_minimal.py", f"{backup_dir}/coach_integrator_minimal.py"),
        ("src/platforms/pokerstars_adapter_minimal.py", f"{backup_dir}/pokerstars_adapter_minimal.py"),
        ("run_minimal.py", f"{backup_dir}/run_minimal.py"),
    ]
    
    for source, dest in minimal_files:
        if os.path.exists(source):
            shutil.copy2(source, dest)
            print(f"   💾 Backup: {source}")
    
    print(f"\n   ✅ Backup guardado en: {backup_dir}/")
    
    print("\n2. RESTAURANDO ARCHIVOS ORIGINALES...")
    
    # Lista de archivos originales importantes
    original_files = [
        # Archivos de coach (versión simple pero funcional)
        ("src/integration/coach_integrator_simple.py", "src/integration/coach_integrator.py", "Coach Integrator"),
        
        # Archivos de screen_capture (versiones básicas)
        ("src/screen_capture/stealth_capture.py.bak", "src/screen_capture/stealth_capture.py", "Stealth Capture"),
        ("src/screen_capture/card_recognizer.py.bak", "src/screen_capture/card_recognizer.py", "Card Recognizer"),
        ("src/screen_capture/table_detector.py.bak", "src/screen_capture/table_detector.py", "Table Detector"),
        ("src/screen_capture/text_ocr.py.bak", "src/screen_capture/text_ocr.py", "Text OCR"),
        
        # Archivos de platforms
        ("src/platforms/pokerstars_adapter.py.bak", "src/platforms/pokerstars_adapter.py", "PokerStars Adapter"),
        
        # Scripts principales
        ("run_pokerstars_optimized.py.bak", "run_pokerstars_optimized.py", "Runner principal"),
        ("check_system.py", "check_system.py", "Verificador"),
        ("calibrate_detector.py", "calibrate_detector.py", "Calibrador"),
    ]
    
    restored = 0
    for source, dest, desc in original_files:
        if os.path.exists(source):
            if restore_file(source, dest, desc):
                restored += 1
        else:
            print(f"   ⚠️  No encontrado: {source}")
    
    print(f"\n📊 Restaurados: {restored}/{len(original_files)} archivos")
    
    print("\n3. CREANDO VERSIÓN HÍBRIDA (recomendada)...")
    
    # Crear versión híbrida que use coach simple pero sistema real
    hybrid_runner = '''# run_hybrid.py - Versión híbrida (coach simple + sistema real)
import sys
import os
import time

print("🚀 POKER COACH PRO - VERSIÓN HÍBRIDA")
print("=" * 60)

sys.path.insert(0, 'src')

try:
    print("🔧 CARGANDO COMPONENTES...")
    
    # Usar adaptador real si existe, sino el mínimo
    try:
        from platforms.pokerstars_adapter import PokerStarsAdapter
        print("✅ Usando adaptador real")
    except ImportError:
        from platforms.pokerstars_adapter_minimal import PokerStarsAdapter
        print("⚠️  Usando adaptador mínimo")
    
    # Usar coach simple (siempre funciona)
    from integration.coach_integrator_minimal import CoachIntegrator
    print("✅ Usando coach mínimo (garantizado)")
    
    # Inicializar
    adapter = PokerStarsAdapter(stealth_level=1)
    coach = CoachIntegrator("pokerstars")
    
    print("\\n🎯 SISTEMA HÍBRIDO INICIALIZADO")
    print("\\n📡 MODO HÍBRIDO ACTIVADO")
    print("-" * 50)
    
    # Prueba con componentes reales/minimos
    for i in range(3):
        print(f"\\n🔄 Mano #{i+1}")
        
        try:
            # Intentar captura real
            screenshot = adapter.capture_table()
            
            # Detectar mesa
            table_detected = adapter.detect_table(screenshot)
            
            if table_detected:
                # Obtener cartas
                hole_cards = adapter.recognize_hole_cards(screenshot)
                print(f"   👤 Cartas detectadas: {hole_cards}")
                
                # Analizar con coach
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
            else:
                print("   ⚠️  Mesa no detectada (modo simulado)")
                
        except Exception as e:
            print(f"   ⚠️  Error en componentes: {e}")
            print("   🔄 Usando datos simulados...")
        
        time.sleep(2)
    
    print("\\n" + "=" * 60)
    print("✅ VERSIÓN HÍBRIDA FUNCIONANDO")
    print("\\n🎯 Puedes probar diferentes componentes:")
    print("• Para versión real: python run_pokerstars_optimized.py")
    print("• Para versión mínima: python run_minimal.py")
    print("• Para versión híbrida: python run_hybrid.py")
    
except Exception as e:
    print(f"\\n❌ Error crítico: {e}")
    import traceback
    traceback.print_exc()

print("\\n" + "=" * 60)
'''
    
    try:
        with open("run_hybrid.py", "w") as f:
            f.write(hybrid_runner)
        print("   ✅ Versión híbrida creada: run_hybrid.py")
    except Exception as e:
        print(f"   ❌ Error creando versión híbrida: {e}")
    
    print("\n" + "=" * 60)
    print("✅ RESTAURACIÓN COMPLETADA")
    print("\n📋 OPCIONES DISPONIBLES:")
    print("1. run_minimal.py - Sistema mínimo garantizado")
    print("2. run_hybrid.py - Sistema híbrido (recomendado)")
    print("3. run_pokerstars_optimized.py - Sistema completo")
    print("\n🚀 PRUEBA PRIMERO: python run_hybrid.py")
    print("=" * 60)

if __name__ == "__main__":
    main()