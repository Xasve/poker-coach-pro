"""
PokerStars Adapter REAL - Con captura de pantalla real
"""
import time
import logging
import random
from typing import Optional, Dict, Any
from dataclasses import dataclass

# Importar screen_capture
import sys
sys.path.insert(0, 'src')

try:
    from screen_capture.stealth_capture import StealthScreenCapture
    from screen_capture.card_recognizer import CardRecognizer
    from screen_capture.table_detector import TableDetector
    from screen_capture.text_ocr import TextOCR
    SCREEN_CAPTURE_AVAILABLE = True
except ImportError as e:
    print(f\"  No se pudo importar screen_capture: {e}\")
    SCREEN_CAPTURE_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class RealPokerStarsGameState:
    """Estado REAL del juego en PokerStars"""
    hero_cards: list = None
    community_cards: list = None
    street: str = ""
    position: str = ""
    pot: int = 0
    stack: int = 0
    to_call: int = 0
    min_raise: int = 0
    max_raise: int = 0
    actions_available: list = None
    is_real_capture: bool = False  # True si es captura real, False si es simulación
    
    def __post_init__(self):
        if self.hero_cards is None:
            self.hero_cards = []
        if self.community_cards is None:
            self.community_cards = []
        if self.actions_available is None:
            self.actions_available = []
    
    def is_valid(self) -> bool:
        """Verificar si el estado es válido"""
        return bool(self.hero_cards) and self.street
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario"""
        return {
            "hero_cards": self.hero_cards,
            "community_cards": self.community_cards,
            "street": self.street,
            "position": self.position,
            "pot": self.pot,
            "stack": self.stack,
            "to_call": self.to_call,
            "min_raise": self.min_raise,
            "max_raise": self.max_raise,
            "actions_available": self.actions_available,
            "is_real_capture": self.is_real_capture
        }

class RealPokerStarsAdapter:
    """Adaptador que INTENTA captura REAL de PokerStars"""
    
    def __init__(self, stealth_level: str = "MEDIUM"):
        self.logger = logging.getLogger(__name__)
        self.stealth_level = stealth_level
        self.hand_history = []
        self.current_hand_id = None
        
        # Inicializar componentes si están disponibles
        if SCREEN_CAPTURE_AVAILABLE:
            try:
                self.capture_system = StealthScreenCapture("POKERSTARS", stealth_level)
                self.card_recognizer = CardRecognizer("pokerstars", stealth_level)
                self.table_detector = TableDetector("pokerstars")
                self.text_ocr = TextOCR("pokerstars")
                self.real_capture_available = True
                print(" Componentes de captura REAL inicializados")
            except Exception as e:
                print(f"  Error inicializando captura real: {e}")
                self.real_capture_available = False
        else:
            self.real_capture_available = False
        
        if not self.real_capture_available:
            print("  Usando modo SIMULACIÓN (captura real no disponible)")
        
        self.logger.info(f" RealPokerStarsAdapter inicializado")
    
    def is_pokerstars_active(self) -> bool:
        """Verificar si PokerStars está activo"""
        if not self.real_capture_available:
            return False  # Sin captura real, no podemos verificar
        
        try:
            # Intentar capturar pantalla
            screenshot = self.capture_system.capture()
            if screenshot is None:
                return False
            
            # Aquí iría la lógica REAL de detección de PokerStars
            # Por ahora, verificar si hay algo en pantalla
            if screenshot.size > 0:
                # Simplemente asumir que PokerStars está abierto
                # (En producción, aquí habría detección de ventana específica)
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Error verificando PokerStars: {e}")
            return False
    
    def capture_and_analyze(self) -> Optional[RealPokerStarsGameState]:
        """
        Intentar captura REAL, si falla usar simulación
        """
        state = None
        
        # PRIMERO: Intentar captura real
        if self.real_capture_available:
            state = self._try_real_capture()
        
        # SEGUNDO: Si falló la captura real, usar simulación
        if state is None:
            state = self._create_simulated_state()
            if state:
                state.is_real_capture = False
        
        # TERCERO: Guardar en historial
        if state and state.hero_cards:
            self._save_to_history(state)
        
        return state
    
    def _try_real_capture(self) -> Optional[RealPokerStarsGameState]:
        """Intentar captura REAL de PokerStars"""
        try:
            self.logger.debug("Intentando captura REAL...")
            
            # 1. Capturar pantalla
            screenshot = self.capture_system.capture()
            if screenshot is None:
                self.logger.warning("No se pudo capturar pantalla")
                return None
            
            # 2. Detectar mesa
            table_info = self.table_detector.detect_table(screenshot)
            if not table_info or not table_info.get("found", False):
                self.logger.debug("Mesa no detectada en captura real")
                return None
            
            # 3. Extraer cartas (usando reconocimiento simulado por ahora)
            hero_cards = self.card_recognizer.recognize_hero_cards(screenshot)
            community_cards = self.card_recognizer.recognize_community_cards(screenshot)
            
            # 4. Extraer montos
            amounts = self.text_ocr.extract_amounts(screenshot)
            
            # 5. Detectar calle basada en cartas comunitarias
            street = self._detect_street_from_cards(community_cards)
            
            # 6. Crear estado REAL
            game_state = RealPokerStarsGameState(
                hero_cards=hero_cards,
                community_cards=community_cards,
                street=street,
                position=self._detect_position(screenshot),  # Simulado por ahora
                pot=amounts.get("pot", 0),
                stack=amounts.get("stack", 0),
                to_call=amounts.get("to_call", 0),
                min_raise=amounts.get("min_raise", 0),
                max_raise=amounts.get("max_raise", 0),
                actions_available=self._detect_available_actions(screenshot),
                is_real_capture=True
            )
            
            self.logger.info(f" Captura REAL exitosa: {street} - Cartas: {hero_cards}")
            return game_state
            
        except Exception as e:
            self.logger.error(f"Error en captura real: {e}")
            return None
    
    def _create_simulated_state(self) -> RealPokerStarsGameState:
        """Crear estado simulado (fallback)"""
        # Mazo completo
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = ['h', 'd', 'c', 's']
        
        deck = [f"{rank}{suit}" for rank in ranks for suit in suits]
        random.shuffle(deck)
        
        # Cartas del héroe
        hero_cards = [deck.pop(), deck.pop()]
        
        # Calle actual
        streets = [("preflop", 0), ("flop", 3), ("turn", 4), ("river", 5)]
        street_name, num_community = random.choice(streets)
        community_cards = [deck.pop() for _ in range(num_community)] if num_community > 0 else []
        
        # Valores realistas
        pot = random.randint(100, 1000)
        stack = random.randint(1000, 5000)
        to_call = random.randint(0, 200) if random.random() > 0.3 else 0
        
        # Acciones disponibles realistas
        if to_call > 0:
            actions = ['FOLD', 'CALL']
            if random.random() > 0.4:
                actions.append('RAISE')
        else:
            actions = ['CHECK']
            if random.random() > 0.5:
                actions.append('BET')
        
        if stack > pot * 1.5:
            actions.append('ALL-IN')
        
        # Crear estado
        state = RealPokerStarsGameState(
            hero_cards=hero_cards,
            community_cards=community_cards,
            street=street_name,
            position=random.choice(['UTG', 'MP', 'CO', 'BTN', 'SB', 'BB']),
            pot=pot,
            stack=stack,
            to_call=to_call,
            min_raise=max(20, to_call * 2) if to_call > 0 else 50,
            max_raise=stack,
            actions_available=actions,
            is_real_capture=False
        )
        
        self.logger.info(f"Estado SIMULADO: {street_name} - Cartas: {hero_cards}")
        return state
    
    def _detect_street_from_cards(self, community_cards) -> str:
        """Detectar calle basada en cartas comunitarias"""
        if not community_cards:
            return "preflop"
        elif len(community_cards) == 3:
            return "flop"
        elif len(community_cards) == 4:
            return "turn"
        elif len(community_cards) == 5:
            return "river"
        else:
            return "unknown"
    
    def _detect_position(self, screenshot) -> str:
        """Detectar posición (simulado por ahora)"""
        positions = ['UTG', 'MP', 'CO', 'BTN', 'SB', 'BB']
        return random.choice(positions)
    
    def _detect_available_actions(self, screenshot) -> list:
        """Detectar acciones disponibles (simulado)"""
        return random.sample(['FOLD', 'CHECK', 'CALL', 'RAISE', 'ALL-IN'], 3)
    
    def _save_to_history(self, game_state: RealPokerStarsGameState):
        """Guardar estado en historial"""
        hand_data = {
            "timestamp": time.time(),
            "hand_id": self.current_hand_id or f"hand_{int(time.time())}",
            "state": game_state.to_dict(),
            "is_real_capture": game_state.is_real_capture
        }
        self.hand_history.append(hand_data)
        
        # Mantener solo las últimas 100 manos
        if len(self.hand_history) > 100:
            self.hand_history = self.hand_history[-100:]
    
    def save_hand_history(self, game_state: RealPokerStarsGameState, decision: Dict[str, Any]):
        """Guardar decisión en historial"""
        if self.hand_history:
            last_hand = self.hand_history[-1]
            last_hand["decision"] = decision
            last_hand["decision_time"] = time.time()
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de la sesión"""
        real_captures = len([h for h in self.hand_history if h.get("is_real_capture", False)])
        
        return {
            "total_hands": len(self.hand_history),
            "real_captures": real_captures,
            "simulated_captures": len(self.hand_history) - real_captures,
            "hands_with_decisions": len([h for h in self.hand_history if "decision" in h]),
            "platform": "PokerStars"
        }
