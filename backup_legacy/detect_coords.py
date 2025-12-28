import mss
import cv2
import numpy as np
import json
import time
import os

print(" DETECTOR DE COORDENADAS POKERSTARS")
print("=" * 60)
print("INSTRUCCIONES:")
print("1. Abre PokerStars en una mesa")
print("2. Asegúrate que la ventana sea visible")
print("3. Este script detectará automáticamente la mesa")
print("=" * 60)

def detect_green_table():
    """Detectar mesas por color verde"""
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        
        print(f"📏 Resolución de pantalla: {monitor['width']}x{monitor['height']}")
        
        for attempt in range(5):
            print(f"\n Intento {attempt + 1}/5...")
            
            # Capturar pantalla
            screenshot = np.array(sct.grab(monitor))
            
            # Convertir a HSV
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # Detectar verde (mesas de PokerStars)
            lower_green = np.array([35, 50, 50])
            upper_green = np.array([85, 255, 255])
            mask = cv2.inRange(hsv, lower_green, upper_green)
            
            # Encontrar contornos
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            tables = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                area = w * h
                
                # Filtrar solo áreas grandes (mesas)
                if area > 100000:  # Más de 100k píxeles
                    tables.append({
                        "x": x, "y": y, "w": w, "h": h, "area": area
                    })
            
            if tables:
                # Ordenar por área (la más grande probablemente es la mesa activa)
                tables.sort(key=lambda t: t["area"], reverse=True)
                main_table = tables[0]
                
                print(f"✅ ¡MESA DETECTADA!")
                print(f"   Posición: [{main_table['x']}, {main_table['y']}]")
                print(f"   Tamaño: {main_table['w']}x{main_table['h']}")
                print(f"   Área: {main_table['area']:,} píxeles")
                
                # Calcular regiones de interés
                regions = calculate_regions(main_table)
                
                # Guardar configuración
                config = {
                    "screen_resolution": f"{monitor['width']}x{monitor['height']}",
                    "detected_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "pokerstars_regions": {
                        "mesa": [main_table["x"], main_table["y"], main_table["w"], main_table["h"]],
                        "cartas_hero": [
                            [main_table["x"] + main_table["w"]//2 - 75, main_table["y"] + main_table["h"] - 100, 70, 95],
                            [main_table["x"] + main_table["w"]//2 + 5, main_table["y"] + main_table["h"] - 100, 70, 95]
                        ],
                        "cartas_comunitarias": [
                            [main_table["x"] + 50, main_table["y"] + main_table["h"]//2 - 40, 70, 95],
                            [main_table["x"] + 130, main_table["y"] + main_table["h"]//2 - 40, 70, 95],
                            [main_table["x"] + 210, main_table["y"] + main_table["h"]//2 - 40, 70, 95],
                            [main_table["x"] + 290, main_table["y"] + main_table["h"]//2 - 40, 70, 95],
                            [main_table["x"] + 370, main_table["y"] + main_table["h"]//2 - 40, 70, 95]
                        ],
                        "pozo": [main_table["x"] + main_table["w"]//2 - 100, main_table["y"] + 100, 200, 40],
                        "bet": [main_table["x"] + main_table["w"]//2 - 75, main_table["y"] + main_table["h"] - 150, 150, 35]
                    }
                }
                
                # Crear directorio config si no existe
                os.makedirs("config", exist_ok=True)
                
                # Guardar archivo JSON
                with open("config/pokerstars_coords.json", "w") as f:
                    json.dump(config, f, indent=2)
                
                print(f"\n💾 Configuración guardada en: config/pokerstars_coords.json")
                print("\n🎯 ¡COORDENADAS LISTAS PARA MODO REAL!")
                
                # Mostrar preview de regiones
                print("\n📊 REGIONES CONFIGURADAS:")
                for region_name, region_coords in config["pokerstars_regions"].items():
                    if isinstance(region_coords[0], list):
                        print(f"   {region_name}: {len(region_coords)} posiciones")
                    else:
                        print(f"   {region_name}: {region_coords}")
                
                return True
            
            print(f"   No se detectaron mesas...")
            time.sleep(2)
    
    print("\n❌ No se pudo detectar PokerStars")
    print("\n💡 SOLUCIÓN:")
    print("   1. Asegúrate que PokerStars esté ABIERTO y VISIBLE")
    print("   2. La mesa debe estar en PRIMER PLANO")
    print("   3. Intenta mover la ventana a la pantalla principal")
    print("   4. Vuelve a ejecutar este script")
    return False

def calculate_regions(table):
    """Calcular regiones basadas en la mesa detectada"""
    regions = {}
    return regions

if __name__ == "__main__":
    detect_green_table()
