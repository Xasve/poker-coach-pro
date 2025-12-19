# run_poker_coach_simple.py
import sys
import os
import time

def main():
    print("🎴 POKER COACH PRO - EJECUCIÓN SIMPLIFICADA")
    print("=" * 60)
    
    # Añadir src al path
    sys.path.insert(0, 'src')
    
    try:
        # Importar componentes
        from platforms.pokerstars_adapter import PokerStarsAdapter
        from core.poker_engine import PokerEngine
        
        print("1. INICIALIZANDO COMPONENTES...")
        
        # Crear adaptador
        adapter = PokerStarsAdapter(stealth_level="LOW")
        print("   ✅ Adaptador PokerStars creado")
        
        # Crear motor GTO
        engine = PokerEngine()
        print("   ✅ Motor GTO creado")
        
        print("\n2. INICIANDO SISTEMA...")
        print("   Presiona Ctrl+C para detener")
        print("=" * 60)
        
        # Iniciar captura
        adapter.start()
        
        iteration = 0
        try:
            while True:
                iteration += 1
                print(f"\n🔄 Iteración {iteration}")
                
                # Obtener estado de la mesa
                table_state = adapter.get_table_state()
                
                if table_state:
                    print(f"   📊 Mesa detectada")
                    
                    # Mostrar información básica
                    if 'simulated' in table_state:
                        print(f"   ⚠️  MODO SIMULADO - PokerStars no detectado")
                    
                    if 'cards' in table_state:
                        cards = table_state['cards']
                        print(f"   🃏 Cartas: {cards}")
                    
                    if 'pot' in table_state:
                        print(f"   💰 Pozo: {table_state['pot']}")
                    
                    # Analizar con motor GTO
                    if table_state.get('cards'):
                        decision = engine.analyze_hand(
                            hole_cards=table_state['cards'].get('hero', []),
                            community_cards=table_state['cards'].get('community', []),
                            pot_size=int(table_state.get('pot', 0)) if str(table_state.get('pot', '0')).isdigit() else 0,
                            position=table_state.get('position', 'middle')
                        )
                        
                        print(f"\n   🎯 RECOMENDACIÓN GTO:")
                        print(f"      Acción: {decision.get('action', 'CHECK')}")
                        print(f"      Confianza: {decision.get('confidence', 0):.1%}")
                        print(f"      Razón: {decision.get('reason', 'Sin datos suficientes')}")
                    
                else:
                    print(f"   ⏳ Esperando mesa de poker...")
                
                # Esperar antes de siguiente iteración
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Deteniendo por usuario...")
        
        finally:
            print("\n3. LIMPIANDO...")
            adapter.stop()
            print("✅ Sistema detenido correctamente")
            
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("🎴 POKER COACH PRO FINALIZADO")

if __name__ == "__main__":
    main()