"""
Configuración para Poker Coach Pro
"""
import os

# Configuración del sistema
class Config:
    # Modo de operación
    DEMO_MODE = True  # Cambiar a False cuando GG Poker esté listo
    
    # Parámetros del motor
    ENGINE_AGGRESSION = 1.0  # 0.5 = pasivo, 1.0 = normal, 1.5 = agresivo
    ENGINE_TIGHTNESS = 1.0   # 0.5 = loose, 1.0 = normal, 1.5 = tight
    
    # Visualización
    DISPLAY_DELAY = 3  # Segundos entre manos en modo demo
    SHOW_ALTERNATIVES = True
    
    # Archivos y directorios
    LOG_DIR = "logs"
    DATA_DIR = "data"
    CARD_TEMPLATES_DIR = os.path.join(DATA_DIR, "card_templates")
    
    @classmethod
    def setup_directories(cls):
        """Crear directorios necesarios"""
        os.makedirs(cls.LOG_DIR, exist_ok=True)
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        os.makedirs(cls.CARD_TEMPLATES_DIR, exist_ok=True)
