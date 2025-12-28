# create_structure.py - Ejecutar en la raíz del proyecto
import os

print('🏗️ CREANDO ESTRUCTURA DE DIRECTORIOS...')

# Directorios a crear
directories = [
    'data/card_templates/pokerstars/hearts',
    'data/card_templates/pokerstars/diamonds', 
    'data/card_templates/pokerstars/clubs',
    'data/card_templates/pokerstars/spades',
    'data/card_templates/ggpoker/hearts',
    'data/card_templates/ggpoker/diamonds',
    'data/card_templates/ggpoker/clubs',
    'data/card_templates/ggpoker/spades',
    'debug/captures',
    'debug/recognitions',
    'logs',
    'hand_history',
    'config'
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f'✅ Creado: {directory}/')

print('\n📄 CREANDO ARCHIVOS DE CONFIGURACIÓN...')

# Archivo: config/settings.json
with open('config/settings.json', 'w') as f:
    f.write('''{
    "stealth_level": 1,
    "capture_delay": 0.5,
    "overlay_opacity": 0.8,
    "analysis_delay": 0.3,
    "auto_adjust": true
}''')
print('✅ Creado: config/settings.json')

# Archivo: config/strategies.json
with open('config/strategies.json', 'w') as f:
    f.write('''{
    "default_strategy": "gto_basic",
    "aggression_factor": 0.7,
    "risk_tolerance": 0.5,
    "bluff_frequency": 0.25
}''')
print('✅ Creado: config/strategies.json')

# Archivo: config/platforms.json
with open('config/platforms.json', 'w') as f:
    f.write('''{
    "pokerstars": {
        "table_color": [0, 100, 0],
        "card_size": [71, 96],
        "table_region": [0, 0, 1920, 1080]
    },
    "ggpoker": {
        "table_color": [30, 60, 30],
        "card_size": [75, 100],
        "table_region": [0, 0, 1920, 1080]
    }
}''')
print('✅ Creado: config/platforms.json')

print('\n🎯 ESTRUCTURA COMPLETADA!')