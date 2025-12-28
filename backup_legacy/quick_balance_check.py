# quick_balance_check.py - Verificación rápida del balance
import os
import json

print("⚡ VERIFICACIÓN RÁPIDA DE BALANCE")
print("=" * 50)

sessions_path = "data/card_templates/auto_captured"
if not os.path.exists(sessions_path):
    print(" No hay sesiones de captura")
    exit(1)

sessions = [d for d in os.listdir(sessions_path) 
           if os.path.isdir(os.path.join(sessions_path, d))]

if not sessions:
    print(" No hay sesiones")
    exit(1)

print(f" Sesiones encontradas: {len(sessions)}")

# Analizar la sesión más reciente
latest_session = max(sessions)
print(f"\n🔍 Analizando sesión más reciente: {latest_session}")

results_file = os.path.join(sessions_path, latest_session, "classification_results.json")
if os.path.exists(results_file):
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
        
        if 'distribution' in data:
            dist = data['distribution']
            total = sum(dist.values())
            
            print("\n📊 DISTRIBUCIÓN:")
            suits = ['hearts', 'diamonds', 'clubs', 'spades']
            suit_symbols = {'hearts': '', 'diamonds': '', 'clubs': '', 'spades': ''}
            
            for suit in suits:
                count = dist.get(suit, 0)
                percentage = (count / total * 100) if total > 0 else 0
                symbol = suit_symbols[suit]
                print(f"   {symbol} {suit.upper():9} {count:4} ({percentage:5.1f}%)")
            
            red_total = dist.get('hearts', 0) + dist.get('diamonds', 0)
            red_percentage = (red_total / total * 100) if total > 0 else 0
            
            print(f"\n RESUMEN:")
            print(f"    Cartas rojas: {red_total} ({red_percentage:.1f}%)")
            print(f"    Cartas negras: {total - red_total} ({100 - red_percentage:.1f}%)")
            
            if red_percentage == 0:
                print("\n PROBLEMA CRÍTICO: 0% cartas rojas")
                print(" Estás capturando en mesa PokerStars incorrecta")
                print(" Cambia a mesa 'Classic' (no 'Dark')")
            elif red_percentage < 30:
                print(f"\n⚠️  ADVERTENCIA: Solo {red_percentage:.1f}% cartas rojas")
                print("💡 Necesitas al menos 30% para buen entrenamiento")
            else:
                print(f"\n✅ EXCELENTE: {red_percentage:.1f}% cartas rojas")
                print("💡 Dataset bien balanceado")
        else:
            print("❌ No hay datos de distribución")
    except Exception as e:
        print(f"❌ Error leyendo archivo: {e}")
else:
    print("❌ No hay resultados de clasificación")

print("\n" + "=" * 50)
print(" RECOMENDACIÓN:")
if os.path.exists("smart_capture_fixed.py"):
    print("   Ejecuta: python smart_capture_fixed.py")
else:
    print("   Configura PokerStars y captura más cartas")
