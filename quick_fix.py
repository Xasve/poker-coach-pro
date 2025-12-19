# quick_fix.py - Solución rápida para 100% cartas negras
import os
import shutil

print(" SOLUCIÓN RÁPIDA PARA 100% CARTAS NEGRAS")
print("=" * 70)

# 1. Eliminar sesión problemática
sessions_path = "data/card_templates/auto_captured"
if os.path.exists(sessions_path):
    sessions = os.listdir(sessions_path)
    
    # Buscar sesiones con 100% spades
    for session in sessions:
        session_path = os.path.join(sessions_path, session)
        results_file = os.path.join(session_path, "classification_results.json")
        
        if os.path.exists(results_file):
            import json
            try:
                with open(results_file, 'r') as f:
                    data = json.load(f)
                
                if 'distribution' in data:
                    dist = data['distribution']
                    total = sum(dist.values())
                    spades = dist.get('spades', 0)
                    
                    if total > 0 and spades / total > 0.95:  # Más del 95% spades
                        print(f"  Eliminando sesión problemática: {session}")
                        shutil.rmtree(session_path)
            except:
                pass

print("\n Sesiones problemáticas eliminadas")
print("\n AHORA SIGUE ESTOS PASOS:")
print("1. CERRAR PokerStars completamente")
print("2. ABRIR PokerStars de nuevo")
print("3. BUSCAR mesa 'NL Holdem Classic' (NO 'Dark')")
print("4. ESPERAR a ver cartas ROJAS")
print("5. Ejecutar: python detect_coords.py")
print("6. Luego: python smart_capture_fixed.py")

print("\n Cómo saber si es mesa correcta?")
print("   - Busca 'Classic' en el nombre")
print("   - El fondo debe ser CLARO (no oscuro)")
print("   - Debes VER cartas rojas con tus ojos")

input("\nPresiona Enter para continuar...")
