#!/usr/bin/env python3
"""
🎴 CARD_OCR_SYSTEM.py - Sistema Avanzado de Reconocimiento de Cartas
Detección en tiempo real de cartas en mesas de PokerStars
"""

import cv2
import numpy as np
import pytesseract
import time
import os
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Optional
import json
from datetime import datetime

# Configurar Tesseract si está en PATH común
tesseract_paths = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    "/usr/bin/tesseract"
]

for path in tesseract_paths:
    if os.path.exists(path):
        pytesseract.pytesseract.tesseract_cmd = path
        break

@dataclass
class Card:
    """Representa una carta de poker"""
    rank: str  # A, K, Q, J, 10, 9, 8, 7, 6, 5, 4, 3, 2
    suit: str  #  (spades),  (hearts),  (diamonds),  (clubs)
    position: Tuple[int, int]  # (x, y) en pantalla
    confidence: float  # Confianza de detección (0-1)
    
    def __str__(self):
        return f"{self.rank}{self.suit}"
    
    def to_dict(self):
        return {
            "rank": self.rank,
            "suit": self.suit,
            "position": self.position,
            "confidence": self.confidence
        }

@dataclass
class TableSituation:
    """Situación actual en la mesa"""
    hero_cards: List[Card]  # Cartas del jugador
    community_cards: List[Card]  # Cartas comunitarias
    pot_size: float  # Tamaño del bote
    position: str  # early, middle, late, button
    players_active: int  # Jugadores activos en la mano
    street: str  # preflop, flop, turn, river
    action_to_hero: str  # check, bet, raise, allin
    bet_size: float  # Tamaño de la apuesta actual
    
    def __str__(self):
        return (f"Situación: {self.street.upper()}\n"
                f"Hero: {[str(c) for c in self.hero_cards]}\n"
                f"Comunitarias: {[str(c) for c in self.community_cards]}\n"
                f"Bote: \n"
                f"Posición: {self.position}\n"
                f"Jugadores: {self.players_active}\n"
                f"Acción: {self.action_to_hero} ()")

