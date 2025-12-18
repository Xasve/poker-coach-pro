#!/bin/bash

# Poker Coach Pro - Instalador de dependencias (Linux/Mac)

echo "========================================"
echo "   INSTALANDO POKER COACH PRO"
echo "========================================"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no encontrado"
    echo "Instala Python desde: https://python.org"
    exit 1
fi

echo "✅ Python3 detectado"
echo ""

# Crear entorno virtual (opcional)
read -p "¿Crear entorno virtual? (s/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "🧪 Creando entorno virtual..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Instalar dependencias
echo "📦 Instalando dependencias de Python..."
pip install --upgrade pip

# Dependencias básicas
pip install opencv-python numpy pillow pytesseract pandas

# Dependencias de captura
pip install mss pyautogui

# Dependencias de red y comunicación
pip install websockets python-socketio

# Base de datos
pip install tinydb

# Para Windows (opcional)
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "🪟 Instalando dependencias específicas de Windows..."
    pip install pywin32 pypiwin32
fi

# Dependencias de desarrollo
read -p "¿Instalar dependencias de desarrollo? (s/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "🔧 Instalando herramientas de desarrollo..."
    pip install pytest black flake8
fi

# Crear directorios necesarios
echo "🎴 Creando estructura de directorios..."

mkdir -p data/card_templates/ggpoker
mkdir -p data/card_templates/pokerstars
mkdir -p data/table_templates
mkdir -p data/fonts
mkdir -p data/logs
mkdir -p data/hand_history

echo ""
echo "✅ Instalación completada!"
echo ""
echo "Para iniciar el sistema:"
echo "   1. Abre GG Poker o PokerStars"
echo "   2. Ejecuta: python start_coach.py"
echo "   3. Selecciona tu plataforma"
echo ""
echo "Para modo stealth avanzado:"
echo "   python scripts/stealth_launcher.py"
echo ""
echo "🎯 Consejo: Empieza con stakes bajos para familiarizarte"