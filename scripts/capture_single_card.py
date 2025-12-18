"""
capture_single_card.py - Captura rápida de una carta individual
"""

import cv2
import numpy as np
import os
import sys
from pathlib import Path

def capture_single_card():
    """Capturar una sola carta manualmente"""
    print("🎴 CAPTURA RÁPIDA DE CARTA")
    print("=" * 40)
    
    # Crear directorio si no existe
    output_dir = Path("data/card_templates/ggpoker")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Capturar pantalla
    print("\n1. Abre GG Poker/PokerStars")
    print("2. Coloca UNA carta visible en la pantalla")
    print("3. Presiona ESPACIO para capturar")
    print("4. Ingresa el nombre de la carta (ej: Ah, Ks)")
    print("\nPresiona ESPACIO para comenzar...")
    
    input("Presiona Enter cuando estés listo...")
    
    try:
        # Usar pyautogui para captura simple
        import pyautogui
        
        print("\n📸 Capturando en 3 segundos...")
        import time
        time.sleep(3)
        
        # Capturar pantalla
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Preguntar por región
        print("\n🖱️  Ahora selecciona la región de la carta:")
        print("   Haz clic y arrastra para seleccionar la carta")
        
        # Usar ROI selector de OpenCV
        roi = cv2.selectROI("Selecciona la carta", screenshot, showCrosshair=True)
        cv2.destroyAllWindows()
        
        if roi[2] > 0 and roi[3] > 0:
            x, y, w, h = roi
            
            # Extraer carta
            card_img = screenshot[y:y+h, x:x+w]
            
            # Redimensionar
            card_img = cv2.resize(card_img, (80, 120))
            
            # Convertir a escala de grises
            gray = cv2.cvtColor(card_img, cv2.COLOR_BGR2GRAY)
            
            # Mostrar preview
            cv2.imshow("Preview de la carta", gray)
            cv2.waitKey(1000)
            
            # Preguntar nombre
            card_name = input("\n📝 Nombre de la carta (ej: Ah, Ks, Qd): ").strip().upper()
            
            if len(card_name) >= 2:
                # Guardar
                template_path = output_dir / f"{card_name}.png"
                cv2.imwrite(str(template_path), gray)
                
                print(f"✅ Template guardado: {template_path}")
            else:
                print("❌ Nombre inválido")
        
        cv2.destroyAllWindows()
        
    except ImportError:
        print("❌ Instala pyautogui: pip install pyautogui")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    capture_single_card()