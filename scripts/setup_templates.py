# scripts/setup_templates.py

import os
import shutil

def setup_pokerstars_templates():
    """Crear estructura de directorios para templates de PokerStars"""
    
    base_path = "data/card_templates/pokerstars"
    suits = ["hearts", "diamonds", "clubs", "spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    
    # Crear directorios
    for suit in suits:
        suit_path = os.path.join(base_path, suit)
        os.makedirs(suit_path, exist_ok=True)
        print(f"📁 Creado: {suit_path}")
        
        # Crear archivos placeholder
        for rank in ranks:
            placeholder_path = os.path.join(suit_path, f"{rank}.png.placeholder")
            with open(placeholder_path, 'w') as f:
                f.write(f"Template para {rank} of {suit}")
    
    print("✅ Estructura de templates creada")
    print("⚠️  Nota: Reemplaza los archivos .placeholder con imágenes reales de las cartas")

if __name__ == "__main__":
    setup_pokerstars_templates()