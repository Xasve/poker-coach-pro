# verify_balance.py - Verificar balance del dataset (VERSIÓN CORREGIDA)
import os
import json
import sys

def check_dataset_balance():
    """Verificar balance del dataset"""
    print(" VERIFICANDO BALANCE DEL DATASET")
    print("=" * 60)
    
    # Verificar sesiones
    sessions_path = "data/card_templates/auto_captured"
    if not os.path.exists(sessions_path):
        print(" No hay sesiones de captura")
        return False
    
    sessions = [d for d in os.listdir(sessions_path) 
               if os.path.isdir(os.path.join(sessions_path, d))]
    
    if not sessions:
        print(" No hay sesiones")
        return False
    
    print(f" Sesiones encontradas: {len(sessions)}")
    
    # Analizar cada sesión
    all_stats = []
    
    for session in sessions:
        results_file = os.path.join(sessions_path, session, "classification_results.json")
        stats_file = os.path.join(sessions_path, session, "capture_stats.json")
        
        session_stats = {'name': session, 'cards': 0, 'red_percentage': 0}
        
        # Intentar cargar classification_results
        if os.path.exists(results_file):
            try:
                with open(results_file, 'r') as f:
                    data = json.load(f)
                
                if 'distribution' in data:
                    dist = data['distribution']
                    total = sum(dist.values())
                    red_cards = dist.get('hearts', 0) + dist.get('diamonds', 0)
                    red_percentage = (red_cards / total * 100) if total > 0 else 0
                    
                    session_stats['cards'] = total
                    session_stats['red_percentage'] = red_percentage
                    session_stats['distribution'] = dist
            except Exception as e:
                print(f"⚠️  Error leyendo {results_file}: {e}")
        
        # Intentar cargar capture_stats
        elif os.path.exists(stats_file):
            try:
                with open(stats_file, 'r') as f:
                    data = json.load(f)
                
                total = data.get('total', 0)
                red_cards = data.get('hearts', 0) + data.get('diamonds', 0)
                red_percentage = (red_cards / total * 100) if total > 0 else 0
                
                session_stats['cards'] = total
                session_stats['red_percentage'] = red_percentage
            except Exception as e:
                print(f"⚠️  Error leyendo {stats_file}: {e}")
        
        if session_stats['cards'] > 0:
            all_stats.append(session_stats)
    
    # Mostrar resultados
    if not all_stats:
        print(" No hay datos de sesiones")
        return False
    
    print("\n SESIONES ANALIZADAS:")
    print("-" * 50)
    
    total_cards = 0
    total_red = 0
    
    for stats in all_stats:
        red_cards = int(stats['cards'] * stats['red_percentage'] / 100)
        total_cards += stats['cards']
        total_red += red_cards
        
        if stats['red_percentage'] >= 30:
            status = ""
        elif stats['red_percentage'] >= 15:
            status = " "
        else:
            status = "❌"
        
        print(f"{status} {stats['name']:30} {stats['cards']:4} cartas | {stats['red_percentage']:5.1f}% rojas")
    
    # Calcular totales
    if total_cards > 0:
        overall_red_percentage = (total_red / total_cards * 100)
    else:
        overall_red_percentage = 0
    
    print("\n" + "=" * 60)
    print(" ESTADÍSTICAS GLOBALES:")
    print(f"    Total cartas: {total_cards}")
    print(f"    Cartas rojas: {total_red} ({overall_red_percentage:.1f}%)")
    print(f"    Cartas negras: {total_cards - total_red} ({100 - overall_red_percentage:.1f}%)")
    
    # Evaluación
    print("\n EVALUACIÓN:")
    if overall_red_percentage >= 35:
        print("    EXCELENTE: Dataset bien balanceado (>35% rojas)")
    elif overall_red_percentage >= 30:
        print("    BUENO: Dataset aceptable (30-35% rojas)")
    elif overall_red_percentage >= 20:
        print("     REGULAR: Necesitas más cartas rojas (20-30%)")
    elif overall_red_percentage >= 10:
        print("    MALO: Dataset muy desbalanceado (10-20%)")
    else:
        print("    CRÍTICO: Dataset inútil (<10% rojas)")
    
    # Recomendación
    print("\n RECOMENDACIÓN:")
    if overall_red_percentage < 30:
        if total_cards > 0:
            needed_red = int((0.3 * total_cards - total_red) / 0.7)
            print(f"   Captura al menos {max(20, needed_red)} cartas más")
        else:
            print("   Captura al menos 100 cartas")
        print(f"   Usa: python smart_capture_fixed.py")
    else:
        print("   Dataset listo para entrenamiento")
    
    return overall_red_percentage >= 30

