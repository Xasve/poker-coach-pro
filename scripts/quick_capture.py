"""
quick_capture.py - Captura rápida y simple de cartas
"""

import cv2
import numpy as np
import os
from pathlib import Path
import pyautogui
import time

def quick_capture():
    """Captura simple sin validación compleja"""
    print("🎴 CAPTURA RÁPIDA DE CARTAS")
    print("=" * 50)
    
    # Crear directorio
    output_dir = Path("data/card_templates/ggpoker")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\nINSTRUCCIONES SIMPLES:")
    print("1. Abre GG Poker")
    print("2. Cuando veas una carta...")
    print("3. Coloca el mouse SOBRE ella")
    print("4. Presiona la LETRA de la carta")
    print("   (ej: 'a' para Ace, 'k' para King)")
    print("5. Luego ingresa el suit (s, h, d, c)")
    print("6. Presiona 'q' para salir")
    
    print("\n📋 EJEMPLOS:")
    print("  Para 'Ace of hearts': Presiona 'a', luego 'h'")
    print("  Para 'King of spades': Presiona 'k', luego 's'")
    print("  Para 'Jack of clubs': Presiona 'j', luego 'c'")
    
    print("\n🎯 Listo? Presiona CUALQUIER TECLA para comenzar...")
    input()
    
    rank_map = {
        'a': 'A', 'k': 'K', 'q': 'Q', 'j': 'J',
        't': '10', '9': '9', '8': '8', '7': '7',
        '6': '6', '5': '5', '4': '4', '3': '3', '2': '2'
    }
    
    suit_map = {
        's': 's', 'h': 'h', 'd': 'd', 'c': 'c',
        'S': 's', 'H': 'h', 'D': 'd', 'C': 'c'
    }
    
    while True:
        print("\n🖱️  Coloca el mouse SOBRE la carta...")
        print("📝 Presiona LETRA del rank (a,k,q,j,t,9,8...) o 'q' para salir")
        
        rank_key = input("Rank: ").strip().lower()
        
        if rank_key == 'q':
            print("👋 Saliendo...")
            break
        
        if rank_key not in rank_map:
            print(f"❌ Rank inválido. Usa: {list(rank_map.keys())}")
            continue
        
        rank = rank_map[rank_key]
        
        print(f"✅ Rank: {rank}. Ahora ingresa el suit (s,h,d,c):")
        suit_key = input("Suit: ").strip().lower()
        
        if suit_key not in suit_map:
            print("❌ Suit inválido. Usa: s, h, d, c")
            continue
        
        suit = suit_map[suit_key]
        card_name = f"{rank}{suit}"
        
        print(f"\n📸 Capturando {card_name} en 2 segundos...")
        print("   (Asegúrate de que el mouse está SOBRE la carta)")
        time.sleep(2)
        
        try:
            # Capturar pantalla
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Posición del mouse
            mouse_x, mouse_y = pyautogui.position()
            
            # Extraer región (80x120 píxeles)
            card_w, card_h = 80, 120
            x1 = max(0, mouse_x - card_w // 2)
            y1 = max(0, mouse_y - card_h // 2)
            x2 = x1 + card_w
            y2 = y1 + card_h
            
            card_img = screenshot[y1:y2, x1:x2]
            
            if card_img.size == 0:
                print("❌ No se pudo capturar la carta")
                continue
            
            # Redimensionar si es necesario
            if card_img.shape[0] != card_h or card_img.shape[1] != card_w:
                card_img = cv2.resize(card_img, (card_w, card_h))
            
            # Convertir a escala de grises
            gray = cv2.cvtColor(card_img, cv2.COLOR_BGR2GRAY)
            
            # Mostrar preview
            cv2.imshow(f"Carta: {card_name}", gray)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
            
            # Preguntar confirmación
            print(f"\n¿Guardar {card_name}? (s/n)")
            confirm = input().strip().lower()
            
            if confirm == 's':
                # Guardar
                template_path = output_dir / f"{card_name}.png"
                cv2.imwrite(str(template_path), gray)
                print(f"✅ Guardado: {template_path}")
                
                # Verificar si existe
                if template_path.exists():
                    file_size = template_path.stat().st_size
                    print(f"📏 Tamaño: {file_size} bytes")
            else:
                print("⏭️  Saltando...")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n✅ Captura completada")

if __name__ == "__main__":
    quick_capture()