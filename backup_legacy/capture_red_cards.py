# capture_red_cards.py
import os
import time
from datetime import datetime

print(" CAPTURA ENFOCADA EN CARTAS ROJAS (Corazones y Diamantes)")
print("=" * 70)
print("Este script te ayudará a capturar más cartas rojas para balancear")
print("=" * 70)

def show_instructions():
    print("\n INSTRUCCIONES PARA CARTAS ROJAS:")
    print("   1. Busca mesas con fondo CLARO en PokerStars")
    print("   2. Las cartas rojas se ven mejor sobre fondos claros")
    print("   3. Juega en mesas con estilo 'Classic' o 'Modern'")
    print("   4. Aumenta el brillo de tu monitor temporalmente")
    print("   5. Enfócate en ver cartas con  y ")

def create_red_focused_session():
    """Crear sesión enfocada en cartas rojas"""
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S_red_focus")
    session_path = f"data/card_templates/auto_captured/{session_id}"
    
    os.makedirs(os.path.join(session_path, "raw_captures"), exist_ok=True)
    os.makedirs(os.path.join(session_path, "reports"), exist_ok=True)
    
    # Crear instrucciones específicas
    instructions = {
        "session_id": session_id,
        "focus": "red_cards",
        "created_at": datetime.now().isoformat(),
        "tips": [
            "Use light-colored tables",
            "Increase screen brightness",
            "Look for hearts and diamonds",
            "Capture community cards (often show suits clearly)"
        ]
    }
    
    import json
    with open(os.path.join(session_path, "session_info.json"), 'w') as f:
        json.dump(instructions, f, indent=2)
    
    print(f"\n Sesión creada: {session_id}")
    print("    Ruta: " + session_path)
    
    return session_path

def main():
    show_instructions()
    
    print("\n OBJETIVO: Capturar 50+ cartas rojas")
    print("   Actual: =8, =7  |  Necesario: =40, =40")
    
    response = input("\nCrear sesión enfocada en cartas rojas? (s/n): ")
    
    if response.lower() == 's':
        session_path = create_red_focused_session()
        
        print("\n EJECUTA ESTO EN OTRA TERMINAL:")
        print(f"   python src/auto_template_capturer.py")
        print("\n CONSEJOS DURANTE CAPTURA:")
        print("    Juega en mesas CLARAS/AMARILLAS")
        print("    Mira el flop (cartas comunitarias)")
        print("    Las cartas rojas tienen símbolos rojos ")
        
        # Sugerir configuración de PokerStars
        print("\n CONFIGURACIÓN RECOMENDADA POKERSTARS:")
        print("   1. Mesa: 'Modern' o 'Classic' style")
        print("   2. Color de fondo: Claro/Amarillo")
        print("   3. Tamaño de cartas: Normal o Grande")
        print("   4. Velocidad: 'Fast-Fold' para más manos")
    
    print("\n" + "=" * 70)
    print(" Recuerda: Cartas ROJAS =  Corazones y  Diamantes")
    print("=" * 70)

if __name__ == "__main__":
    main()