class PokerStarsCardDetector:
    """Detector de cartas específico para PokerStars"""
    
    # Rangos y palos en PokerStars
    RANKS = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
    SUITS = ['', '', '', '']
    
    # Colores para diferentes temas de PokerStars
    THEME_COLORS = {
        'classic': {
            'card_bg': (240, 240, 220),  # Fondo carta claro
            'text_color': (30, 30, 30),   # Texto oscuro
            'heart_color': (220, 50, 50), # Rojo corazones
            'diamond_color': (220, 50, 50), # Rojo diamantes
            'spade_color': (30, 30, 30),   # Negro picas
            'club_color': (30, 30, 30)     # Negro tréboles
        },
        'dark': {
            'card_bg': (50, 50, 70),
            'text_color': (220, 220, 220),
            'heart_color': (255, 100, 100),
            'diamond_color': (255, 100, 100),
            'spade_color': (200, 200, 200),
            'club_color': (200, 200, 200)
        }
    }
    
    def __init__(self, theme='classic'):
        self.theme = theme
        self.colors = self.THEME_COLORS.get(theme, self.THEME_COLORS['classic'])
        
        # Templates para detección rápida (simulados)
        self.card_templates = self._create_card_templates()
        self.last_detection_time = time.time()
        self.detection_cache = {}
        
        print(f" Inicializado detector PokerStars - Tema: {theme}")
    
    def _create_card_templates(self):
        """Crear templates de cartas para detección rápida"""
        templates = {}
        
        # Simular templates básicos para cada carta
        for rank in self.RANKS:
            for suit in self.SUITS:
                card_key = f"{rank}{suit}"
                # En un sistema real, aquí cargaríamos imágenes de referencia
                templates[card_key] = {
                    'rank': rank,
                    'suit': suit,
                    'color': self._get_suit_color(suit)
                }
        
        return templates
    
    def _get_suit_color(self, suit):
        """Obtener color RGB para un palo"""
        if suit in ['♥', '♦']:
            return self.colors['heart_color']
        else:
            return self.colors['spade_color']
    
    def detect_cards_in_screenshot(self, screenshot):
        """
        Detectar cartas en una captura de pantalla
        screenshot: imagen numpy array (BGR)
        """
        try:
            height, width = screenshot.shape[:2]
            
            # Convertir a diferentes espacios de color
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            
            # Detectar áreas de cartas basado en el tema
            card_regions = self._find_card_regions(screenshot, gray)
            
            detected_cards = []
            
            for region in card_regions:
                x, y, w, h = region
                
                # Recortar región de carta
                card_region = screenshot[y:y+h, x:x+w]
                
                # Detectar carta en esta región
                card = self._detect_card_in_region(card_region)
                
                if card:
                    card.position = (x + w//2, y + h//2)
                    detected_cards.append(card)
            
            return detected_cards
            
        except Exception as e:
            print(f" Error en detección: {e}")
            return []
    
    def _find_card_regions(self, image, gray_image):
        """Encontrar regiones que probablemente sean cartas"""
        regions = []
        height, width = image.shape[:2]
        
        # Umbral adaptativo para encontrar bordes claros/oscuros
        _, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filtrar por tamaño (cartas típicas en PokerStars)
            if 1000 < area < 5000:  # Área aproximada de una carta
                x, y, w, h = cv2.boundingRect(contour)
                
                # Verificar relación de aspecto (cartas ~1.4:1)
                aspect_ratio = w / h
                if 1.2 < aspect_ratio < 1.6:
                    regions.append((x, y, w, h))
        
        return regions
    
    def _detect_card_in_region(self, card_region):
        """Detectar carta específica en una región"""
        try:
            # Convertir a escala de grises para OCR
            gray_card = cv2.cvtColor(card_region, cv2.COLOR_BGR2GRAY)
            
            # Aplicar threshold para mejorar contraste
            _, binary = cv2.threshold(gray_card, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Invertir si es necesario (texto oscuro sobre fondo claro)
            if np.mean(binary) > 127:
                binary = cv2.bitwise_not(binary)
            
            # Usar OCR para leer texto
            custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=AKQJ1098765432'
            text = pytesseract.image_to_string(binary, config=custom_config).strip()
            
            if text:
                # Limpiar y analizar texto detectado
                rank = self._parse_rank(text)
                suit = self._detect_suit(card_region)
                
                if rank and suit:
                    confidence = 0.8  # Confianza base
                    return Card(rank=rank, suit=suit, position=(0, 0), confidence=confidence)
            
            # Si OCR falla, intentar detección por color/formas
            return self._detect_by_color_and_shape(card_region)
            
        except Exception as e:
            print(f" Error detectando carta: {e}")
            return None
    
    def _parse_rank(self, text):
        """Analizar texto para extraer rango"""
        text = text.upper().strip()
        
        # Buscar rangos en el texto
        for rank in self.RANKS:
            if rank in text:
                return rank
        
        # Manejar casos especiales
        if '10' in text or 'TEN' in text:
            return '10'
        elif 'A' in text or 'ACE' in text:
            return 'A'
        elif 'K' in text or 'KING' in text:
            return 'K'
        elif 'Q' in text or 'QUEEN' in text:
            return 'Q'
        elif 'J' in text or 'JACK' in text:
            return 'J'
        
        return None
    
    def _detect_suit(self, card_region):
        """Detectar palo basado en color y forma"""
        hsv = cv2.cvtColor(card_region, cv2.COLOR_BGR2HSV)
        
        # Definir rangos de color para rojo (corazones y diamantes)
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])
        
        # Máscaras para rojo
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        
        # Contar píxeles rojos
        red_pixels = cv2.countNonZero(mask_red)
        total_pixels = card_region.shape[0] * card_region.shape[1]
        red_ratio = red_pixels / total_pixels
        
        # Si hay suficiente rojo, es corazón o diamante
        if red_ratio > 0.05:  # 5% de píxeles rojos
            # Intentar distinguir entre corazón y diamante por forma
            # (simplificado - en sistema real usaríamos templates)
            return ''  # Por defecto corazón
        
        # Si no es rojo, es pica o trébol (negro)
        return ''  # Por defecto pica
    
    def _detect_by_color_and_shape(self, card_region):
        """Detección alternativa por color y formas"""
        # Este es un método simplificado
        # En un sistema real, usaríamos machine learning
        return None
    
    def analyze_table_situation(self, screenshot, hero_position='middle'):
        """Analizar situación completa de la mesa"""
        # Detectar cartas
        detected_cards = self.detect_cards_in_screenshot(screenshot)
        
        if not detected_cards:
            print(" No se detectaron cartas")
            return None
        
        # Separar cartas del hero y comunitarias (simplificado)
        # En sistema real, usaríamos posición en pantalla
        height = screenshot.shape[0]
        
        hero_cards = []
        community_cards = []
        
        for card in detected_cards:
            # Cartas abajo (hero) vs cartas en medio (comunitarias)
            if card.position[1] > height * 0.7:  # Parte inferior
                hero_cards.append(card)
            else:  # Parte central/superior
                community_cards.append(card)
        
        # Determinar calle (preflop, flop, turn, river)
        street = self._determine_street(len(community_cards))
        
        # Crear situación
        situation = TableSituation(
            hero_cards=hero_cards[:2],  # Máximo 2 cartas para hero
            community_cards=community_cards[:5],  # Máximo 5 comunitarias
            pot_size=100.0,  # Valor simulado
            position=hero_position,
            players_active=6,  # Valor simulado
            street=street,
            action_to_hero="bet",  # Valor simulado
            bet_size=20.0  # Valor simulado
        )
        
        return situation
    
    def _determine_street(self, community_card_count):
        """Determinar calle basado en número de cartas comunitarias"""
        if community_card_count == 0:
            return "preflop"
        elif community_card_count == 3:
            return "flop"
        elif community_card_count == 4:
            return "turn"
        elif community_card_count == 5:
            return "river"
        else:
            return "unknown"

