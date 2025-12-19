# capture_templates.py - Capturar templates reales de PokerStars
import sys
import os
import cv2
import numpy as np
import time

print("📸 CAPTURADOR DE TEMPLATES REALES PARA POKERSTARS")
print("=" * 60)

sys.path.insert(0, 'src')

try:
    from platforms.pokerstars_adapter import PokerStarsAdapter
    
    print("🔧 Inicializando sistema...")
    adapter = PokerStarsAdapter(stealth_level=1)
    
    print("\n🎮 INSTRUCCIONES:")
    print("1. Abre PokerStars y siéntate en una mesa")
    print("2. Juega algunas manos para ver diferentes cartas")
    print("3. El sistema capturará automáticamente")
    print("4. Presiona Ctrl+C para detener")
    print("\n⏳ Iniciando en 5 segundos...")
    time.sleep(5)
    
    # Directorio para templates
    templates_dir = "data/card_templates/pokerstars_captured"
    os.makedirs(templates_dir, exist_ok=True)
    
    # Contadores
    capture_count = 0
    saved_templates = 0
    
    print("\n📡 CAPTURANDO TEMPLATES EN TIEMPO REAL...")
    print("-" * 50)
    
    try:
        while True:
            capture_count += 1
            
            # Capturar pantalla
            screenshot = adapter.capture_table()
            if screenshot is None:
                time.sleep(0.5)
                continue
            
            # Detectar mesa
            if adapter.detect_table(screenshot):
                # Reconocer cartas
                hole_cards = adapter.recognize_hole_cards(screenshot)
                community_cards = adapter.recognize_community_cards(screenshot)
                
                # Mostrar lo detectado
                if capture_count % 10 == 0:
                    print(f"\n🔄 Captura #{capture_count}")
                    print(f"   Cartas propias: {hole_cards}")
                    print(f"   Mesa: {community_cards}")
                
                # Intentar guardar templates si reconocemos cartas
                self.save_detected_cards(screenshot, hole_cards, community_cards, templates_dir)
                
            time.sleep(0.3)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Captura detenida")
    
    print(f"\n📊 RESULTADOS:")
    print(f"   Capturas totales: {capture_count}")
    print(f"   Templates guardados: {saved_templates}")
    print(f"   Directorio: {templates_dir}/")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

def save_detected_cards(self, screenshot, hole_cards, community_cards, save_dir):
    """Guardar cartas detectadas como templates"""
    global saved_templates
    
    # Posiciones de cartas (ajustar según tu calibración)
    positions = {
        "hole": [(850, 930, 71, 96), (1000, 930, 71, 96)],
        "community": [(780, 480, 71, 96), (870, 480, 71, 96), 
                     (960, 480, 71, 96), (1050, 480, 71, 96), 
                     (1140, 480, 71, 96)]
    }
    
    # Guardar hole cards
    for i, card_info in enumerate(hole_cards):
        if len(card_info) >= 3 and card_info[0] != "?" and card_info[1] != "?":
            value, suit, confidence = card_info
            if confidence > 0.7:  # Solo si confianza alta
                x, y, w, h = positions["hole"][i]
                card_img = screenshot[y:y+h, x:x+w]
                
                # Crear directorio para el palo
                suit_dir = os.path.join(save_dir, suit)
                os.makedirs(suit_dir, exist_ok=True)
                
                # Guardar imagen
                filename = os.path.join(suit_dir, f"{value}.png")
                cv2.imwrite(filename, card_img)
                saved_templates += 1
                print(f"💾 Template guardado: {value}{suit[0].upper()} ({confidence:.0%})")