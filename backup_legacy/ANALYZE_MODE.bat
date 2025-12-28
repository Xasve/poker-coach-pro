@echo off
chcp 65001 > nul
echo  MODO AN?LISIS - ESTUDIO PROFUNDO
echo ====================================
echo Tiempo: 10+s por decisi?n
echo Objetivo: Aprender patrones
echo Analiza: 100+ variables
echo.
python "professional_system\professional_validation.py" --mode analyze --depth 10
pause
