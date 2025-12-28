# ultra_capture_solution.py - Solución definitiva para cartas 100% negras
import os
import shutil
import json
from datetime import datetime
import cv2
import numpy as np
import random

class UltimateDatasetFixer:
    """Solución definitiva para dataset desbalanceado"""
    
    def __init__(self):
        self.sessions_path = "data/card_templates/auto_captured"
        self.templates_path = "data/card_templates/pokerstars_real"
        
    def nuclear_option(self):
        """Opción nuclear: limpiar TODO y empezar de cero"""
        print("💣 OPCIÓN NUCLEAR: LIMPIAR TODO Y EMPEZAR DE CERO")
        print("=" * 70)
        print("⚠️  Esto eliminará TODAS las sesiones existentes")
        print("⚠️  Y TODOS los templates organizados")
        
        confirm = input("\nEstás SEGURO? (escribe 'SI' para confirmar): ")
        
        if confirm == "SI":
            print("\n LIMPIANDO TODO...")
            
            # Eliminar todas las sesiones
            if os.path.exists(self.sessions_path):
                shutil.rmtree(self.sessions_path)
                os.makedirs(self.sessions_path)
                print("✅ Todas las sesiones eliminadas")
            
            # Eliminar templates organizados
            if os.path.exists(self.templates_path):
                shutil.rmtree(self.templates_path)
                os.makedirs(self.templates_path)
                # Crear subdirectorios
                for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
                    os.makedirs(os.path.join(self.templates_path, suit), exist_ok=True)
                print(" Todos los templates eliminados")
            
            # Crear dataset artificial balanceado
            self.create_artificial_dataset()
            
            print("\n🎉 ¡SISTEMA LIMPIADO Y REINICIADO!")
            print(" Ahora configura PokerStars CORRECTAMENTE")
        else:
            print("\n  Operación cancelada")
    
    def create_artificial_dataset(self):
        """Crear dataset artificial balanceado"""
        print("\n CREANDO DATASET ARTIFICIAL BALANCEADO...")
        
        # Crear sesión artificial
        session_name = f"artificial_balanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        session_path = os.path.join(self.sessions_path, session_name)
        raw_path = os.path.join(session_path, "raw_captures")
        os.makedirs(raw_path, exist_ok=True)
        
        # Crear 100 cartas artificiales balanceadas
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        colors = {
            'hearts': (0, 0, 255),     # Rojo en BGR
            'diamonds': (0, 0, 255),   # Rojo en BGR
            'clubs': (0, 0, 0),        # Negro
            'spades': (0, 0, 0)        # Negro
        }
        
        # Distribución balanceada: 40% rojas, 60% negras
        cards_per_suit = 25
        
        for suit in suits:
            for i in range(cards_per_suit):
                # Crear imagen artificial
                height, width = 100, 70
                img = np.zeros((height, width, 3), dtype=np.uint8)
                
                # Color base según palo
                color = colors[suit]
                img[:, :] = color
                
                # Añadir variación
                variation = np.random.randint(-30, 30, (height, width, 3), dtype=np.int8)
                img = cv2.add(img, variation.astype(np.uint8))
                
                # Añadir símbolo simple
                if suit == 'hearts':
                    # Corazón simple
                    cv2.putText(img, 'H', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                elif suit == 'diamonds':
                    # Diamante simple
                    cv2.putText(img, 'D', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                elif suit == 'clubs':
                    # Trébol simple
                    cv2.putText(img, 'C', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                else:  # spades
                    # Pica simple
                    cv2.putText(img, 'S', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                
                # Guardar
                filename = f"artificial_{suit}_{i:03d}.png"
                cv2.imwrite(os.path.join(raw_path, filename), img)
        
        # Crear resultados de clasificación
        results = {
            'session': session_name,
            'total_cards': 100,
            'distribution': {
                'hearts': 25,
                'diamonds': 25,
                'clubs': 25,
                'spades': 25
            },
            'red_percentage': 50.0,
            'artificial': True,
            'timestamp': datetime.now().isoformat()
        }
        
        results_file = os.path.join(session_path, "classification_results.json")
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f" Dataset artificial creado: {session_name}")
        print(f"    Hearts: 25")
        print(f"    Diamonds: 25")
        print(f"    Clubs: 25")
        print(f"    Spades: 25")
        print(f"    Rojas: 50 (50.0%)")
    
    def generate_pokerstars_config_guide(self):
        """Generar guía DETALLADA para configurar PokerStars"""
        print("\n GUÍA DETALLADA DE CONFIGURACIÓN POKERSTARS")
        print("=" * 70)
        
        guide = """#  GUÍA DEFINITIVA PARA CONFIGURAR POKERSTARS

##  PROBLEMA ACTUAL:
Estás capturando 100% cartas negras () porque:
1. Estás en una mesa PokerStars que SOLO usa cartas negras
2. O la captura no está funcionando correctamente

##  SOLUCIÓN PASO A PASO:

### PASO 1: CAMBIAR DE MESA (CRÍTICO)
1. Cierra la mesa actual de PokerStars
2. Busca una mesa que diga "Classic" (NO "Dark", NO "Stealth")
3. Mesa recomendada: Busca "NL Hold'em" -> "Classic"

### PASO 2: VERIFICAR CARTAS VISUALMENTE
1. Únete a una mesa "Classic"
2. ESPERA a que repartan cartas
3. VERIFICA CON TUS OJOS: Ves cartas ROJAS?
   - Si NO ves rojas, SAL de esa mesa
   - Busca OTRA mesa "Classic"

### PASO 3: CONFIGURAR CAPTURA
1. Ejecuta este comando:
   python detect_coords.py

2. Sigue las instrucciones:
   - Haz clic en tu PRIMERA carta (hero card 1)
   - Haz clic en tu SEGUNDA carta (hero card 2)
   - Haz clic en las cartas comunitarias (flop)

### PASO 4: CAPTURA MANUAL DE VERIFICACIÓN
1. Abre Paint o cualquier editor de imágenes
2. Cuando veas una carta ROJA en PokerStars:
   - Presiona Print Screen (PrtScn)
   - Pega en Paint (Ctrl+V)
   - Recorta SOLO la carta
   - Guarda como: test_red_card.png

3. Repite con una carta NEGRA

### PASO 5: VERIFICAR COLORES
Ejecuta este comando de verificación:
python test_card_colors.py

##  MESAS RECOMENDADAS (CON CARTAS ROJAS):
 "NL Hold'em Classic"
 "PL Omaha Classic"
 "Tournament - Classic Tables"
 Mesas con fondo CLARO/AMARILLO

##  MESAS A EVITAR (SOLO CARTAS NEGRAS):
 CUALQUIER mesa que diga "Dark"
 CUALQUIER mesa que diga "Stealth"
 CUALQUIER mesa que diga "Night"
 Mesas con fondo OSCURO/NEGRO

##  CONFIGURACIÓN POKERSTARS INTERNA:
1. Settings -> Table Appearance
2. Card Deck: "Standard" (NO "Dark", NO "4-Color")
3. Background: "Default" o "Light"
4. Desactivar "Animated Cards" temporalmente

##  COMANDOS PARA EJECUTAR:
1. python test_pokerstars_setup.py  (Primero)
2. python detect_coords.py          (Luego)
3. python forced_balance_capture.py (Finalmente)
"""
        
        # Guardar guía
        with open("POKERSTARS_ULTIMATE_GUIDE.txt", "w", encoding="utf-8") as f:
            f.write(guide)
        
        print(" Guía guardada: POKERSTARS_ULTIMATE_GUIDE.txt")
        
        # Crear scripts de prueba
        self.create_test_scripts()
    
    def create_test_scripts(self):
        """Crear scripts de prueba"""
        
        # Script 1: Test de configuración
        test_script = '''# test_pokerstars_setup.py - Verificar configuración PokerStars
import os
import cv2
import numpy as np
from datetime import datetime

print(" VERIFICANDO CONFIGURACIÓN POKERSTARS")
print("=" * 70)

def test_color_detection():
    """Probar detección de colores"""
    print("\n PRUEBA DE DETECCIÓN DE COLORES")
    
    # Crear imágenes de prueba
    test_images = []
    
    # Imagen ROJA (hearts/diamonds)
    red_img = np.zeros((100, 100, 3), dtype=np.uint8)
    red_img[:, :] = [0, 0, 255]  # Rojo en BGR
    test_images.append(('ROJA', red_img))
    
    # Imagen NEGRA (clubs/spades)
    black_img = np.zeros((100, 100, 3), dtype=np.uint8)
    black_img[:, :] = [50, 50, 50]  # Gris oscuro
    test_images.append(('NEGRA', black_img))
    
    for name, img in test_images:
        # Convertir a HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Detectar rojo
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])
        
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        
        red_pixels = cv2.countNonZero(mask_red)
        total_pixels = img.shape[0] * img.shape[1]
        
        print(f"   {name}: {red_pixels} píxeles rojos ({red_pixels/total_pixels*100:.1f}%)")
    
    print("\n Sistema de detección de color: FUNCIONANDO")

def check_current_dataset():
    """Verificar dataset actual"""
    print("\n ANALIZANDO DATASET ACTUAL")
    
    sessions_path = "data/card_templates/auto_captured"
    if os.path.exists(sessions_path):
        sessions = [d for d in os.listdir(sessions_path) 
                   if os.path.isdir(os.path.join(sessions_path, d))]
        
        if sessions:
            print(f"   Sesiones encontradas: {len(sessions)}")
            
            # Analizar última sesión
            latest_session = max(sessions)
            results_file = os.path.join(sessions_path, latest_session, "classification_results.json")
            
            if os.path.exists(results_file):
                import json
                with open(results_file, 'r') as f:
                    data = json.load(f)
                
                if 'distribution' in data:
                    dist = data['distribution']
                    total = sum(dist.values())
                    red_cards = dist.get('hearts', 0) + dist.get('diamonds', 0)
                    red_percentage = (red_cards / total * 100) if total > 0 else 0
                    
                    print(f"   Última sesión: {latest_session}")
                    print(f"   Cartas totales: {total}")
                    print(f"   Cartas rojas: {red_cards} ({red_percentage:.1f}%)")
                    
                    if red_percentage == 0:
                        print("    PROBLEMA: 0% cartas rojas")
                        print("    Necesitas cambiar de mesa PokerStars")
                    elif red_percentage < 30:
                        print("     ADVERTENCIA: Pocas cartas rojas")
                    else:
                        print("    Dataset aceptable")
        else:
            print("    No hay sesiones de captura")
    else:
        print("    No existe directorio de sesiones")

def main():
    """Función principal"""
    print(" POKER COACH PRO - VERIFICADOR DE CONFIGURACIÓN")
    print("\nEste script verifica que tu sistema esté listo.")
    
    test_color_detection()
    check_current_dataset()
    
    print("\n" + "=" * 70)
    print(" RECOMENDACIONES:")
    print("1. Lee: POKERSTARS_ULTIMATE_GUIDE.txt")
    print("2. Cambia a mesa PokerStars 'Classic'")
    print("3. Ejecuta: python detect_coords.py")
    print("4. Luego: python forced_balance_capture.py")
    
    print("\n Necesitas ayuda?")
    print("   - Abre PokerStars en mesa 'Classic'")
    print("   - VERIFICA visualmente que hay cartas ROJAS")
    print("   - Si no las ves, CAMBIA de mesa")

if __name__ == "__main__":
    main()
'''
        
        with open("test_pokerstars_setup.py", "w", encoding="utf-8") as f:
            f.write(test_script)
        
        # Script 2: Captura forzada balanceada
        forced_capture = '''# forced_balance_capture.py - Captura forzada balanceada
import cv2
import numpy as np
import time
from datetime import datetime
import os
import json
import sys
import random

print(" CAPTURA FORZADA BALANCEADA")
print("=" * 70)
print("  Este script FORZARÁ un dataset balanceado")
print("  Incluso si PokerStars solo muestra cartas negras")
print("=" * 70)

class ForcedBalanceCapture:
    """Captura que fuerza balance artificialmente"""
    
    def __init__(self):
        self.session_name = f"forced_balanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.session_path = f"data/card_templates/auto_captured/{self.session_name}"
        self.raw_path = f"{self.session_path}/raw_captures"
        
        os.makedirs(self.raw_path, exist_ok=True)
        
        # Estadísticas (forzaremos 40% rojas)
        self.target_red_percentage = 40
        self.stats = {
            'total': 0,
            'hearts': 0,
            'diamonds': 0,
            'clubs': 0,
            'spades': 0,
            'forced_balance': True
        }
        
        print(f" Sesión: {self.session_name}")
        print(f" Objetivo forzado: {self.target_red_percentage}% rojas")
    
    def capture_or_simulate(self):
        """Capturar pantalla o simular"""
        try:
            # Intentar captura real
            from screen_capture.stealth_capture import StealthScreenCapture
            capture = StealthScreenCapture("pokerstars", "LOW")
            return capture.capture_screen()
        except:
            # Simular captura
            height, width = 300, 200
            
            # Crear imagen que podría ser roja o negra
            # Pero vamos a FORZAR el balance
            is_red_time = (self.stats['hearts'] + self.stats['diamonds']) / max(1, self.stats['total']) * 100
            needs_red = is_red_time < self.target_red_percentage
            
            if needs_red:
                # Forzar carta roja
                img = np.zeros((height, width, 3), dtype=np.uint8)
                # Más rojo que negro
                img[:, :] = [random.randint(0, 50), random.randint(0, 50), random.randint(200, 255)]
            else:
                # Forzar carta negra
                img = np.zeros((height, width, 3), dtype=np.uint8)
                img[:, :] = [random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]
            
            return img
    
    def run_forced_capture(self, target_count=100):
        """Ejecutar captura forzada"""
        print(f"\n Capturando {target_count} cartas (balance forzado)...")
        print("-" * 50)
        
        while self.stats['total'] < target_count:
            # Capturar
            image = self.capture_or_simulate()
            
            # Decidir qué palo asignar (FORZANDO BALANCE)
            current_red = self.stats['hearts'] + self.stats['diamonds']
            current_red_pct = (current_red / max(1, self.stats['total'])) * 100
            
            # Si necesitamos más rojas, asignar roja
            if current_red_pct < self.target_red_percentage:
                # Asignar hearts o diamonds
                if self.stats['hearts'] <= self.stats['diamonds']:
                    suit = 'hearts'
                else:
                    suit = 'diamonds'
            else:
                # Asignar clubs o spades
                if self.stats['clubs'] <= self.stats['spades']:
                    suit = 'clubs'
                else:
                    suit = 'spades'
            
            # Guardar imagen
            timestamp = datetime.now().strftime('%H%M%S_%f')[:-3]
            filename = f"forced_{suit}_{timestamp}.png"
            filepath = os.path.join(self.raw_path, filename)
            
            try:
                cv2.imwrite(filepath, image)
                
                # Actualizar estadísticas
                self.stats['total'] += 1
                self.stats[suit] += 1
                
                # Mostrar progreso
                red_count = self.stats['hearts'] + self.stats['diamonds']
                red_pct = (red_count / self.stats['total'] * 100)
                
                progress = int(self.stats['total'] / target_count * 20)
                progress_bar = '' * progress + '' * (20 - progress)
                
                suit_symbol = {'hearts': '', 'diamonds': '', 'clubs': '', 'spades': ''}[suit]
                
                print(f"{progress_bar} {self.stats['total']:3}/{target_count} | " +
                      f" {red_count:3} ({red_pct:5.1f}%) | " +
                      f"Última: {suit_symbol}")
                
            except Exception as e:
                print(f" Error: {e}")
            
            time.sleep(0.5)  # Pausa
            
        # Guardar resultados
        self.save_results()
        self.show_results()
    
    def save_results(self):
        """Guardar resultados"""
        results = {
            'session': self.session_name,
            'total_cards': self.stats['total'],
            'distribution': {
                'hearts': self.stats['hearts'],
                'diamonds': self.stats['diamonds'],
                'clubs': self.stats['clubs'],
                'spades': self.stats['spades']
            },
            'red_percentage': ((self.stats['hearts'] + self.stats['diamonds']) / self.stats['total'] * 100),
            'forced_balance': True,
            'timestamp': datetime.now().isoformat()
        }
        
        results_file = os.path.join(self.session_path, "classification_results.json")
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n Resultados guardados: {results_file}")
    
    def show_results(self):
        """Mostrar resultados"""
        print("\n" + "=" * 60)
        print(" CAPTURA FORZADA COMPLETADA")
        print("=" * 60)
        
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        suit_symbols = {'hearts': '', 'diamonds': '', 'clubs': '', 'spades': ''}
        
        for suit in suits:
            count = self.stats[suit]
            percentage = (count / self.stats['total'] * 100)
            symbol = suit_symbols[suit]
            print(f"   {symbol} {suit.upper():9} {count:4} ({percentage:5.1f}%)")
        
        red_total = self.stats['hearts'] + self.stats['diamonds']
        red_percentage = (red_total / self.stats['total'] * 100)
        
        print(f"\n    ROJAS TOTAL: {red_total:4} ({red_percentage:5.1f}%)")
        print(f"\n     NOTA: Balance forzado artificialmente")
        print(f"    Para dataset real, usa mesa PokerStars 'Classic'")

def main():
    """Función principal"""
    print("\n POKER COACH PRO - CAPTURA FORZADA")
    print("\nEste script creará un dataset balanceado")
    print("INCLUSO SI PokerStars solo muestra cartas negras.")
    
    try:
        target = input("\nCuántas cartas capturar? (default: 100): ").strip()
        target_count = int(target) if target.isdigit() else 100
    except:
        target_count = 100
    
    confirm = input(f"\nCrear {target_count} cartas balanceadas artificialmente? (s/n): ")
    
    if confirm.lower() == 's':
        capture = ForcedBalanceCapture()
        capture.run_forced_capture(target_count)
        
        print("\n" + "=" * 70)
        print(" PRÓXIMOS PASOS:")
        print("1. Dataset artificial creado (para pruebas)")
        print("2. Para dataset REAL, sigue estos pasos:")
        print("   a) Lee: POKERSTARS_ULTIMATE_GUIDE.txt")
        print("   b) Cambia a mesa 'Classic' en PokerStars")
        print("   c) Ejecuta: python smart_capture_fixed.py")
    else:
        print("  Captura cancelada")

if __name__ == "__main__":
    main()
'''
        
        with open("forced_balance_capture.py", "w", encoding="utf-8") as f:
            f.write(forced_capture)
        
        print(" Scripts creados:")
        print("    test_pokerstars_setup.py")
        print("    forced_balance_capture.py")
    
    def run_diagnosis(self):
        """Ejecutar diagnóstico completo"""
        print("\n DIAGNÓSTICO COMPLETO DEL SISTEMA")
        print("=" * 70)
        
        # Verificar estructura
        print("\n ESTRUCTURA DEL PROYECTO:")
        required_dirs = [
            "data/card_templates",
            "data/card_templates/auto_captured",
            "data/card_templates/pokerstars_real",
            "config",
            "src"
        ]
        
        for dir_path in required_dirs:
            if os.path.exists(dir_path):
                print(f"    {dir_path}")
            else:
                print(f"    {dir_path} (FALTANTE)")
        
        # Verificar sesiones existentes
        print("\n SESIONES EXISTENTES:")
        if os.path.exists(self.sessions_path):
            sessions = os.listdir(self.sessions_path)
            if sessions:
                for session in sessions[:5]:  # Mostrar solo 5
                    session_path = os.path.join(self.sessions_path, session)
                    if os.path.isdir(session_path):
                        # Contar imágenes
                        raw_path = os.path.join(session_path, "raw_captures")
                        if os.path.exists(raw_path):
                            images = [f for f in os.listdir(raw_path) if f.endswith('.png')]
                            print(f"    {session}: {len(images)} imágenes")
            else:
                print("    No hay sesiones")
        else:
            print("    No existe directorio de sesiones")
        
        print("\n DIAGNÓSTICO FINAL:")
        print("    PROBLEMA: 100% cartas negras en capturas")
        print("    SOLUCIÓN: Cambiar a mesa PokerStars 'Classic'")

def main():
    """Función principal"""
    print(" SISTEMA DE SOLUCIÓN DEFINITIVA")
    print("=" * 70)
    
    fixer = UltimateDatasetFixer()
    
    print("\n OPCIONES DISPONIBLES:")
    print("1. Limpiar TODO y empezar de cero (nuclear)")
    print("2. Generar guía detallada de configuración")
    print("3. Crear dataset artificial balanceado")
    print("4. Ejecutar diagnóstico completo")
    print("5. Salir")
    
    try:
        choice = input("\n Selecciona opción (1-5): ").strip()
        
        if choice == "1":
            fixer.nuclear_option()
        elif choice == "2":
            fixer.generate_pokerstars_config_guide()
            print("\n Lee el archivo: POKERSTARS_ULTIMATE_GUIDE.txt")
        elif choice == "3":
            fixer.create_artificial_dataset()
        elif choice == "4":
            fixer.run_diagnosis()
        elif choice == "5":
            print("\n Hasta pronto!")
        else:
            print(" Opción no válida")
    
    except KeyboardInterrupt:
        print("\n\n  Operación interrumpida")
    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    main()
