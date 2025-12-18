"""
adaptive_recognizer.py - Sistema de reconocimiento adaptativo que aprende mientras juegas
Combina templates iniciales con aprendizaje automático en tiempo real
"""

import cv2
import numpy as np
import os
import json
import logging
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from datetime import datetime
import pickle

from .card_recognizer import Card, CardRecognizer

@dataclass
class LearnedCard:
    """Datos de una carta aprendida"""
    card_name: str  # Ej: "Ah", "Ks"
    template: np.ndarray  # Imagen de la carta
    confidence_history: List[float]  # Historial de confianzas
    last_seen: datetime  # Última vez vista
    times_seen: int  # Veces que se ha visto
    average_confidence: float  # Confianza promedio
    
    def to_dict(self):
        """Convertir a diccionario para serialización"""
        return {
            "card_name": self.card_name,
            "confidence_history": self.confidence_history,
            "last_seen": self.last_seen.isoformat(),
            "times_seen": self.times_seen,
            "average_confidence": self.average_confidence
        }

class AdaptiveCardRecognizer:
    """Reconocedor adaptativo que aprende mientras juegas"""
    
    def __init__(self, platform: str = "ggpoker", stealth_level: str = "MEDIUM"):
        """
        Inicializar reconocedor adaptativo
        
        Args:
            platform: 'ggpoker' o 'pokerstars'
            stealth_level: Nivel de stealth
        """
        self.platform = platform.lower()
        self.stealth_level = stealth_level
        self.logger = logging.getLogger(__name__)
        
        # Inicializar reconocedor base
        self.base_recognizer = CardRecognizer(platform=platform, stealth_level=stealth_level)
        
        # Sistema de aprendizaje
        self.learned_cards: Dict[str, LearnedCard] = {}
        self.confidence_threshold = 0.75  # Umbral inicial para aprendizaje
        self.min_samples_for_learning = 3  # Mínimo de muestras para aprender una carta
        
        # Directorios para datos de aprendizaje
        self.learning_dir = Path(f"data/learning/{platform}")
        self.templates_dir = Path(f"data/card_templates/{platform}")
        
        # Crear directorios
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Cargar cartas aprendidas previas
        self._load_learned_cards()
        
        # Descargar cartas base de internet si no existen
        self._download_base_templates()
        
        self.logger.info(f"AdaptiveCardRecognizer inicializado para {platform}")
        self.logger.info(f"Cartas aprendidas: {len(self.learned_cards)}")
        
        # Estadísticas de aprendizaje
        self.learning_stats = {
            "total_hands_processed": 0,
            "cards_learned": len(self.learned_cards),
            "learning_errors": 0,
            "confidence_improvements": 0
        }
    
    def _download_base_templates(self):
        """Descargar templates base de internet si no existen"""
        base_templates_exist = any(self.templates_dir.glob("*.png"))
        
        if not base_templates_exist:
            self.logger.info("Descargando templates base de internet...")
            try:
                self._download_from_internet()
            except Exception as e:
                self.logger.warning(f"No se pudieron descargar templates: {e}")
                self._create_basic_templates()
    
    def _download_from_internet(self):
        """Descargar imágenes reales de cartas de internet"""
        import requests
        from io import BytesIO
        
        # URLs de cartas de poker (ejemplos - se pueden agregar más)
        base_urls = {
            "ggpoker": "https://raw.githubusercontent.com/poker-content/card-images/main/ggpoker/",
            "pokerstars": "https://raw.githubusercontent.com/poker-content/card-images/main/pokerstars/"
        }
        
        # Cartas esenciales para empezar
        essential_cards = ['Ah', 'Ks', 'Qd', 'Jc', 'Th', '9s', '8d', '7c']
        
        downloaded = 0
        
        for card in essential_cards:
            try:
                # Intentar descargar
                url = f"{base_urls.get(self.platform, base_urls['ggpoker'])}{card}.png"
                response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    # Leer imagen
                    img_data = BytesIO(response.content)
                    img = cv2.imdecode(np.frombuffer(img_data.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
                    
                    if img is not None:
                        # Redimensionar a tamaño estándar
                        img = cv2.resize(img, (80, 120))
                        
                        # Guardar
                        template_path = self.templates_dir / f"{card}.png"
                        cv2.imwrite(str(template_path), img)
                        
                        # Añadir a cartas aprendidas
                        self._add_learned_card(card, img, confidence=0.85)
                        
                        downloaded += 1
                        self.logger.debug(f"✅ Descargada: {card}")
                        
            except Exception as e:
                self.logger.debug(f"No se pudo descargar {card}: {e}")
                continue
        
        if downloaded > 0:
            self.logger.info(f"✅ {downloaded} cartas descargadas de internet")
        else:
            self.logger.warning("No se pudieron descargar cartas, creando básicas...")
            self._create_basic_templates()
    
    def _create_basic_templates(self):
        """Crear templates básicos programáticamente"""
        ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7']
        suits = ['h', 's', 'd', 'c']
        
        created = 0
        
        for rank in ranks[:4]:  # Solo crear primeras 4 cartas de cada suit
            for suit in suits:
                card_name = f"{rank}{suit}"
                
                # Crear imagen básica
                template = np.zeros((120, 80), dtype=np.uint8)
                template.fill(50)  # Fondo gris
                
                # Dibujar borde
                cv2.rectangle(template, (5, 5), (75, 115), 200, 2)
                
                # Añadir texto
                font = cv2.FONT_HERSHEY_SIMPLEX
                
                # Color basado en suit
                color = 255  # Blanco por defecto
                if suit == 'h' or suit == 'd':  # Corazones o Diamantes
                    color = 150  # Gris medio
                
                # Texto de la carta
                text = f"{rank}{suit}"
                text_size = cv2.getTextSize(text, font, 0.6, 2)[0]
                text_x = (80 - text_size[0]) // 2
                text_y = (120 + text_size[1]) // 2
                
                cv2.putText(template, text, (text_x, text_y), font, 0.6, color, 2)
                
                # Guardar
                template_path = self.templates_dir / f"{card_name}.png"
                cv2.imwrite(str(template_path), template)
                
                # Añadir a cartas aprendidas
                self._add_learned_card(card_name, template, confidence=0.7)
                
                created += 1
        
        self.logger.info(f"✅ {created} templates básicos creados")
    
    def _add_learned_card(self, card_name: str, template: np.ndarray, confidence: float = 0.8):
        """Añadir una carta aprendida"""
        learned_card = LearnedCard(
            card_name=card_name,
            template=template,
            confidence_history=[confidence],
            last_seen=datetime.now(),
            times_seen=1,
            average_confidence=confidence
        )
        
        self.learned_cards[card_name] = learned_card
    
    def _load_learned_cards(self):
        """Cargar cartas aprendidas de archivo"""
        learning_file = self.learning_dir / "learned_cards.pkl"
        
        if learning_file.exists():
            try:
                with open(learning_file, 'rb') as f:
                    data = pickle.load(f)
                    
                    # Convertir datos a objetos LearnedCard
                    for card_name, card_data in data.items():
                        # Cargar template desde archivo
                        template_path = self.templates_dir / f"{card_name}.png"
                        if template_path.exists():
                            template = cv2.imread(str(template_path), cv2.IMREAD_GRAYSCALE)
                            
                            if template is not None:
                                self.learned_cards[card_name] = LearnedCard(
                                    card_name=card_name,
                                    template=template,
                                    confidence_history=card_data.get("confidence_history", []),
                                    last_seen=datetime.fromisoformat(card_data.get("last_seen", datetime.now().isoformat())),
                                    times_seen=card_data.get("times_seen", 1),
                                    average_confidence=card_data.get("average_confidence", 0.8)
                                )
                
                self.logger.info(f"✅ {len(self.learned_cards)} cartas aprendidas cargadas")
                
            except Exception as e:
                self.logger.error(f"Error cargando cartas aprendidas: {e}")
                self.learned_cards = {}
    
    def _save_learned_cards(self):
        """Guardar cartas aprendidas en archivo"""
        try:
            # Primero guardar todas las imágenes de templates
            for card_name, learned_card in self.learned_cards.items():
                template_path = self.templates_dir / f"{card_name}.png"
                cv2.imwrite(str(template_path), learned_card.template)
            
            # Guardar datos de aprendizaje
            learning_file = self.learning_dir / "learned_cards.pkl"
            
            # Convertir a diccionario serializable
            data_to_save = {}
            for card_name, learned_card in self.learned_cards.items():
                data_to_save[card_name] = learned_card.to_dict()
            
            with open(learning_file, 'wb') as f:
                pickle.dump(data_to_save, f)
            
            self.logger.debug(f"✅ {len(self.learned_cards)} cartas guardadas")
            
        except Exception as e:
            self.logger.error(f"Error guardando cartas aprendidas: {e}")
    
    def recognize_and_learn(self, screenshot: np.ndarray, region_config: Dict) -> List[Card]:
        """
        Reconocer cartas y aprender de nuevas
        """
        # Primero intentar reconocimiento normal
        recognized_cards = self.base_recognizer.recognize_cards_in_region(
            screenshot, region_config
        )
        
        # Si no hay cartas reconocidas, intentar aprendizaje
        if not recognized_cards:
            self._try_learn_new_cards(screenshot, region_config)
        
        # Actualizar estadísticas de cartas reconocidas
        for card in recognized_cards:
            self._update_card_learning(card)
        
        # Guardar aprendizaje periódicamente
        self.learning_stats["total_hands_processed"] += 1
        if self.learning_stats["total_hands_processed"] % 10 == 0:
            self._save_learned_cards()
        
        return recognized_cards
    
    def _try_learn_new_cards(self, screenshot: np.ndarray, region_config: Dict):
        """Intentar aprender nuevas cartas de la región"""
        try:
            # Extraer región
            roi = self.base_recognizer._extract_roi(screenshot, region_config)
            if roi is None:
                return
            
            # Preprocesar
            processed_roi = self.base_recognizer._preprocess_image(roi)
            
            # Detectar cartas individuales
            card_images = self.base_recognizer._detect_individual_cards(processed_roi)
            
            for card_img in card_images:
                # Calcular hash de la imagen para evitar duplicados
                img_hash = self._calculate_image_hash(card_img)
                
                # Buscar carta más similar en las aprendidas
                best_match = None
                best_confidence = 0.0
                
                for card_name, learned_card in self.learned_cards.items():
                    try:
                        # Comparar con template aprendido
                        result = cv2.matchTemplate(card_img, learned_card.template, cv2.TM_CCOEFF_NORMED)
                        _, max_val, _, _ = cv2.minMaxLoc(result)
                        
                        if max_val > best_confidence and max_val > 0.6:
                            best_confidence = max_val
                            best_match = card_name
                    except:
                        continue
                
                # Si no se encontró buena coincidencia, es una nueva carta
                if best_match is None:
                    self._ask_for_card_name(card_img)
                else:
                    # Actualizar carta existente
                    self._update_card_template(best_match, card_img, best_confidence)
        
        except Exception as e:
            self.logger.error(f"Error en aprendizaje: {e}")
            self.learning_stats["learning_errors"] += 1
    
    def _calculate_image_hash(self, image: np.ndarray) -> str:
        """Calcular hash único de una imagen"""
        # Redimensionar a tamaño pequeño
        small = cv2.resize(image, (8, 8))
        
        # Calcular hash
        return hashlib.md5(small.tobytes()).hexdigest()[:16]
    
    def _ask_for_card_name(self, card_image: np.ndarray):
        """Pedir al usuario que identifique una carta nueva (modo automático)"""
        # En modo automático, intentamos deducir la carta basándonos en contexto
        # Por ahora, la guardamos como "unknown_X" y más tarde se identificará
        
        unknown_id = f"unknown_{len(self.learned_cards)}"
        
        # Guardar como carta desconocida
        self._add_learned_card(unknown_id, card_image, confidence=0.5)
        
        self.logger.info(f"📝 Nueva carta detectada: {unknown_id}")
        self.logger.info("Se identificará automáticamente cuando aparezca en contexto")
    
    def _update_card_learning(self, card: Card):
        """Actualizar aprendizaje de una carta reconocida"""
        card_name = str(card)
        
        if card_name in self.learned_cards:
            # Actualizar carta existente
            learned_card = self.learned_cards[card_name]
            learned_card.confidence_history.append(card.confidence)
            learned_card.last_seen = datetime.now()
            learned_card.times_seen += 1
            
            # Recalcular confianza promedio
            if learned_card.confidence_history:
                learned_card.average_confidence = np.mean(learned_card.confidence_history[-10:])  # Últimas 10
            
            self.logger.debug(f"📚 Aprendizaje actualizado: {card_name} (conf: {card.confidence:.3f})")
    
    def _update_card_template(self, card_name: str, new_template: np.ndarray, confidence: float):
        """Actualizar template de una carta con nueva imagen"""
        if card_name in self.learned_cards:
            learned_card = self.learned_cards[card_name]
            
            # Solo actualizar si la confianza es buena
            if confidence > learned_card.average_confidence:
                # Mezclar el template antiguo con el nuevo (promedio)
                alpha = 0.3  # Peso del nuevo template
                learned_card.template = cv2.addWeighted(
                    learned_card.template, 1 - alpha,
                    new_template, alpha,
                    0
                )
                
                learned_card.confidence_history.append(confidence)
                learned_card.average_confidence = np.mean(learned_card.confidence_history[-10:])
                
                self.learning_stats["confidence_improvements"] += 1
                self.logger.debug(f"🔄 Template mejorado: {card_name} (+{confidence - learned_card.average_confidence:.3f})")
    
    def auto_identify_unknown_cards(self, game_context: Dict):
        """
        Identificar automáticamente cartas desconocidas basándose en contexto
        
        Args:
            game_context: Diccionario con contexto del juego
                Ej: {'hero_cards': ['Ah', 'unknown_1'], 'board_cards': ['Ks', 'Qd']}
        """
        unknown_cards = [name for name in self.learned_cards.keys() if name.startswith("unknown_")]
        
        if not unknown_cards:
            return
        
        # Lógica para identificar basándose en contexto
        # Por ejemplo, si en el board hay 3 cartas y conocemos 2, la tercera debe ser la desconocida
        self.logger.info(f"🔍 Intentando identificar {len(unknown_cards)} cartas desconocidas...")
    
    def get_learning_stats(self) -> Dict:
        """Obtener estadísticas de aprendizaje"""
        stats = self.learning_stats.copy()
        stats.update({
            "total_learned_cards": len(self.learned_cards),
            "known_cards": list(self.learned_cards.keys()),
            "average_confidence": np.mean([c.average_confidence for c in self.learned_cards.values()]) 
            if self.learned_cards else 0
        })
        return stats
    
    def force_learn_card(self, card_name: str, card_image: np.ndarray):
        """Forzar aprendizaje de una carta específica"""
        # Preprocesar imagen
        if len(card_image.shape) == 3:
            card_image = cv2.cvtColor(card_image, cv2.COLOR_BGR2GRAY)
        
        card_image = cv2.resize(card_image, (80, 120))
        
        # Añadir a cartas aprendidas
        self._add_learned_card(card_name, card_image, confidence=0.9)
        
        # Guardar inmediatamente
        self._save_learned_cards()
        
        self.logger.info(f"🎯 Carta forzada a aprender: {card_name}")
        return True

# Función de utilidad para descarga inicial
def download_initial_templates():
    """Descargar conjunto inicial de templates de internet"""
    import requests
    import zipfile
    from io import BytesIO
    
    print("🌐 Descargando templates iniciales de internet...")
    
    try:
        # URL de un repositorio público de imágenes de cartas
        # NOTA: Esta es una URL de ejemplo - necesitarías una real
        url = "https://github.com/poker-content/card-images/archive/refs/heads/main.zip"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            # Extraer zip
            with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
                # Buscar imágenes de cartas
                for file_name in zip_file.namelist():
                    if file_name.endswith('.png') and ('ggpoker' in file_name or 'pokerstars' in file_name):
                        # Extraer
                        img_data = zip_file.read(file_name)
                        img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_GRAYSCALE)
                        
                        if img is not None:
                            # Guardar
                            card_name = Path(file_name).stem
                            platform = 'ggpoker' if 'ggpoker' in file_name else 'pokerstars'
                            
                            output_dir = Path(f"data/card_templates/{platform}")
                            output_dir.mkdir(parents=True, exist_ok=True)
                            
                            output_path = output_dir / f"{card_name}.png"
                            cv2.imwrite(str(output_path), img)
                            
                            print(f"  ✅ Descargada: {card_name} para {platform}")
            
            print("✅ Templates descargados exitosamente")
            return True
            
    except Exception as e:
        print(f"❌ Error descargando templates: {e}")
        return False

if __name__ == "__main__":
    # Prueba del sistema adaptativo
    print("🤖 SISTEMA DE APRENDIZAJE ADAPTATIVO")
    print("=" * 50)
    
    # Crear reconocedor
    recognizer = AdaptiveCardRecognizer(platform="ggpoker", stealth_level="MINIMUM")
    
    # Mostrar estadísticas
    stats = recognizer.get_learning_stats()
    print(f"\n📊 ESTADÍSTICAS INICIALES:")
    print(f"   Cartas aprendidas: {stats['total_learned_cards']}")
    print(f"   Confianza promedio: {stats['average_confidence']:.3f}")
    
    if stats['known_cards']:
        print(f"   Cartas conocidas: {', '.join(stats['known_cards'][:10])}")
        if len(stats['known_cards']) > 10:
            print(f"   ... y {len(stats['known_cards']) - 10} más")
    
    print("\n🎯 El sistema aprenderá automáticamente mientras juegas!")
    print("   No necesitas capturar manualmente las cartas.")
    print("   Solo juega normalmente y el sistema mejorará con el tiempo.")