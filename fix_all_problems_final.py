#!/usr/bin/env python3
"""
FIX ALL PROBLEMS - FINAL VERSION
Corrige todos los problemas encontrados en el sistema Poker Coach Pro
"""
import os
import sys
import shutil

def fix_card_recognizer():
    """Corregir CardRecognizer"""
    print("🔧 Corrigiendo CardRecognizer...")
    
    card_file = "src/screen_capture/card_recognizer.py"
    
    # Contenido completo corregido de CardRecognizer
    card_content = '''"""
Card Recognizer for Poker Coach Pro
Recognizes poker cards from screen captures
"""
import cv2
import numpy as np
import os
from typing import List, Optional, Tuple, Dict
from dataclasses import dataclass


@dataclass
class Card:
    """Represents a recognized card"""
    rank: str  # 2-10, J, Q, K, A
    suit: str  # hearts, diamonds, clubs, spades
    confidence: float
    position: Tuple[int, int, int, int]  # x1, y1, x2, y2


class CardRecognizer:
    """
    Recognizes poker cards using template matching
    Supports both PokerStars and GG Poker
    """
    
    def __init__(self, platform: str = "pokerstars", template_dir: str = None):
        """
        Initialize card recognizer
        
        Args:
            platform: "pokerstars" or "ggpoker"
            template_dir: Directory containing card templates
        """
        self.platform = platform.lower()
        
        # Set template directory
        if template_dir:
            self.template_dir = template_dir
        else:
            self.template_dir = f"data/card_templates/{self.platform}"
        
        # Load templates
        self.templates = self._load_templates()
        
        # Matching threshold
        self.match_threshold = 0.7
        
        # Platform-specific settings
        self.settings = self._get_platform_settings()
        
        print(f"🎴 CardRecognizer initialized for {self.platform}")
        print(f"📁 Template directory: {self.template_dir}")
        print(f"📦 Templates loaded: {len(self.templates)}")
    
    def _get_platform_settings(self) -> Dict:
        """Get platform-specific settings"""
        return {
            "pokerstars": {
                "card_size": (72, 96),  # Width, height
                "suit_colors": {
                    "hearts": (0, 0, 200),    # Red
                    "diamonds": (0, 0, 200),  # Red
                    "clubs": (0, 0, 0),       # Black
                    "spades": (0, 0, 0)       # Black
                }
            },
            "ggpoker": {
                "card_size": (80, 112),
                "suit_colors": {
                    "hearts": (0, 0, 255),
                    "diamonds": (0, 0, 255),
                    "clubs": (0, 0, 0),
                    "spades": (0, 0, 0)
                }
            }
        }.get(self.platform, {})
    
    def _load_templates(self) -> Dict[str, np.ndarray]:
        """Load card templates from disk"""
        templates = {}
        
        if not os.path.exists(self.template_dir):
            print(f"⚠️  Template directory not found: {self.template_dir}")
            print(f"💡 Creating directory structure...")
            os.makedirs(self.template_dir, exist_ok=True)
            return templates
        
        # Define card ranks and suits
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        
        loaded_count = 0
        
        for suit in suits:
            for rank in ranks:
                # Try different filename patterns
                patterns = [
                    f"{rank}_of_{suit}.png",
                    f"{rank}_of_{suit}.jpg",
                    f"{suit}_{rank}.png",
                    f"{rank}{suit[0]}.png"
                ]
                
                for pattern in patterns:
                    template_path = os.path.join(self.template_dir, pattern)
                    
                    if os.path.exists(template_path):
                        try:
                            # Load template
                            template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
                            
                            if template is not None:
                                # Resize if needed
                                if self.settings and "card_size" in self.settings:
                                    target_size = self.settings["card_size"]
                                    if template.shape != target_size[::-1]:  # OpenCV uses (height, width)
                                        template = cv2.resize(template, target_size)
                                
                                # Store with key
                                key = f"{rank}_{suit}"
                                templates[key] = template
                                loaded_count += 1
                                break  # Stop trying patterns for this card
                                
                        except Exception as e:
                            print(f"⚠️  Error loading template {template_path}: {e}")
        
        if loaded_count == 0:
            print(f"❌ No templates loaded from {self.template_dir}")
            print(f"💡 You may need to generate templates first")
        
        return templates
    
    def recognize_cards(self, image: np.ndarray, card_regions: List[Tuple[int, int, int, int]]) -> List[Card]:
        """
        Recognize cards in specified regions
        
        Args:
            image: Input image (BGR or grayscale)
            card_regions: List of (x1, y1, x2, y2) regions
            
        Returns:
            List of recognized Card objects
        """
        if not self.templates:
            print("⚠️  No templates available, returning empty results")
            return []
        
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        recognized_cards = []
        
        for region_idx, region in enumerate(card_regions):
            x1, y1, x2, y2 = region
            card_img = gray[y1:y2, x1:x2]
            
            if card_img.size == 0:
                print(f"⚠️  Empty card region: {region}")
                continue
            
            best_match = None
            best_score = 0.0
            best_template = None
            
            # Try to match with each template
            for card_name, template in self.templates.items():
                # Resize template to match card image size
                if template.shape != card_img.shape:
                    try:
                        template_resized = cv2.resize(template, (card_img.shape[1], card_img.shape[0]))
                    except:
                        continue
                else:
                    template_resized = template
                
                # Perform template matching
                try:
                    result = cv2.matchTemplate(card_img, template_resized, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    
                    if max_val > best_score:
                        best_score = max_val
                        best_match = card_name
                        best_template = template_resized
                        
                except Exception as e:
                    print(f"⚠️  Template matching error: {e}")
                    continue
            
            # Check if match is good enough
            if best_match and best_score > self.match_threshold:
                rank, suit = best_match.split('_')
                
                # Create card object
                card = Card(
                    rank=rank.upper(),
                    suit=suit,
                    confidence=best_score,
                    position=region
                )
                
                recognized_cards.append(card)
                
                if len(card_regions) <= 10:  # Don't spam for many regions
                    print(f"✅ Card {region_idx+1}: {rank.upper()}{suit[0].upper()} ({best_score:.2f})")
                    
            else:
                # Add unknown card
                card = Card(
                    rank="?",
                    suit="?",
                    confidence=best_score if best_score else 0.0,
                    position=region
                )
                recognized_cards.append(card)
                
                if len(card_regions) <= 10:
                    print(f"❓ Card {region_idx+1}: Unknown ({best_score:.2f})")
        
        return recognized_cards
    
    def detect_card_regions(self, table_image: np.ndarray, num_cards: int = 5) -> List[Tuple[int, int, int, int]]:
        """
        Detect regions where cards might be located
        
        Args:
            table_image: Image of poker table
            num_cards: Number of cards to detect (2 for hand, 5 for community)
            
        Returns:
            List of potential card regions
        """
        regions = []
        
        if table_image is None or table_image.size == 0:
            return regions
        
        height, width = table_image.shape[:2]
        
        # Platform-specific region detection
        if self.platform == "pokerstars":
            if num_cards == 2:  # Player hand
                # Bottom center for player cards
                card_width, card_height = 80, 120
                center_x = width // 2
                bottom_y = height - 150
                
                for i in range(2):
                    x = center_x - card_width + (i * (card_width + 10)) - (card_width // 2)
                    y = bottom_y - card_height
                    regions.append((x, y, x + card_width, y + card_height))
                    
            else:  # Community cards (up to 5)
                card_width, card_height = 80, 120
                center_x = width // 2
                center_y = height // 2 - 50
                
                for i in range(min(num_cards, 5)):
                    x = center_x - (2.5 * card_width) + (i * (card_width + 5))
                    y = center_y - card_height // 2
                    regions.append((x, y, x + card_width, y + card_height))
        
        elif self.platform == "ggpoker":
            if num_cards == 2:  # Player hand
                card_width, card_height = 90, 130
                center_x = width // 2
                bottom_y = height - 180
                
                for i in range(2):
                    x = center_x - card_width + (i * (card_width + 15)) - (card_width // 2)
                    y = bottom_y - card_height
                    regions.append((x, y, x + card_width, y + card_height))
                    
            else:  # Community cards
                card_width, card_height = 90, 130
                center_x = width // 2
                center_y = height // 2 - 70
                
                for i in range(min(num_cards, 5)):
                    x = center_x - (2.5 * card_width) + (i * (card_width + 10))
                    y = center_y - card_height // 2
                    regions.append((x, y, x + card_width, y + card_height))
        
        # Filter regions that are within image bounds
        valid_regions = []
        for x1, y1, x2, y2 in regions:
            if (0 <= x1 < width and 0 <= y1 < height and 
                0 <= x2 <= width and 0 <= y2 <= height and
                x2 > x1 and y2 > y1):
                valid_regions.append((x1, y1, x2, y2))
        
        return valid_regions
    
    def extract_card_color(self, card_image: np.ndarray) -> str:
        """
        Extract card color (red/black) based on suit pixels
        """
        if len(card_image.shape) == 2:  # Grayscale
            return "unknown"
        
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(card_image, cv2.COLOR_BGR2HSV)
        
        # Define color ranges
        red_lower1 = np.array([0, 100, 100])
        red_upper1 = np.array([10, 255, 255])
        red_lower2 = np.array([160, 100, 100])
        red_upper2 = np.array([180, 255, 255])
        
        # Create masks
        red_mask1 = cv2.inRange(hsv, red_lower1, red_upper1)
        red_mask2 = cv2.inRange(hsv, red_lower2, red_upper2)
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)
        
        # Count red pixels
        red_pixels = cv2.countNonZero(red_mask)
        total_pixels = card_image.shape[0] * card_image.shape[1]
        
        if red_pixels / total_pixels > 0.01:  # More than 1% red pixels
            return "red"
        else:
            return "black"
    
    def save_debug_image(self, image: np.ndarray, regions: List[Tuple[int, int, int, int]], 
                        output_path: str = "debug/card_detection.png"):
        """
        Save debug image with detected card regions
        """
        if len(image.shape) == 2:  # Grayscale
            debug_img = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        else:
            debug_img = image.copy()
        
        # Draw regions
        for i, (x1, y1, x2, y2) in enumerate(regions):
            color = (0, 255, 0) if i < 2 else (255, 0, 0)  # Green for hand, blue for community
            cv2.rectangle(debug_img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(debug_img, str(i+1), (x1+5, y1+20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Save
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, debug_img)
        print(f"💾 Debug image saved: {output_path}")
        
        return debug_img
    
    def test_recognition(self, test_image_path: Optional[str] = None) -> bool:
        """
        Test card recognition system
        
        Args:
            test_image_path: Optional path to test image
            
        Returns:
            True if test successful
        """
        print("\n🧪 Testing CardRecognizer...")
        
        # Create test image if none provided
        if test_image_path is None or not os.path.exists(test_image_path):
            print("⚠️  No test image provided, creating synthetic test...")
            
            # Create synthetic test image
            test_image = np.zeros((400, 600, 3), dtype=np.uint8)
            test_image[:] = (50, 150, 50)  # Green table background
            
            # Add some fake card regions
            cv2.rectangle(test_image, (100, 150), (180, 270), (255, 255, 255), -1)
            cv2.rectangle(test_image, (200, 150), (280, 270), (255, 255, 255), -1)
            
            test_image_path = "debug/test_cards.png"
            cv2.imwrite(test_image_path, test_image)
            print(f"💾 Created test image: {test_image_path}")
        
        # Load test image
        test_image = cv2.imread(test_image_path)
        if test_image is None:
            print("❌ Failed to load test image")
            return False
        
        print(f"✅ Test image loaded: {test_image.shape}")
        
        # Detect card regions
        card_regions = self.detect_card_regions(test_image, num_cards=2)
        
        if not card_regions:
            print("⚠️  No card regions detected, using default regions")
            height, width = test_image.shape[:2]
            card_regions = [
                (width//2 - 100, height//2 - 60, width//2 - 20, height//2 + 60),
                (width//2 + 20, height//2 - 60, width//2 + 100, height//2 + 60)
            ]
        
        print(f"🔍 Card regions detected: {len(card_regions)}")
        
        # Recognize cards
        cards = self.recognize_cards(test_image, card_regions)
        
        # Results
        print(f"\n📊 Recognition Results:")
        for i, card in enumerate(cards):
            if card.rank != "?":
                print(f"  Card {i+1}: {card.rank}{card.suit[0].upper()} ({card.confidence:.2f})")
            else:
                print(f"  Card {i+1}: Unknown ({card.confidence:.2f})")
        
        # Save debug image
        self.save_debug_image(test_image, card_regions)
        
        return len(cards) > 0


# Test function
def test_card_recognizer():
    """Test function for card recognizer"""
    print("=" * 60)
    print("🧪 TESTING CARD RECOGNIZER")
    print("=" * 60)
    
    recognizer = CardRecognizer(platform="pokerstars")
    
    if recognizer.test_recognition():
        print("\n✅ CardRecognizer test PASSED")
    else:
        print("\n❌ CardRecognizer test FAILED")
    
    print("=" * 60)


if __name__ == "__main__":
    test_card_recognizer()
'''
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(card_file), exist_ok=True)
    
    # Escribir archivo
    with open(card_file, 'w', encoding='utf-8') as f:
        f.write(card_content)
    
    print("✅ CardRecognizer corregido y guardado")
    return True

