# TEMPLATES DE CARTAS DE POKER

## Estructura
data/card_templates/
├── ggpoker/ # Templates para GG Poker
│ ├── Ah.png
│ ├── Kh.png
│ ├── ...
│ └── template_map.json
├── pokerstars/ # Templates para PokerStars
│ ├── Ah.png
│ ├── Kh.png
│ ├── ...
│ └── template_map.json
└── README.md

## Generar Templates

### Método 1: Generador Automático
```bash
python scripts/generate_card_templates.py