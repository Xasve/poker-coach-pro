# run_poker_coach.py
import sys
import os
import time

def main():
    print("🎴 POKER COACH PRO - SISTEMA PRINCIPAL")
    print("=" * 60)
    
    # Verificar Python
    if sys.version_info < (3, 11):
        print("❌ Necesitas Python 3.11 o superior")
        return
    
    # Verificar dependencias
    print("\n1. Verificando dependencias...")
    try:
        import numpy as np
        import cv2
        from PIL import Image
        import mss
        
        print(f"   ✅ NumPy {np.__version__}")
        print(f"   ✅ OpenCV {cv2.__version__}")
        print(f"   ✅ Pillow {Image.__version__}")
    except ImportError as e:
        print(f"   ❌ Dependencia faltante: {e}")
        return
    
    # Verificar estructura
    print("\n2. Verificando estructura...")
    required = ['src', 'config', 'data/card_templates/pokerstars']
    for dir in required:
        if os.path.exists(dir):
            print(f"   ✅ {dir}/")
        else:
            print(f"   ❌ {dir}/ (faltante)")
    
    # Importar sistema
    print("\n3. Inicializando sistema...")
    sys.path.insert(0, 'src')
    
    try:
        from integration.poker_coach_integrator import PokerCoachIntegrator
        
        # Crear integrador
        config_path = 'config/default_config.yaml'
        if not os.path.exists(config_path):
            print(f"   ⚠️  Config no encontrada, usando valores por defecto")
            config_path = None
        
        integrator = PokerCoachIntegrator(config_path=config_path)
        
        # Inicializar
        if integrator.initialize():
            print("   ✅ Sistema inicializado")
        else:
            print("   ❌ Falló inicialización")
            return
        
        # Ciclo principal
        print("\n4. Iniciando ciclo principal...")
        print("   Presiona Ctrl+C para detener")
        print("=" * 60)
        
        try:
            iteration = 0
            while True:
                iteration += 1
                print(f"\n🔄 Iteración {iteration}")
                
                result = integrator.run_single_iteration()
                if result:
                    print(f"   ✅ Análisis completado")
                else:
                    print(f"   ⚠️  Sin datos de mesa")
                
                time.sleep(1)  # Esperar 1 segundo
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Deteniendo por usuario...")
        
        finally:
            print("\n5. Limpiando...")
            integrator.cleanup()
            print("✅ Sistema detenido correctamente")
            
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("🎴 POKER COACH PRO FINALIZADO")

if __name__ == "__main__":
    main()