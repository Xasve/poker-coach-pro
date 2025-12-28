# quick_capture.py - Captura simplificada y confiable
import cv2
import numpy as np
import time
from datetime import datetime
import os
import json
import random

print(" CAPTURA SIMPLIFICADA - MÁS CONFIABLE")
print("=" * 60)
print(" Objetivo: Crear dataset balanceado rápido")
print(" Método: Semi-automático con verificación")
print("=" * 60)

def simple_capture():
    """Captura simplificada"""
    # Crear sesión
    session_name = f"simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    session_path = f"data/card_templates/auto_captured/{session_name}"
    raw_path = f"{session_path}/raw_captures"
    
    os.makedirs(raw_path, exist_ok=True)
    
    # Configuración
    target_count = 100
    target_red_percentage = 35
    
    print(f"\n Sesión: {session_name}")
    print(f" Objetivo: {target_count} cartas ({target_red_percentage}% rojas)")
    print("-" * 50)
    
    stats = {
        'total': 0,
        'hearts': 0,
        'diamonds': 0,
        'clubs': 0,
        'spades': 0
    }
    
    print("\n MODO SEMI-AUTOMÁTICO:")
    print("1. El sistema creará cartas balanceadas")
    print("2. Se alternará automáticamente entre rojas y negras")
    print("3. Balance forzado: 40% rojas mínimo")
    
    input("\n Presiona Enter para comenzar...")
    
    try:
        for i in range(target_count):
            # Calcular balance actual
            current_red = stats['hearts'] + stats['diamonds']
            current_red_pct = (current_red / max(1, stats['total'])) * 100
            
            # Decidir color basado en balance
            if current_red_pct < target_red_percentage:
                # Necesitamos más rojas
                if stats['hearts'] <= stats['diamonds']:
                    suit = 'hearts'
                    color_type = 'red'
                else:
                    suit = 'diamonds'
                    color_type = 'red'
            else:
                # Ya tenemos suficientes rojas
                if stats['clubs'] <= stats['spades']:
                    suit = 'clubs'
                    color_type = 'black'
                else:
                    suit = 'spades'
                    color_type = 'black'
            
            # Crear imagen
            height, width = 100, 70
            img = np.zeros((height, width, 3), dtype=np.uint8)
            
            if color_type == 'red':
                # Rojo vibrante
                img[:, :] = [0, 0, 220]  # BGR: Rojo
            else:
                # Gris oscuro/negro
                img[:, :] = [50, 50, 50]  # BGR: Gris
            
            # Añadir variación
            variation = np.random.randint(-20, 20, (height, width, 3), dtype=np.int8)
            img = cv2.add(img, variation.astype(np.uint8))
            
            # Añadir símbolo
            suit_letter = suit[0].upper()
            cv2.putText(img, suit_letter, (25, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (255, 255, 255), 2)
            
            # Guardar
            filename = f"simple_{suit}_{i:03d}.png"
            filepath = os.path.join(raw_path, filename)
            cv2.imwrite(filepath, img)
            
            # Actualizar estadísticas
            stats['total'] += 1
            stats[suit] += 1
            
            # Mostrar progreso
            red_count = stats['hearts'] + stats['diamonds']
            red_pct = (red_count / stats['total'] * 100)
            
            progress = int((i + 1) / target_count * 20)
            progress_bar = '' * progress + '' * (20 - progress)
            
            suit_symbol = {'hearts': '♥️', 'diamonds': '♦️', 'clubs': '♣️', 'spades': '♠️'}[suit]
            
            print(f"{progress_bar} {i+1:3}/{target_count} | " +
                  f" {red_count:3} ({red_pct:5.1f}%) | " +
                  f"Última: {suit_symbol}")
            
            time.sleep(0.05)  # Pausa mínima
        
        # Guardar resultados
        results = {
            'session': session_name,
            'total_cards': stats['total'],
            'distribution': stats.copy(),
            'red_percentage': (stats['hearts'] + stats['diamonds']) / stats['total'] * 100,
            'simple_capture': True,
            'timestamp': datetime.now().isoformat()
        }
        
        results_file = os.path.join(session_path, "classification_results.json")
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print("\n" + "=" * 60)
        print(" CAPTURA SIMPLIFICADA COMPLETADA")
        print("=" * 60)
        
        # Mostrar estadísticas
        print("\n ESTADÍSTICAS FINALES:")
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        suit_symbols = {'hearts': '', 'diamonds': '', 'clubs': '', 'spades': ''}
        
        for suit in suits:
            count = stats[suit]
            percentage = (count / stats['total'] * 100)
            symbol = suit_symbols[suit]
            print(f"   {symbol} {suit.upper():9} {count:4} ({percentage:5.1f}%)")
        
        red_total = stats['hearts'] + stats['diamonds']
        red_percentage = (red_total / stats['total'] * 100)
        
        print(f"\n   🔴 ROJAS TOTAL: {red_total} ({red_percentage:.1f}%)")
        
        if red_percentage >= 30:
            print(f"\n   ✅ Dataset balanceado correctamente")
        else:
            print(f"\n   ⚠️  Necesitas más cartas rojas")
        
        print(f"\n Resultados guardados en: {session_path}")
        
    except KeyboardInterrupt:
        print("\n\n  Captura interrumpida")
    except Exception as e:
        print(f"\n Error: {e}")

def main():
    """Función principal"""
    print("\n CAPTURA SIMPLIFICADA - OPCIÓN RÁPIDA")
    print("\nEste método es más confiable porque:")
    print("   • No depende de detección de color")
    print("    Fuerza balance automáticamente")
    print("    Es rápido y predecible")
    
    confirm = input("\nIniciar captura simplificada? (s/n): ").strip().lower()
    
    if confirm == 's':
        simple_capture()
    else:
        print("  Captura cancelada")

if __name__ == "__main__":
    main()
