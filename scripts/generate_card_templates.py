"""
generate_card_templates.py - Generador de templates reales de cartas para poker
Captura screenshots de cartas reales y las guarda como templates
"""

import cv2
import numpy as np
import os
import time
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple
import pyautogui
from mss import mss
import keyboard

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CardTemplateGenerator:
    """Generador de templates de cartas para poker"""
    
    def __init__(self, platform: str = "ggpoker"):
        """
        Inicializar generador de templates
        
        Args:
            platform: 'ggpoker' o 'pokerstars'
        """
        self.platform = platform.lower()
        self.sct = mss()
        
        # Configuraciones por plataforma
        self.configs = {
            "ggpoker": {
                "card_size": (80, 120),  # Ancho, Alto
                "card_spacing": 25,  # Espacio entre cartas
                "table_color_range": [(30, 30, 30), (80, 80, 80)],  # Rango de color de fondo
                "screenshot_delay": 1.0,  # Delay entre capturas
                "output_dir": "data/card_templates/ggpoker"
            },
            "pokerstars": {
                "card_size": (75, 115),
                "card_spacing": 20,
                "table_color_range": [(20, 60, 20), (50, 100, 50)],  # Verde típico
                "screenshot_delay": 1.0,
                "output_dir": "data/card_templates/pokerstars"
            }
        }
        
        self.config = self.configs.get(self.platform, self.configs["ggpoker"])
        self.output_dir = Path(self.config["output_dir"])
        
        # Crear directorio de salida
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Todas las cartas posibles
        self.ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
        self.suits = ['s', 'h', 'd', 'c']  # spades, hearts, diamonds, clubs
        
        logger.info(f"Generador de templates inicializado para {platform}")
        logger.info(f"Directorio de salida: {self.output_dir}")
    
    def capture_screen(self) -> np.ndarray:
        """Capturar pantalla completa"""
        try:
            # Capturar pantalla principal
            monitor = self.sct.monitors[1]  # Monitor principal
            screenshot = self.sct.grab(monitor)
            
            # Convertir a numpy array
            img = np.array(screenshot)
            
            # Convertir BGRA a BGR si es necesario
            if img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            return img
            
        except Exception as e:
            logger.error(f"Error capturando pantalla: {e}")
            return None
    
    def find_card_positions(self, screenshot: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Encontrar posiciones de cartas en la pantalla
        
        Returns:
            Lista de rectángulos (x, y, w, h) donde están las cartas
        """
        try:
            # Convertir a HSV para mejor detección de colores
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # Crear máscara para colores de cartas (blanco/amarillo típico)
            # Para cartas claras sobre fondo oscuro
            lower_white = np.array([0, 0, 150])
            upper_white = np.array([180, 30, 255])
            
            mask = cv2.inRange(hsv, lower_white, upper_white)
            
            # Operaciones morfológicas para limpiar la máscara
            kernel = np.ones((3, 3), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            
            # Encontrar contornos
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            card_positions = []
            min_area = 500  # Área mínima para una carta
            max_area = 5000  # Área máxima para una carta
            
            for contour in contours:
                area = cv2.contourArea(contour)
                
                if min_area < area < max_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Filtrar por relación de aspecto (cartas ~2:3)
                    aspect_ratio = h / w
                    if 1.2 < aspect_ratio < 2.0:
                        card_positions.append((x, y, w, h))
            
            # Ordenar por posición X (de izquierda a derecha)
            card_positions.sort(key=lambda rect: rect[0])
            
            logger.info(f"Encontradas {len(card_positions)} posibles cartas")
            return card_positions
            
        except Exception as e:
            logger.error(f"Error encontrando cartas: {e}")
            return []
    
    def extract_card_image(self, screenshot: np.ndarray, position: Tuple[int, int, int, int]) -> np.ndarray:
        """
        Extraer y preprocesar imagen de una carta
        
        Args:
            screenshot: Imagen completa
            position: (x, y, w, h) de la carta
            
        Returns:
            Imagen de la carta preprocesada
        """
        x, y, w, h = position
        
        # Extraer la región de la carta
        card_img = screenshot[y:y+h, x:x+w]
        
        if card_img.size == 0:
            return None
        
        # Redimensionar a tamaño estándar
        target_size = self.config["card_size"]
        card_img = cv2.resize(card_img, target_size)
        
        # Convertir a escala de grises
        gray = cv2.cvtColor(card_img, cv2.COLOR_BGR2GRAY)
        
        # Aplicar umbral adaptativo
        thresh = cv2.adaptiveThreshold(gray, 255, 
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY_INV, 11, 2)
        
        return thresh
    
    def manual_template_capture(self):
        """Modo manual para capturar templates"""
        print("\n" + "=" * 60)
        print("🎴 MODO MANUAL DE CAPTURA DE TEMPLATES")
        print("=" * 60)
        
        print("\nINSTRUCCIONES:")
        print("1. Abre GG Poker o PokerStars en una mesa")
        print("2. Asegúrate de que las cartas sean visibles")
        print("3. Para CADA carta:")
        print("   - Presiona ESPACIO cuando la carta esté centrada")
        print("   - Ingresa el valor (ej: Ah, Ks, Qd)")
        print("4. Presiona ESC para terminar")
        print("\nPresiona ESPACIO para comenzar...")
        
        keyboard.wait('space')
        
        templates_captured = 0
        
        while True:
            print(f"\n[{templates_captured}/52] Preparado para capturar carta...")
            print("Coloca el mouse sobre la carta y presiona ESPACIO")
            print("Presiona ESC para terminar")
            
            try:
                # Esperar a que presionen espacio
                keyboard.wait('space')
                
                # Obtener posición del mouse
                mouse_x, mouse_y = pyautogui.position()
                logger.info(f"Posición del mouse: ({mouse_x}, {mouse_y})")
                
                # Capturar región alrededor del mouse
                screenshot = self.capture_screen()
                if screenshot is None:
                    print("❌ Error capturando pantalla")
                    continue
                
                # Definir región alrededor del mouse (tamaño de carta)
                card_w, card_h = self.config["card_size"]
                region_x = max(0, mouse_x - card_w // 2)
                region_y = max(0, mouse_y - card_h // 2)
                
                # Extraer la carta
                card_region = (region_x, region_y, card_w, card_h)
                card_img = self.extract_card_image(screenshot, card_region)
                
                if card_img is None:
                    print("❌ No se pudo extraer la carta")
                    continue
                
                # Mostrar preview
                cv2.imshow("Preview de la carta", card_img)
                cv2.waitKey(100)  # Mostrar por 100ms
                
                # Preguntar por el nombre de la carta
                card_name = input("Ingresa el nombre de la carta (ej: Ah, Ks, Qd): ").strip().upper()
                
                if len(card_name) >= 2:
                    # Validar formato básico
                    rank = card_name[:-1]
                    suit = card_name[-1]
                    
                    if rank in self.ranks and suit in self.suits:
                        # Guardar template
                        template_path = self.output_dir / f"{card_name}.png"
                        cv2.imwrite(str(template_path), card_img)
                        
                        templates_captured += 1
                        print(f"✅ Template guardado: {card_name}")
                        
                        # Mostrar estadísticas
                        remaining = 52 - templates_captured
                        print(f"📊 Progreso: {templates_captured}/52 ({remaining} restantes)")
                    else:
                        print("❌ Nombre inválido. Formato: RankSuit (ej: Ah, Ks)")
                else:
                    print("❌ Nombre demasiado corto")
                    
                cv2.destroyAllWindows()
                
            except keyboard.KeyboardInterrupt:
                print("\n⏹️  Captura interrumpida por el usuario")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
        
        print(f"\n✅ Captura completada. Templates guardados: {templates_captured}")
        return templates_captured
    
    def auto_detect_and_save(self, screenshot: np.ndarray, card_names: List[str]):
        """
        Detectar cartas automáticamente y guardarlas con nombres específicos
        
        Args:
            screenshot: Imagen de la pantalla
            card_names: Lista de nombres de cartas (ej: ['Ah', 'Ks', 'Qd'])
        """
        positions = self.find_card_positions(screenshot)
        
        if len(positions) != len(card_names):
            logger.warning(f"Cartas detectadas: {len(positions)}, Nombres proporcionados: {len(card_names)}")
            return
        
        for i, (position, card_name) in enumerate(zip(positions, card_names)):
            try:
                # Extraer y preprocesar carta
                card_img = self.extract_card_image(screenshot, position)
                
                if card_img is not None:
                    # Guardar template
                    template_path = self.output_dir / f"{card_name}.png"
                    cv2.imwrite(str(template_path), card_img)
                    
                    logger.info(f"✅ Template guardado: {card_name}")
                    
                    # Mostrar preview
                    cv2.imshow(f"Carta {i+1}: {card_name}", card_img)
                    cv2.waitKey(300)  # Mostrar por 300ms
                    
            except Exception as e:
                logger.error(f"Error procesando carta {card_name}: {e}")
        
        cv2.destroyAllWindows()
    
    def create_sample_templates(self):
        """Crear templates de muestra básicos (para desarrollo)"""
        print("\nCreando templates de muestra básicos...")
        
        samples = ['Ah', 'Ks', 'Qd', 'Jc', '10h', '9s', '8d', '7c']
        
        for card_name in samples:
            # Crear imagen simple
            img = np.zeros(self.config["card_size"][::-1], dtype=np.uint8)  # Nota: (alto, ancho)
            
            # Rellenar con color de fondo
            img.fill(50)
            
            # Dibujar borde
            cv2.rectangle(img, (5, 5), (self.config["card_size"][0]-6, self.config["card_size"][1]-6), 200, 2)
            
            # Añadir texto
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_size = cv2.getTextSize(card_name, font, 0.7, 2)[0]
            text_x = (self.config["card_size"][0] - text_size[0]) // 2
            text_y = (self.config["card_size"][1] + text_size[1]) // 2
            
            cv2.putText(img, card_name, (text_x, text_y), font, 0.7, 255, 2)
            
            # Guardar
            template_path = self.output_dir / f"{card_name}.png"
            cv2.imwrite(str(template_path), img)
            
            print(f"  ✅ Template de muestra: {card_name}")
        
        print(f"\n✅ {len(samples)} templates de muestra creados en {self.output_dir}")
    
    def verify_templates(self) -> Dict:
        """Verificar templates existentes y generar reporte"""
        templates_found = []
        missing_templates = []
        
        for rank in self.ranks:
            for suit in self.suits:
                card_name = f"{rank}{suit}"
                template_path = self.output_dir / f"{card_name}.png"
                
                if template_path.exists():
                    templates_found.append(card_name)
                else:
                    missing_templates.append(card_name)
        
        # Generar reporte
        report = {
            "platform": self.platform,
            "total_possible": 52,
            "templates_found": len(templates_found),
            "missing_templates": len(missing_templates),
            "completion_percentage": (len(templates_found) / 52) * 100,
            "found_templates": templates_found,
            "missing_templates_list": missing_templates
        }
        
        return report
    
    def generate_template_map(self):
        """Generar archivo JSON con mapeo de templates"""
        template_map = {}
        
        for rank in self.ranks:
            for suit in self.suits:
                card_name = f"{rank}{suit}"
                template_path = self.output_dir / f"{card_name}.png"
                
                if template_path.exists():
                    # Leer imagen y extraer características
                    img = cv2.imread(str(template_path), cv2.IMREAD_GRAYSCALE)
                    
                    if img is not None:
                        template_map[card_name] = {
                            "path": str(template_path.relative_to("data/card_templates")),
                            "size": img.shape[::-1],  # (ancho, alto)
                            "mean_intensity": float(np.mean(img)),
                            "hash": self._image_hash(img)
                        }
        
        # Guardar mapa
        map_path = self.output_dir / "template_map.json"
        with open(map_path, 'w') as f:
            json.dump(template_map, f, indent=2)
        
        logger.info(f"Mapa de templates guardado: {map_path}")
        return template_map
    
    def _image_hash(self, image: np.ndarray) -> str:
        """Generar hash simple de la imagen"""
        # Redimensionar a 8x8
        small = cv2.resize(image, (8, 8))
        
        # Calcular promedio
        avg = np.mean(small)
        
        # Crear hash binario
        hash_str = ''.join(['1' if pixel > avg else '0' for pixel in small.flatten()])
        
        return hash_str

def main():
    """Función principal"""
    print("=" * 60)
    print("🎴 POKER COACH PRO - GENERADOR DE TEMPLATES")
    print("=" * 60)
    
    # Seleccionar plataforma
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
    
    for platform in platforms:
        print(f"\n{'='*40}")
        print(f"PLATAFORMA: {platform.upper()}")
        print(f"{'='*40}")
        
        generator = CardTemplateGenerator(platform=platform)
        
        # Verificar templates existentes
        report = generator.verify_templates()
        
        print(f"\n📊 ESTADO ACTUAL:")
        print(f"   Templates encontrados: {report['templates_found']}/52")
        print(f"   Porcentaje completado: {report['completion_percentage']:.1f}%")
        
        if report['templates_found'] == 52:
            print("✅ ¡Todos los templates ya existen!")
            continue
        
        print(f"\n📋 Templates faltantes: {len(report['missing_templates_list'])}")
        if len(report['missing_templates_list']) <= 10:
            print(f"   {', '.join(report['missing_templates_list'])}")
        
        # Menú de opciones
        print("\n📝 OPCIONES:")
        print("1. Modo manual (recomendado para mejores resultados)")
        print("2. Crear templates de muestra básicos")
        print("3. Verificar templates existentes")
        print("4. Generar mapa de templates")
        print("5. Saltar esta plataforma")
        
        option = input("\nSelecciona opción (1-5): ").strip()
        
        if option == "1":
            print("\n🔄 Iniciando modo manual...")
            templates_captured = generator.manual_template_capture()
            print(f"✅ Capturados {templates_captured} templates nuevos")
            
        elif option == "2":
            print("\n🔄 Creando templates de muestra...")
            generator.create_sample_templates()
            
        elif option == "3":
            print("\n📋 Reporte de templates:")
            print(json.dumps(report, indent=2))
            
        elif option == "4":
            print("\n🗺️  Generando mapa de templates...")
            template_map = generator.generate_template_map()
            print(f"✅ Mapa generado con {len(template_map)} templates")
            
        else:
            print(f"⏭️  Saltando {platform}...")
            continue
        
        # Verificar progreso final
        final_report = generator.verify_templates()
        print(f"\n📈 PROGRESO FINAL para {platform}:")
        print(f"   {final_report['templates_found']}/52 templates")
        print(f"   {final_report['completion_percentage']:.1f}% completo")
    
    print("\n" + "=" * 60)
    print("✅ GENERACIÓN DE TEMPLATES COMPLETADA")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()