class GTOAnalyzer:
    """Analizador GTO para situaciones de poker"""
    
    def __init__(self):
        # Base de conocimiento GTO simplificada
        self.gto_rules = self._load_gto_rules()
        self.hand_strengths = self._load_hand_strengths()
        
    def _load_gto_rules(self):
        """Cargar reglas GTO básicas"""
        return {
            "preflop": {
                "early": {
                    "AA": "RAISE", "KK": "RAISE", "QQ": "RAISE", "JJ": "RAISE",
                    "AK": "RAISE", "AQ": "RAISE", "AJ": "RAISE", "KQ": "RAISE"
                },
                "middle": {
                    "AA": "RAISE", "KK": "RAISE", "QQ": "RAISE", "JJ": "RAISE",
                    "TT": "RAISE", "99": "RAISE", "AK": "RAISE", "AQ": "RAISE",
                    "AJ": "RAISE", "KQ": "RAISE", "KJ": "CALL", "QJ": "CALL"
                },
                "late": {
                    "AA": "RAISE", "KK": "RAISE", "QQ": "RAISE", "JJ": "RAISE",
                    "TT": "RAISE", "99": "RAISE", "88": "RAISE", "77": "RAISE",
                    "AK": "RAISE", "AQ": "RAISE", "AJ": "RAISE", "AT": "RAISE",
                    "KQ": "RAISE", "KJ": "RAISE", "KT": "RAISE", "QJ": "RAISE",
                    "QT": "CALL", "JT": "CALL", "T9": "CALL"
                }
            },
            "postflop": {
                "top_pair": "BET/RAISE",
                "overpair": "BET/RAISE",
                "middle_pair": "CHECK/CALL",
                "bottom_pair": "CHECK/FOLD",
                "flush_draw": "BET/CALL",
                "straight_draw": "BET/CALL",
                "nothing": "CHECK/FOLD"
            }
        }
    
    def _load_hand_strengths(self):
        """Cargar fuerza de manos preflop"""
        return {
            "AA": 1, "KK": 2, "QQ": 3, "JJ": 4, "TT": 5,
            "99": 6, "88": 7, "77": 8, "66": 9, "55": 10,
            "44": 11, "33": 12, "22": 13,
            "AK": 14, "AQ": 15, "AJ": 16, "AT": 17,
            "KQ": 18, "KJ": 19, "KT": 20,
            "QJ": 21, "QT": 22, "JT": 23
        }
    
    def analyze_situation(self, situation):
        """Analizar situación y recomendar acción GTO"""
        if not situation or not situation.hero_cards:
            return {"action": "FOLD", "confidence": 0.0, "reason": "No cards detected"}
        
        # Obtener mano del hero
        hero_hand = self._get_hero_hand_string(situation.hero_cards)
        
        # Análisis basado en calle
        if situation.street == "preflop":
            return self._analyze_preflop(hero_hand, situation)
        else:
            return self._analyze_postflop(hero_hand, situation)
    
    def _get_hero_hand_string(self, hero_cards):
        """Convertir cartas del hero a string (ej: 'AKs' o 'AKo')"""
        if len(hero_cards) < 2:
            return "??"
        
        card1 = hero_cards[0]
        card2 = hero_cards[1]
        
        # Ordenar por fuerza
        ranks = [card1.rank, card2.rank]
        strengths = [self.hand_strengths.get(r + r, 100) for r in ranks]
        sorted_cards = sorted(zip(ranks, strengths), key=lambda x: x[1])
        
        hand = sorted_cards[0][0] + sorted_cards[1][0]
        
        # Añadir suited/offsuit
        if card1.suit == card2.suit:
            hand += "s"  # suited
        else:
            hand += "o"  # offsuit
        
        return hand
    
    def _analyze_preflop(self, hero_hand, situation):
        """Analizar situación preflop"""
        position = situation.position
        hand_rank = hero_hand[:2]  # Primeros 2 caracteres (ej: 'AK')
        
        # Buscar en reglas GTO
        if position in self.gto_rules["preflop"]:
            if hand_rank in self.gto_rules["preflop"][position]:
                action = self.gto_rules["preflop"][position][hand_rank]
                confidence = 0.85
                reason = f"GTO Standard: {hand_rank} from {position} position"
            else:
                # Mano no en rango GTO estándar
                action = "FOLD"
                confidence = 0.7
                reason = f"{hand_rank} not in standard {position} range"
        else:
            action = "CALL" if situation.bet_size == 0 else "FOLD"
            confidence = 0.5
            reason = "Default action for unknown position"
        
        return {
            "action": action,
            "confidence": confidence,
            "reason": reason,
            "hand": hero_hand,
            "position": position,
            "street": situation.street
        }
    
    def _analyze_postflop(self, hero_hand, situation):
        """Analizar situación postflop (simplificado)"""
        # En sistema real, aquí iría análisis de equity, board texture, etc.
        
        # Evaluar fuerza de mano aproximada
        hand_strength = self._evaluate_hand_strength(situation)
        
        if hand_strength > 0.7:
            action = "RAISE"
            confidence = 0.8
            reason = "Strong hand on current board"
        elif hand_strength > 0.4:
            action = "CALL"
            confidence = 0.6
            reason = "Medium strength, pot odds favorable"
        else:
            action = "FOLD"
            confidence = 0.7
            reason = "Weak hand relative to board"
        
        return {
            "action": action,
            "confidence": confidence,
            "reason": reason,
            "hand_strength": hand_strength,
            "hand": hero_hand,
            "street": situation.street
        }
    
    def _evaluate_hand_strength(self, situation):
        """Evaluar fuerza de mano postflop (simplificado)"""
        # Sistema simplificado - en realidad usaríamos equity calculators
        return 0.5  # Valor medio por defecto

