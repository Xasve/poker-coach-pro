"""
download_poker_cards.py - Descargar cartas de poker de internet automáticamente
"""

import cv2
import numpy as np
import requests
import os
from pathlib import Path
from typing import List, Dict
import json

class PokerCardDownloader:
    """Descargador automático de cartas de poker"""
    
    def __init__(self):
        self.sources = [
            {
                "name": "Wikimedia Commons",
                "base_url": "https://upload.wikimedia.org/wikipedia/commons/",
                "cards": {
                    "Ah": "a/a2/Playing_card_heart_A.svg",
                    "Kh": "9/9c/Playing_card_heart_K.svg",
                    "Qh": "5/5c/Playing_card_heart_Q.svg",
                    "Jh": "4/41/Playing_card_heart_J.svg",
                    "Th": "8/8a/Playing_card_heart_10.svg",
                    "9h": "7/72/Playing_card_heart_9.svg",
                    # Agregar más según necesidad
                }
            },
            {
                "name": "OpenClipart",
                "base_url": "https://openclipart.org/image/800px/",
                "cards": {
                    "As": "272226/Playing_card_spade_A",
                    "Ks": "272230/Playing_card_spade_K",
                    "Qs": "272234/Playing_card_spade_Q",
                    "Js": "272238/Playing_card_spade_J",
                    "Ts": "272242/Playing_card_spade_10",
                }
            }
        ]
        
    def download_all_cards(self, platform: str = "ggpoker"):
        """Descargar todas las cartas disponibles"""
        print(f"🌐 Descargando cartas para {platform}...")
        
        output_dir = Path(f"data/card_templates/{platform}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        downloaded = 0
        
        for source in self.sources:
            print(f"\n📡 Fuente: {source['name']}")
            
            for card_name, card_path in source['cards'].items():
                try:
                    # Construir URL
                    url = f"{source['base_url']}{card_path}"
                    
                    # Descargar
                    response = requests.get(url, timeout=10, stream=True)
                    
                    if response.status_code == 200:
                        # Convertir a imagen
                        img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
                        img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
                        
                        if img is not None:
                            # Redimensionar a tamaño estándar
                            img = cv2.resize(img, (80, 120))
                            
                            # Guardar
                            output_path = output_dir / f"{card_name}.png"
                            cv2.imwrite(str(output_path), img)
                            
                            downloaded += 1
                            print(f"  ✅ {card_name}")
                    else:
                        print(f"  ❌ {card_name} (HTTP {response.status_code})")
                        
                except Exception as e:
                    print(f"  ❌ {card_name}: {e}")
                    continue
        
        print(f"\n✅ Descargadas {downloaded} cartas")
        return downloaded
    
    def create_missing_cards(self, platform: str = "ggpoker"):
        """Crear cartas faltantes automáticamente"""
        print(f"\n🎨 Creando cartas faltantes para {platform}...")
        
        output_dir = Path(f"data/card_templates/{platform}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Todas las cartas posibles
        ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
        suits = ['h', 's', 'd', 'c']
        
        created = 0
        
        for rank in ranks:
            for suit in suits:
                card_name = f"{rank}{suit}"
                card_path = output_dir / f"{card_name}.png"
                
                # Solo crear si no existe
                if not card_path.exists():
                    # Crear carta básica
                    img = self._create_card_image(rank, suit)
                    
                    # Guardar
                    cv2.imwrite(str(card_path), img)
                    created += 1
                    print(f"  ✅ Creada: {card_name}")
        
        print(f"\n🎯 {created} cartas creadas automáticamente")
        return created
    
    def _create_card_image(self, rank: str, suit: str) -> np.ndarray:
        """Crear imagen de carta programáticamente"""
        # Crear imagen vacía
        img = np.zeros((120, 80), dtype=np.uint8)
        img.fill(50)  # Fondo gris
        
        # Determinar color basado en suit
        color = 255  # Blanco para spades y clubs
        if suit in ['h', 'd']:  # Corazones o Diamantes
            color = 200  # Gris claro
        
        # Dibujar borde
        cv2.rectangle(img, (5, 5), (75, 115), color, 2)
        
        # Símbolo del suit
        suit_symbol = {
            'h': '♥',
            's': '♠',
            'd': '♦',
            'c': '♣'
        }.get(suit, '?')
        
        # Texto de la carta
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = f"{rank}{suit_symbol}"
        
        # Tamaño del texto
        text_size = cv2.getTextSize(text, font, 0.6, 2)[0]
        text_x = (80 - text_size[0]) // 2
        text_y = (120 + text_size[1]) // 2
        
        # Dibujar texto
        cv2.putText(img, text, (text_x, text_y), font, 0.6, color, 2)
        
        return img

def main():
    """Función principal"""
    print("=" * 60)
    print("🌐 DESCARGADOR AUTOMÁTICO DE CARTAS DE POKER")
    print("=" * 60)
    
    downloader = PokerCardDownloader()
    
    print("\nSelecciona plataforma:")
    print("1. GG Poker")
    print("2. PokerStars")
    print("3. Ambas")
    
    choice = input("\nOpción (1-3): ").strip()
    
    platforms = []
    if choice == "1":
        platforms = ["ggpoker"]
    elif choice == "2":
        platforms = ["pokerstars"]
    else:
        platforms = ["ggpoker", "pokerstars"]
    
    total_downloaded = 0
    total_created = 0
    
    for platform in platforms:
        print(f"\n{'='*40}")
        print(f"PLATAFORMA: {platform.upper()}")
        print(f"{'='*40}")
        
        # Descargar de internet
        downloaded = downloader.download_all_cards(platform)
        total_downloaded += downloaded
        
        # Crear cartas faltantes
        created = downloader.create_missing_cards(platform)
        total_created += created
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL:")
    print(f"   Cartas descargadas de internet: {total_downloaded}")
    print(f"   Cartas creadas automáticamente: {total_created}")
    print(f"   Total: {total_downloaded + total_created}/52 cartas")
    print("\n✅ ¡Listo para jugar!")
    print("=" * 60)

if __name__ == "__main__":
    main()