def analyze_specific_session(session_name):
    """Analizar sesión específica"""
    print(f"\n ANALIZANDO SESIÓN: {session_name}")
    
    session_path = os.path.join("data/card_templates/auto_captured", session_name)
    if not os.path.exists(session_path):
        print(f" Sesión no encontrada: {session_name}")
        return
    
    results_file = os.path.join(session_path, "classification_results.json")
    if os.path.exists(results_file):
        try:
            with open(results_file, 'r') as f:
                data = json.load(f)
            
            print(f" RESULTADOS:")
            if 'distribution' in data:
                dist = data['distribution']
                total = sum(dist.values())
                
                for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
                    count = dist.get(suit, 0)
                    percentage = (count / total * 100) if total > 0 else 0
                    suit_symbol = {'hearts': '', 'diamonds': '', 'clubs': '', 'spades': ''}[suit]
                    print(f"   {suit_symbol} {suit.upper():9} {count:4} ({percentage:5.1f}%)")
                
                red_total = dist.get('hearts', 0) + dist.get('diamonds', 0)
                red_percentage = (red_total / total * 100) if total > 0 else 0
                
                print(f"\n    ROJAS TOTAL: {red_total} ({red_percentage:.1f}%)")
                
                if red_percentage == 0:
                    print(f"\n    PROBLEMA: 0% cartas rojas")
                    print(f"    Esta sesión es inútil para entrenamiento")
                    print(f"    Posible causa: Mesa PokerStars 'Dark' en lugar de 'Classic'")
        except Exception as e:
            print(f" Error analizando sesión: {e}")
    else:
        print(f" No hay resultados de clasificación para esta sesión")

def list_all_sessions():
    """Listar todas las sesiones"""
    print("\n LISTANDO TODAS LAS SESIONES:")
    print("-" * 50)
    
    sessions_path = "data/card_templates/auto_captured"
    if not os.path.exists(sessions_path):
        print(" No hay directorio de sesiones")
        return []
    
    sessions = [d for d in os.listdir(sessions_path) 
               if os.path.isdir(os.path.join(sessions_path, d))]
    
    if not sessions:
        print(" No hay sesiones")
        return []
    
    sessions.sort(reverse=True)  # Ordenar por fecha (más reciente primero)
    
    for i, session in enumerate(sessions[:10]):  # Mostrar solo 10 más recientes
        print(f"{i+1:2}. {session}")
    
    if len(sessions) > 10:
        print(f"   ... y {len(sessions) - 10} más")
    
    return sessions

def main():
    """Función principal"""
    print(" POKER COACH PRO - VERIFICADOR DE BALANCE")
    print("=" * 70)
    
    # Listar sesiones
    sessions = list_all_sessions()
    
    if sessions:
        print("\n OPCIONES:")
        print("1. Verificar balance general")
        print("2. Analizar sesión específica")
        print("3. Salir")
        
        try:
            choice = input("\n Selecciona opción (1-3): ").strip()
            
            if choice == "1":
                if check_dataset_balance():
                    print("\n El dataset está listo para usar")
                    print(" Ejecuta: python main_integrated.py")
                else:
                    print("\n El dataset necesita más cartas rojas")
                    print(" Ejecuta: python smart_capture_fixed.py")
                    
            elif choice == "2":
                if sessions:
                    print("\n Sesiones disponibles:")
                    for i, session in enumerate(sessions[:5]):
                        print(f"   {i+1}. {session}")
                    
                    session_choice = input("\n Número de sesión a analizar (o nombre completo): ").strip()
                    
                    if session_choice.isdigit():
                        idx = int(session_choice) - 1
                        if 0 <= idx < len(sessions):
                            session_name = sessions[idx]
                        else:
                            print(" Número inválido")
                            return
                    else:
                        session_name = session_choice
                    
                    analyze_specific_session(session_name)
                else:
                    print(" No hay sesiones para analizar")
                    
            elif choice == "3":
                print("\n Hasta pronto!")
            else:
                print(" Opción no válida")
                
        except KeyboardInterrupt:
            print("\n\n  Operación interrumpida")
        except Exception as e:
            print(f" Error: {e}")
    else:
        # No hay sesiones, solo verificar balance general
        check_dataset_balance()

if __name__ == "__main__":
    main()
