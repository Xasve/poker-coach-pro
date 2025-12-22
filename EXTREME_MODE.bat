@echo off
chcp 65001 > nul
echo  MODO EXTREMO - VELOCIDAD M?XIMA
echo ===================================
echo Tiempo: 0.5-1s por decisi?n
echo Objetivo: M?ximo volumen
echo Winrate: 58-62% esperado
echo.
python "extreme_optimization\extreme_bot_simple.py" --mode extreme --speed 1
pause