class PokerTableOverlay:
    """Overlay para mostrar información en tiempo real"""
    
    def __init__(self, detector, analyzer):
        self.detector = detector
        self.analyzer = analyzer
        self.last_update = time.time()
        
    def update_overlay(self, screenshot):
        """Actualizar overlay con nueva información"""
        current_time = time.time()
        
        # Actualizar cada 0.5 segundos máximo
        if current_time - self.last_update < 0.5:
            return None
        
        self.last_update = current_time
        
        # Analizar situación
        situation = self.detector.analyze_table_situation(screenshot)
        
        if not situation:
            return None
        
        # Obtener recomendación GTO
        analysis = self.analyzer.analyze_situation(situation)
        
        # Crear información para overlay
        overlay_info = {
            "timestamp": datetime.now().isoformat(),
            "situation": str(situation),
            "analysis": analysis,
            "detected_cards": [
                card.to_dict() for card in (situation.hero_cards + situation.community_cards)
            ]
        }
        
        return overlay_info
    
    def display_overlay(self, overlay_info):
        """Mostrar información en formato legible"""
        if not overlay_info:
            print(" Esperando detección...")
            return
        
        print("\n" + "="*60)
        print(" POKER COACH PRO - ANÁLISIS EN TIEMPO REAL")
        print("="*60)
        
        # Mostrar situación
        print(f"\n SITUACIÓN DETECTADA:")
        print(f"  {overlay_info['situation']}")
        
        # Mostrar cartas detectadas
        print(f"\n CARTAS DETECTADAS:")
        for card in overlay_info['detected_cards']:
            print(f"   {card['rank']}{card['suit']} (conf: {card['confidence']:.2f})")
        
        # Mostrar análisis GTO
        analysis = overlay_info['analysis']
        print(f"\n RECOMENDACIÓN GTO:")
        print(f"  Acción: {analysis['action']}")
        print(f"  Confianza: {analysis['confidence']:.1%}")
        print(f"  Razón: {analysis['reason']}")
        
        if 'hand' in analysis:
            print(f"  Mano: {analysis['hand']}")
        
        print("="*60)