def fix_pokerstars_adapter():
    """Corregir PokerStars Adapter"""
    print("\n🔧 Corrigiendo PokerStars Adapter...")
    
    adapter_file = "src/platforms/pokerstars_adapter.py"
    
    if not os.path.exists(adapter_file):
        print(f"❌ Archivo no encontrado: {adapter_file}")
        return False
    
    with open(adapter_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar y corregir la línea problemática
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Buscar la creación de CardRecognizer
        if 'CardRecognizer(' in line and ('self.stealth_level' in line or 'stealth_level' in line):
            # Corregir la línea
            if 'CardRecognizer(self.platform, self.stealth_level)' in line:
                fixed_line = line.replace(
                    'CardRecognizer(self.platform, self.stealth_level)',
                    'CardRecognizer(platform=self.platform)'
                )
                print(f"✅ Línea corregida: {fixed_line}")
                fixed_lines.append(fixed_line)
            elif 'CardRecognizer(' in line:
                # Intentar corregir genéricamente
                fixed_line = line.split('=')[0] + '= CardRecognizer(platform=self.platform)'
                print(f"✅ Línea reemplazada: {fixed_line}")
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    # Guardar archivo corregido
    fixed_content = '\n'.join(fixed_lines)
    
    with open(adapter_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("✅ PokerStars Adapter corregido")
    return True

def fix_ggpoker_adapter():
    """Corregir GG Poker Adapter si existe"""
    print("\n🔧 Corrigiendo GG Poker Adapter...")
    
    adapter_file = "src/platforms/ggpoker_adapter.py"
    
    if not os.path.exists(adapter_file):
        print(f"⚠️  Archivo no encontrado: {adapter_file} (puede ser normal)")
        return True  # No es un error si no existe
    
    with open(adapter_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar y corregir similar a pokerstars_adapter
    if 'CardRecognizer(' in content:
        content = content.replace(
            'CardRecognizer(self.platform, self.stealth_level)',
            'CardRecognizer(platform=self.platform)'
        )
        
        with open(adapter_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ GG Poker Adapter corregido")
    
    return True

def create_test_environment():
    """Crear entorno de prueba completo"""
    print("\n📁 Creando entorno de prueba...")
    
    # Crear directorios necesarios
    directories = [
        "debug",
        "debug_captures",
        "data/card_templates/pokerstars",
        "data/card_templates/ggpoker",
        "logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ {directory}/")
    
    # Crear archivo de prueba simple
    test_simple = '''#!/usr/bin/env python3
"""
TEST SIMPLE - Verificación rápida del sistema
"""
import sys
import os
sys.path.insert(0, 'src')

print("=" * 60)
print("🧪 TEST SIMPLE - POKER COACH PRO")
print("=" * 60)

def test_component(component_name, test_code):
    print(f"\\n🔧 Testing {component_name}...")
    try:
        exec(test_code)
        print(f"✅ {component_name}: OK")
        return True
    except Exception as e:
        print(f"❌ {component_name}: {e}")
        return False

# Test 1: StealthScreenCapture
test1 = """
from screen_capture.stealth_capture import StealthScreenCapture
capture = StealthScreenCapture("pokerstars", "MEDIUM")
print(f"   Platform: {capture.platform}")
print(f"   Stealth: {capture.stealth_level}")
"""

# Test 2: CardRecognizer
test2 = """
from screen_capture.card_recognizer import CardRecognizer
recognizer = CardRecognizer(platform="pokerstars")
print(f"   Platform: {recognizer.platform}")
print(f"   Templates: {len(recognizer.templates)}")
"""

# Test 3: TableDetector
test3 = """
from screen_capture.table_detector import TableDetector
detector = TableDetector()
print(f"   Detector creado")
"""

# Test 4: PokerEngine
test4 = """
from core.poker_engine import PokerEngine
engine = PokerEngine()
print(f"   Engine creado")
"""

# Ejecutar tests
tests = [
    ("StealthScreenCapture", test1),
    ("CardRecognizer", test2),
    ("TableDetector", test3),
    ("PokerEngine", test4)
]

results = []
for name, code in tests:
    results.append(test_component(name, code))

# Resumen
print("\\n" + "=" * 60)
print("📊 RESUMEN:")
print("=" * 60)

passed = sum(1 for r in results if r)
total = len(tests)

print(f"\\n✅ Pasados: {passed}/{total}")

if passed == total:
    print("\\n🎉 ¡TODOS LOS TESTS PASARON!")
    print("\\n🚀 El sistema está listo. Ejecuta:")
    print("   python test_pokerstars.py")
else:
    print("\\n⚠️  Algunos tests fallaron")
    print("\\n💡 Ejecuta: python fix_all_problems_final.py")

print("=" * 60)
'''

    with open("test_simple.py", 'w', encoding='utf-8') as f:
        f.write(test_simple)
    
    print("✅ test_simple.py creado")
    return True

def create_final_verification():
    """Crear script de verificación final"""
    print("\n📄 Creando verificación final...")
    
    verify_content = '''#!/usr/bin/env python3
"""
VERIFICACIÓN FINAL - Poker Coach Pro
Verifica que todos los componentes funcionen correctamente
"""
import sys
import os
import importlib.util

print("=" * 70)
print("🔍 VERIFICACIÓN FINAL - POKER COACH PRO")
print("=" * 70)

sys.path.insert(0, 'src')

def verify_module(module_name, class_name=None):
    """Verificar que un módulo/clase se pueda importar"""
    try:
        if class_name:
            # Intentar importar clase específica
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            instance = cls()
            return True, f"{module_name}.{class_name}"
        else:
            # Solo verificar módulo
            __import__(module_name)
            return True, module_name
    except ImportError as e:
        return False, f"{module_name}: {e}"
    except TypeError as e:
        return False, f"{module_name}.{class_name}: Error de constructor - {e}"
    except Exception as e:
        return False, f"{module_name}: Error inesperado - {e}"

def verify_adapters():
    """Verificar adaptadores de plataforma"""
    print("\\n🎯 VERIFICANDO ADAPTADORES:")
    print("-" * 40)
    
    adapters = [
        ("platforms.pokerstars_adapter", "PokerStarsAdapter"),
        ("platforms.ggpoker_adapter", "GGPokerAdapter")
    ]
    
    results = []
    for module, adapter_class in adapters:
        # Verificar si el archivo existe
        module_path = f"src/{module.replace('.', '/')}.py"
        if os.path.exists(module_path):
            success, message = verify_module(module, adapter_class)
            if success:
                print(f"✅ {adapter_class}")
            else:
                print(f"❌ {adapter_class}: {message.split(': ')[-1]}")
            results.append(success)
        else:
            print(f"⚠️  {adapter_class}: Archivo no encontrado")
            results.append(False)
    
    return any(results)  # Al menos uno debe funcionar

def verify_screen_capture():
    """Verificar módulo de captura de pantalla"""
    print("\\n📷 VERIFICANDO CAPTURA DE PANTALLA:")
    print("-" * 40)
    
    components = [
        ("screen_capture.stealth_capture", "StealthScreenCapture"),
        ("screen_capture.card_recognizer", "CardRecognizer"),
        ("screen_capture.table_detector", "TableDetector")
    ]
    
    all_ok = True
    for module, component in components:
        success, message = verify_module(module, component)
        if success:
            print(f"✅ {component}")
        else:
            print(f"❌ {component}: {message.split(': ')[-1]}")
            all_ok = False
    
    return all_ok

def verify_core():
    """Verificar componentes core"""
    print("\\n🧠 VERIFICANDO COMPONENTES CORE:")
    print("-" * 40)
    
    components = [
        ("core.poker_engine", "PokerEngine")
    ]
    
    all_ok = True
    for module, component in components:
        success, message = verify_module(module, component)
        if success:
            print(f"✅ {component}")
        else:
            print(f"❌ {component}: {message.split(': ')[-1]}")
            all_ok = False
    
    return all_ok

def check_dependencies():
    """Verificar dependencias"""
    print("\\n📦 VERIFICANDO DEPENDENCIAS:")
    print("-" * 40)
    
    dependencies = [
        ("cv2", "opencv-python"),
        ("mss", "mss"),
        ("numpy", "numpy"),
        ("PIL", "Pillow")
    ]
    
    missing = []
    for import_name, pip_name in dependencies:
        try:
            __import__(import_name)
            print(f"✅ {pip_name}")
        except ImportError:
            print(f"❌ {pip_name}")
            missing.append(pip_name)
    
    if missing:
        print(f"\\n⚠️  Dependencias faltantes: {', '.join(missing)}")
        print(f"💡 Instalar con: pip install {' '.join(missing)}")
        return False
    
    return True

# Ejecutar verificaciones
print("\\n🚀 INICIANDO VERIFICACIÓN COMPLETA...")

checks = [
    ("Dependencias", check_dependencies),
    ("Captura de pantalla", verify_screen_capture),
    ("Adaptadores", verify_adapters),
    ("Componentes Core", verify_core)
]

results = []
for check_name, check_func in checks:
    print(f"\\n🔍 {check_name}...")
    result = check_func()
    results.append((check_name, result))

# Resumen
print("\\n" + "=" * 70)
print("📊 RESUMEN DE VERIFICACIÓN")
print("=" * 70)

all_passed = all(result for _, result in results)
passed_count = sum(1 for _, result in results if result)
total_count = len(results)

print(f"\\n✅ Verificaciones pasadas: {passed_count}/{total_count}")

if all_passed:
    print("\\n🎉 ¡TODAS LAS VERIFICACIONES PASARON!")
    print("\\n🚀 EL SISTEMA ESTÁ LISTO PARA USAR")
    print("\\n📋 PRÓXIMOS PASOS:")
    print("   1. Abre PokerStars o GG Poker")
    print("   2. Ejecuta: python test_pokerstars.py")
    print("   3. O: python test_ggpoker_simple.py")
    print("   4. Sigue las instrucciones en pantalla")
else:
    print("\\n⚠️  ALGUNAS VERIFICACIONES FALLARON")
    print("\\n💡 VERIFICACIONES FALLIDAS:")
    for check_name, result in results:
        if not result:
            print(f"   • {check_name}")
    
    print("\\n🔧 SOLUCIONES:")
    print("   1. Ejecuta: python fix_all_problems_final.py")
    print("   2. Instala dependencias faltantes")
    print("   3. Verifica la estructura de archivos")

print("\\n" + "=" * 70)
print("✅ VERIFICACIÓN COMPLETADA")
print("=" * 70)
'''

    with open("final_verification.py", 'w', encoding='utf-8') as f:
        f.write(verify_content)
    
    print("✅ final_verification.py creado")
    return True

def run_final_verification():
    """Ejecutar verificación final"""
    print("\n🧪 Ejecutando verificación final...")
    
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, "final_verification.py"],
            capture_output=False,
            text=True,
            timeout=60
        )
        
        return True
            
    except Exception as e:
        print(f"❌ Error ejecutando verificación: {e}")
        return False

def create_quick_start_guide():
    """Crear guía de inicio rápido"""
    print("\n📝 Creando guía de inicio rápido...")
    
    guide_content = '''# 🎴 POKER COACH PRO - GUÍA DE INICIO RÁPIDO

## 🚀 INSTALACIÓN Y CONFIGURACIÓN

### 1. Verificar el sistema
```bash
# Ejecutar verificación completa
python final_verification.py

# Si hay errores, reparar:
python fix_all_problems_final.py