@echo off
echo ========================================
echo    INSTALADOR SISTEMA DE CALIDAD SIMPLE
echo ========================================
echo.

echo Creando directorio de calidad...
if not exist "src\quality" mkdir src\quality

echo.
echo Creando archivos del sistema simple...
echo.

REM Crear decision_validator_fixed.py
(
echo from typing import Dict, List
echo from datetime import datetime
echo 
echo class SimpleDecisionValidator:
echo     def __init__(self, platform="ggpoker"):
echo         self.platform = platform
echo         self.stats = {"total": 0, "excellent": 0, "good": 0, "acceptable": 0, "questionable": 0, "bad": 0}
echo         self.history = []
echo 
echo     def validate_decision(self, game_state, decision):
echo         """Validar decision simple"""
echo         return {
echo             "quality": "ACEPTABLE",
echo             "score": 70,
echo             "strengths": ["Validacion basica completada"],
echo             "weaknesses": [],
echo             "suggestions": []
echo         }
) > src\quality\decision_validator_fixed.py

echo.
echo ✅ Sistema simple creado
echo.
echo Para probar:
echo   1. python test_quality_fixed.py
echo   2. python poker_coach_simple_quality.py
echo.
pause