def main():
    """Función principal para probar el sistema"""
    print(" INICIANDO SISTEMA DE DETECCIÓN DE CARTAS")
    print("="*50)
    
    # Inicializar componentes
    detector = PokerStarsCardDetector(theme='classic')
    analyzer = GTOAnalyzer()
    overlay = PokerTableOverlay(detector, analyzer)
    
    print("\n OPCIONES:")
    print("1. Usar captura de pantalla real (requiere PokerStars abierto)")
    print("2. Usar imagen de prueba simulada")
    print("3. Demo con situaciones predefinidas")
    
    choice = input("\nSeleccione opción (1-3): ").strip()
    
    if choice == "1":
        # Modo captura real
        run_real_time_mode(detector, analyzer, overlay)
    elif choice == "2":
        # Modo imagen de prueba
        run_test_image_mode(detector, analyzer)
    elif choice == "3":
        # Modo demo
        run_demo_mode(analyzer)
    else:
        print(" Opción no válida")

def run_real_time_mode(detector, analyzer, overlay):
    """Ejecutar en modo tiempo real"""
    print("\n MODO TIEMPO REAL ACTIVADO")
    print("  Asegúrese de tener PokerStars abierto en una mesa")
    print(" Presione Ctrl+C para salir")
    print("-"*50)
    
    import pyautogui
    import mss
    
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Monitor principal
            
            while True:
                # Capturar pantalla
                screenshot = np.array(sct.grab(monitor))
                
                # Actualizar overlay
                overlay_info = overlay.update_overlay(screenshot)
                overlay.display_overlay(overlay_info)
                
                # Esperar antes de siguiente captura
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\n Modo tiempo real finalizado")
    except Exception as e:
        print(f" Error en modo tiempo real: {e}")

def run_test_image_mode(detector, analyzer):
    """Probar con imagen de prueba"""
    print("\n  MODO IMAGEN DE PRUEBA")
    
    # Crear imagen de prueba simulada
    test_image = create_test_image()
    
    # Guardar para referencia
    cv2.imwrite("test_table.png", test_image)
    print(" Imagen de prueba creada: test_table.png")
    
    # Detectar cartas
    print("\n Detectando cartas...")
    cards = detector.detect_cards_in_screenshot(test_image)
    
    if cards:
        print(f" Detección exitosa: {len(cards)} cartas encontradas")
        for card in cards:
            print(f"   {card}")
    else:
        print(" No se detectaron cartas")
    
    # Analizar situación
    print("\n Analizando situación...")
    situation = detector.analyze_table_situation(test_image)
    
    if situation:
        print(f" Situación analizada:")
        print(situation)
        
        # Obtener recomendación GTO
        analysis = analyzer.analyze_situation(situation)
        print(f"\n Recomendación GTO:")
        print(f"  Acción: {analysis['action']}")
        print(f"  Confianza: {analysis['confidence']:.1%}")
        print(f"  Razón: {analysis['reason']}")
    else:
        print(" No se pudo analizar la situación")

