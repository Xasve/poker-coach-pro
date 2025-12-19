# simple_capture.py - Captura simplificada sin errores
import cv2
import numpy as np
import os
import time
from datetime import datetime

def create_simple_capture():
    """Crear captura simplificada y segura"""
    print(" CAPTURA SIMPLIFICADA - SIN ERRORES")
    print("=" * 60)
    
    # Crear directorio de sesión
    session_name = f"simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    session_path = f"data/card_templates/auto_captured/{session_name}"
    raw_path = f"{session_path}/raw_captures"
    
    os.makedirs(raw_path, exist_ok=True)
    
    print(f"📁 Sesión: {session_name}")
    print(f"📂 Guardando en: {raw_path}")
    
    # Estadísticas
    stats = {
        'total': 0,
        'hearts': 0,
        'diamonds': 0, 
        'clubs': 0,
        'spades': 0
    }
    
    # Capturar N cartas
    target_count = 50
    
    print(f"\n Capturando {target_count} cartas...")
    print("Presiona Ctrl+C para detener")
    print("-" * 50)
    
    try:
        for i in range(target_count):
            # Crear imagen artificial (para pruebas)
            height, width = 100, 70
            
            # Alternar entre rojas y negras para balance
            if i % 3 == 0:  # 33% rojas, 66% negras
                # Carta roja (hearts o diamonds)
                if stats['hearts'] <= stats['diamonds']:
                    suit = 'hearts'
                    color = [0, 0, 200]  # Rojo
                else:
                    suit = 'diamonds'
                    color = [0, 0, 200]  # Rojo
            else:
                # Carta negra (clubs o spades)
                if stats['clubs'] <= stats['spades']:
                    suit = 'clubs'
                    color = [50, 50, 50]  # Negro
                else:
                    suit = 'spades'
                    color = [50, 50, 50]  # Negro
            
            # Crear imagen
            img = np.zeros((height, width, 3), dtype=np.uint8)
            img[:, :] = color
            
            # Añadir texto simple
            suit_text = suit[0].upper()
            cv2.putText(img, suit_text, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 
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
            red_percentage = (red_count / stats['total'] * 100)
            
            progress = int((i + 1) / target_count * 20)
            progress_bar = '█' * progress + '░' * (20 - progress)
            
            suit_symbol = {'hearts': '♥️', 'diamonds': '♦️', 'clubs': '♣️', 'spades': '♠️'}[suit]
            
            print(f"{progress_bar} {i+1:3}/{target_count} | " +
                  f"🔴 {red_count:3} ({red_percentage:5.1f}%) | " +
                  f"Última: {suit_symbol}")
            
            time.sleep(0.1)  # Pequeña pausa
            
        print("\n" + "=" * 60)
        print("✅ CAPTURA COMPLETADA")
        
        # Mostrar estadísticas finales
        print("\n📊 ESTADÍSTICAS FINALES:")
        for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
            count = stats[suit]
            percentage = (count / stats['total'] * 100)
            symbol = {'hearts': '♥️', 'diamonds': '♦️', 'clubs': '♣️', 'spades': '♠️'}[suit]
            print(f"   {symbol} {suit.upper():9} {count:3} ({percentage:5.1f}%)")
        
        red_total = stats['hearts'] + stats['diamonds']
        red_percentage = (red_total / stats['total'] * 100)
        
        print(f"\n   🔴 ROJAS TOTAL: {red_total} ({red_percentage:.1f}%)")
        
        if red_percentage >= 30:
            print(f"\n   ✅ Dataset balanceado correctamente")
        else:
            print(f"\n   ⚠️  Necesitas más cartas rojas")
        
        # Guardar resultados
        import json
        results = {
            'session': session_name,
            'total_cards': stats['total'],
            'distribution': {
                'hearts': stats['hearts'],
                'diamonds': stats['diamonds'],
                'clubs': stats['clubs'],
                'spades': stats['spades']
            },
            'red_percentage': red_percentage,
            'simple_capture': True,
            'timestamp': datetime.now().isoformat()
        }
        
        results_file = os.path.join(session_path, "classification_results.json")
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📊 Resultados guardados: {results_file}")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Captura interrumpida por usuario")
    
    print("\n🎯 Para clasificar estas cartas:")
    print("   Ejecuta: python session_manager.py")
    print("   Selecciona opción 2")

if __name__ == "__main__":
    create_simple_capture()
