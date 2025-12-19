#!/usr/bin/env python3
import os
import subprocess

print('=' * 50)
print('POKER COACH PRO - LAUNCHER DEFINITIVO')
print('=' * 50)

scripts = [
    ('1', 'test_pokerstars.py', 'Sistema PokerStars completo'),
    ('2', 'test_ggpoker_simple.py', 'Sistema GG Poker'),
    ('3', 'test_capture.py', 'Probar captura'),
    ('4', 'check.py', 'Verificar sistema'),
    ('5', 'cleanup.py', 'Limpiar archivos'),
    ('6', 'src/integration/pokerstars_coach.py', 'Integrador avanzado')
]

for num, script, desc in scripts:
    if os.path.exists(script):
        print(f'{num}. {script:30} - {desc}')

print('0. Salir')

choice = input('\\n Selecciona número: ')

for num, script, desc in scripts:
    if choice == num and os.path.exists(script):
        print(f'\\n Ejecutando: {script}')
        print('=' * 50)
        subprocess.run(['python', script])
        break
elif choice == '0':
    print('\\n Hasta pronto!')
else:
    print('\\n Opción inválida')