def create_test_image():
    """Crear imagen de prueba simulada con cartas"""
    # Crear fondo de mesa verde
    height, width = 800, 1200
    table_color = (40, 90, 40)  # Verde poker
    image = np.full((height, width, 3), table_color, dtype=np.uint8)
    
    # Dibujar áreas de cartas
    card_color = (240, 240, 220)  # Color carta
    card_size = (80, 120)  # Ancho, alto
    
    # Cartas del hero (abajo)
    hero_y = height - 150
    hero_x1 = width // 2 - 100
    hero_x2 = width // 2 + 20
    
    cv2.rectangle(image, (hero_x1, hero_y), (hero_x1 + card_size[0], hero_y + card_size[1]), card_color, -1)
    cv2.rectangle(image, (hero_x2, hero_y), (hero_x2 + card_size[0], hero_y + card_size[1]), card_color, -1)
    
    # Escribir "A" y "K" en las cartas (simulación)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, "A", (hero_x1 + 10, hero_y + 30), font, 1, (0, 0, 0), 2)
    cv2.putText(image, "K", (hero_x2 + 10, hero_y + 30), font, 1, (0, 0, 0), 2)
    
    # Cartas comunitarias (centro)
    community_y = height // 2 - 60
    community_x_start = width // 2 - 200
    
    for i in range(5):
        x = community_x_start + i * 90
        cv2.rectangle(image, (x, community_y), (x + card_size[0], community_y + card_size[1]), card_color, -1)
        
        # Escribir cartas comunitarias simuladas
        community_cards = ["Q", "7", "2", "10", "J"]
        cv2.putText(image, community_cards[i], (x + 10, community_y + 30), font, 1, (0, 0, 0), 2)
    
    return image

def run_demo_mode(analyzer):
    """Ejecutar demostración con situaciones predefinidas"""
    print("\n MODO DEMOSTRACIÓN")
    print("="*50)
    
    # Situaciones de ejemplo
    demo_situations = [
        {
            "name": "Preflop con AA desde posición temprana",
            "hero_cards": [Card("A", "", (0,0), 0.9), Card("A", "", (0,0), 0.9)],
            "community_cards": [],
            "pot_size": 15,
            "position": "early",
            "players_active": 8,
            "street": "preflop",
            "action_to_hero": "raise",
            "bet_size": 10
        },
        {
            "name": "Flop con top pair",
            "hero_cards": [Card("A", "", (0,0), 0.9), Card("K", "", (0,0), 0.9)],
            "community_cards": [Card("A", "", (0,0), 0.9), Card("7", "", (0,0), 0.9), Card("2", "", (0,0), 0.9)],
            "pot_size": 50,
            "position": "late",
            "players_active": 3,
            "street": "flop",
            "action_to_hero": "check",
            "bet_size": 0
        },
        {
            "name": "River con flush draw incompleto",
            "hero_cards": [Card("Q", "", (0,0), 0.9), Card("J", "", (0,0), 0.9)],
            "community_cards": [
                Card("A", "", (0,0), 0.9), Card("7", "", (0,0), 0.9), 
                Card("2", "", (0,0), 0.9), Card("9", "", (0,0), 0.9),
                Card("3", "", (0,0), 0.9)
            ],
            "pot_size": 100,
            "position": "middle",
            "players_active": 2,
            "street": "river",
            "action_to_hero": "bet",
            "bet_size": 30
        }
    ]
    
    for i, situation_data in enumerate(demo_situations, 1):
        print(f"\n SITUACIÓN {i}: {situation_data['name']}")
        print("-"*40)
        
        # Crear objeto situación
        situation = TableSituation(**situation_data)
        print(situation)
        
        # Analizar
        analysis = analyzer.analyze_situation(situation)
        
        print(f"\n RECOMENDACIÓN GTO:")
        print(f"  Acción: {analysis['action']}")
        print(f"  Confianza: {analysis['confidence']:.1%}")
        print(f"  Razón: {analysis['reason']}")
        
        if i < len(demo_situations):
            input("\nPresione Enter para siguiente situación...")

if __name__ == "__main__":
    main()
