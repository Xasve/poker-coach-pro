import mss, cv2, numpy as np, os, time

print("📸 CAPTURA AUTOMÁTICA DE TEMPLATES DE CARTAS")
print("="*60)
print("INSTRUCCIONES:")
print("1. Abre PokerStars en una mesa")
print("2. Este script capturará cuando detecte cartas")
print("3. Mueve el mouse sobre cada carta para nombrarla")
print("="*60)

template_dir = "data/card_templates/pokerstars_real"
os.makedirs(f"{template_dir}/hearts", exist_ok=True)
os.makedirs(f"{template_dir}/diamonds", exist_ok=True)
os.makedirs(f"{template_dir}/clubs", exist_ok=True)
os.makedirs(f"{template_dir}/spades", exist_ok=True)

# Coordenadas aproximadas (ajustar según detección)
card_regions = [
    {"name": "hero_1", "pos": [870, 750, 70, 95], "suit": None, "rank": None},
    {"name": "hero_2", "pos": [950, 750, 70, 95], "suit": None, "rank": None},
    {"name": "flop_1", "pos": [750, 450, 70, 95], "suit": None, "rank": None},
    {"name": "flop_2", "pos": [830, 450, 70, 95], "suit": None, "rank": None},
    {"name": "flop_3", "pos": [910, 450, 70, 95], "suit": None, "rank": None},
]

print(f"\n🎯 Monitoreando {len(card_regions)} posiciones de cartas...")
print("   Presiona Ctrl+C para terminar")

try:
    with mss.mss() as sct:
        capture_count = 0
        while capture_count < 52:  # Máximo 52 cartas
            screenshot = np.array(sct.grab(sct.monitors[1]))
            
            for card in card_regions:
                x,y,w,h = card["pos"]
                if y+h < screenshot.shape[0] and x+w < screenshot.shape[1]:
                    card_img = screenshot[y:y+h, x:x+w]
                    
                    # Detectar si hay carta (basado en bordes/contraste)
                    gray = cv2.cvtColor(card_img, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray, 50, 150)
                    edge_ratio = np.sum(edges > 0) / (w*h)
                    
                    if edge_ratio > 0.05:  # Posible carta detectada
                        # Guardar para clasificación manual
                        filename = f"{template_dir}/uncategorized/card_{capture_count}.png"
                        os.makedirs(f"{template_dir}/uncategorized", exist_ok=True)
                        cv2.imwrite(filename, card_img)
                        capture_count += 1
                        print(f"📷 Capturada carta #{capture_count}: {filename}")
            
            time.sleep(0.5)
            
except KeyboardInterrupt:
    print(f"\n✅ Captura finalizada: {capture_count} cartas guardadas")
    print(f"📁 Revisa: {template_dir}/uncategorized/")
    print("💡 Clasifícalas manualmente en hearts/diamonds/clubs/spades")
