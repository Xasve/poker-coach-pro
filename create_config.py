# create_config.py
import os
import yaml

def create_default_config():
    """Crear configuración por defecto"""
    
    config = {
        'capture': {
            'stealth_level': 'MEDIUM',
            'region': None,  # Auto-detect
            'capture_interval': 0.5,
            'debug_save_captures': False
        },
        'recognition': {
            'card_matching_threshold': 0.8,
            'table_detection_confidence': 0.7,
            'ocr_engine': 'tesseract',
            'ocr_language': 'eng'
        },
        'platforms': {
            'default': 'pokerstars',
            'supported': ['pokerstars', 'ggpoker'],
            'pokerstars': {
                'card_template_path': 'data/card_templates/pokerstars/',
                'table_regions': {
                    'cards_hero': [100, 200, 150, 50],
                    'cards_community': [300, 150, 400, 80],
                    'pot_region': [400, 100, 200, 40]
                }
            }
        },
        'overlay': {
            'enabled': True,
            'position': 'top_right',
            'transparency': 0.9,
            'font_size': 14,
            'show_recommendations': True,
            'show_odds': True,
            'show_gto_suggestions': True
        },
        'gto': {
            'engine': 'basic',
            'update_interval': 1.0,
            'cache_size': 100
        },
        'logging': {
            'level': 'INFO',
            'file': 'logs/poker_coach.log',
            'max_size_mb': 10
        }
    }
    
    # Crear directorio si no existe
    os.makedirs('config', exist_ok=True)
    
    # Guardar configuración
    config_path = 'config/default_config.yaml'
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    print(f"✅ Configuración creada: {config_path}")
    print(f"📄 Tamaño: {os.path.getsize(config_path)} bytes")
    
    return config_path

if __name__ == "__main__":
    create_default_config()