# verify_balance.py - Verificar balance del dataset
import os
import json

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
            except:
                pass
        
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
            except:
                pass
        
        if session_stats['cards'] > 0:
            all_stats.append(session_stats)
    
    # Mostrar resultados
    if not all_stats:
        print(" No hay datos de sesiones")
        return False
    
    print("
 SESIONES ANALIZADAS:")
    print("-" * 50)
    
    total_cards = 0
    total_red = 0
    
    for stats in all_stats:
        red_cards = int(stats['cards'] * stats['red_percentage'] / 100)
        total_cards += stats['cards']
        total_red += red_cards
        
        status = "" if stats['red_percentage'] >= 30 else " " if stats['red_percentage'] >= 15 else ""
        
        print(f"{status} {stats['name']:30} {stats['cards']:4} cartas | "
              f"{stats['red_percentage']:5.1f}% rojas")
    
    # Calcular totales
    overall_red_percentage = (total_red / total_cards * 100) if total_cards > 0 else 0
    
    print("
" + "=" * 60)
    print(" ESTADÍSTICAS GLOBALES:")
    print(f"    Total cartas: {total_cards}")
    print(f"    Cartas rojas: {total_red} ({overall_red_percentage:.1f}%)")
    print(f"    Cartas negras: {total_cards - total_red} ({100-overall_red_percentage:.1f}%)")
    
    # Evaluación
    print("
 EVALUACIÓN:")
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
    print("
 RECOMENDACIÓN:")
    if overall_red_percentage < 30:
        needed_red = int((0.3 * total_cards - total_red) / 0.7)
        print(f"   Captura al menos {max(20, needed_red)} cartas más")
        print(f"   Usa: python smart_capture_fixed.py")
    else:
        print("   Dataset listo para entrenamiento")
    
    return overall_red_percentage >= 30

def main():
    """Función principal"""
    if check_dataset_balance():
        print("
 El dataset está listo para usar")
        print(" Ejecuta: python main_integrated.py")
    else:
        print("
 El dataset necesita más cartas rojas")
        print(" Ejecuta: python smart_capture_fixed.py")

if __name__ == "__main__":
    main()
