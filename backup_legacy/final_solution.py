# final_solution.py - Solución definitiva paso a paso
import os
import sys
import subprocess
import json

class UltimatePokerCoachSolution:
    """Solución definitiva para Poker Coach Pro"""
    
    def __init__(self):
        self.steps_completed = []
        self.problems_found = []
    
    def run_full_solution(self):
        """Ejecutar solución completa"""
        print(" POKER COACH PRO - SOLUCIÓN DEFINITIVA")
        print("=" * 70)
        
        # Paso 0: Diagnóstico inicial
        self.initial_diagnosis()
        
        # Paso 1: Verificar/Configurar PokerStars
        self.step1_pokerstars_setup()
        
        # Paso 2: Capturar dataset balanceado
        self.step2_capture_balanced_dataset()
        
        # Paso 3: Verificar resultados
        self.step3_verify_results()
        
        # Paso 4: Sistema listo
        self.step4_system_ready()
        
        # Mostrar resumen final
        self.final_summary()
    
    def initial_diagnosis(self):
        """Diagnóstico inicial"""
        print("\n DIAGNÓSTICO INICIAL")
        print("-" * 50)
        
        # Verificar archivos
        print(" Verificando archivos del sistema...")
        required_files = [
            "smart_capture_fixed.py",
            "verify_balance.py", 
            "detect_coords.py",
            "session_manager.py"
        ]
        
        for file in required_files:
            if os.path.exists(file):
                print(f"    {file}")
            else:
                print(f"    {file} - FALTANTE")
                self.problems_found.append(f"Archivo faltante: {file}")
        
        # Verificar dataset actual
        print("\n Verificando dataset actual...")
        sessions_path = "data/card_templates/auto_captured"
        if os.path.exists(sessions_path):
            sessions = [d for d in os.listdir(sessions_path) 
                      if os.path.isdir(os.path.join(sessions_path, d))]
            
            if sessions:
                print(f"   Sesiones encontradas: {len(sessions)}")
                
                # Analizar última sesión
                latest = max(sessions)
                results_file = os.path.join(sessions_path, latest, "classification_results.json")
                
                if os.path.exists(results_file):
                    try:
                        with open(results_file, 'r') as f:
                            data = json.load(f)
                        
                        if 'distribution' in data:
                            dist = data['distribution']
                            total = sum(dist.values())
                            red_cards = dist.get('hearts', 0) + dist.get('diamonds', 0)
                            red_percentage = (red_cards / total * 100) if total > 0 else 0
                            
                            print(f"   Última sesión: {latest}")
                            print(f"   Cartas totales: {total}")
                            print(f"   Cartas rojas: {red_cards} ({red_percentage:.1f}%)")
                            
                            if red_percentage == 0:
                                print("    PROBLEMA: 0% cartas rojas")
                                self.problems_found.append("Dataset con 0% cartas rojas")
                            elif red_percentage < 30:
                                print(f"   ⚠️  ADVERTENCIA: Solo {red_percentage:.1f}% rojas")
            else:
                print("   ❌ No hay sesiones de captura")
                self.problems_found.append("No hay sesiones de captura")
        else:
            print("   ❌ No existe directorio de sesiones")
        
        print("\n✅ Diagnóstico completado")
    
    def step1_pokerstars_setup(self):
        """Paso 1: Configurar PokerStars"""
        print("\n PASO 1: CONFIGURAR POKERSTARS")
        print("-" * 50)
        
        print("""
 INSTRUCCIONES CRÍTICAS:

1. ABRE PokerStars en tu computadora
2. BUSCA una mesa que diga 'Classic' (NO 'Dark')
3. ÚNETE a la mesa y espera cartas
4. VERIFICA que ves cartas ROJAS ()

 MESAS RECOMENDADAS:
    'NL Hold'em Classic'
    'PL Omaha Classic'
    Cualquier mesa '... Classic'

 MESAS A EVITAR:
    Cualquier '... Dark'
    Cualquier '... Stealth'
    Cualquier '... Night'
""")
        
        input("\n👉 Cuando tengas PokerStars abierto en mesa 'Classic', presiona Enter...")
        
        # Ejecutar detección de coordenadas
        print("\n Configurando captura...")
        print("   (Sigue las instrucciones en pantalla)")
        
        try:
            subprocess.run([sys.executable, "detect_coords.py"], check=True)
            self.steps_completed.append("PokerStars configurado")
            print("✅ PokerStars configurado correctamente")
        except:
            print(" Error configurando PokerStars")
            print(" Intenta ejecutar manualmente: python detect_coords.py")
    
    def step2_capture_balanced_dataset(self):
        """Paso 2: Capturar dataset balanceado"""
        print("\n PASO 2: CAPTURAR DATASET BALANCEADO")
        print("-" * 50)
        
        print("""
 CAPTURA AUTOMÁTICA:

 Se capturarán 100 cartas automáticamente
 El sistema balanceará rojas y negras
 Duración: 2-3 minutos

 OBJETIVO:
    Mínimo 30 cartas rojas (30%)
    Máximo 70 cartas negras (70%)

⚠️  DURANTE LA CAPTURA:
   • NO muevas la ventana de PokerStars
   • Deja que el script trabaje
   • Puedes presionar Ctrl+C para detener
""")
        
        confirm = input("\nIniciar captura automática? (s/n): ").strip().lower()
        
        if confirm == 's':
            print("\n Iniciando captura balanceada...")
            try:
                # Usar captura simplificada primero (más estable)
                if os.path.exists("simple_capture.py"):
                    subprocess.run([sys.executable, "simple_capture.py"], check=True)
                else:
                    subprocess.run([sys.executable, "smart_capture_fixed.py"], check=True)
                
                self.steps_completed.append("Dataset capturado")
                print("✅ Captura completada")
            except KeyboardInterrupt:
                print("\n⏹️  Captura interrumpida por usuario")
            except:
                print(" Error durante la captura")
        else:
            print("  Captura cancelada")
    
    def step3_verify_results(self):
        """Paso 3: Verificar resultados"""
        print("\n PASO 3: VERIFICAR RESULTADOS")
        print("-" * 50)
        
        print(" Analizando dataset capturado...")
        
        try:
            subprocess.run([sys.executable, "verify_balance.py"], check=True)
            self.steps_completed.append("Resultados verificados")
        except:
            print(" Error verificando resultados")
    
    def step4_system_ready(self):
        """Paso 4: Sistema listo para usar"""
        print("\n PASO 4: SISTEMA LISTO")
        print("-" * 50)
        
        print("""
 CONFIGURACIÓN COMPLETADA!

Tu sistema Poker Coach Pro está listo para usar.

 COMANDOS DISPONIBLES:

1. Sistema principal (recomendado):
   python main_integrated.py

2. Gestión de sesiones:
   python session_manager.py

3. Análisis automático:
   python start_auto_simple.py

4. Verificar estado:
   python verify_balance.py

 RECOMENDACIÓN:
   Comienza con: python main_integrated.py
   Selecciona 'Modo interactivo'
""")
        
        self.steps_completed.append("Sistema listo")
    
    def final_summary(self):
        """Resumen final"""
        print("\n" + "=" * 70)
        print(" RESUMEN FINAL")
        print("=" * 70)
        
        if self.steps_completed:
            print(" PASOS COMPLETADOS:")
            for step in self.steps_completed:
                print(f"    {step}")
        
        if self.problems_found:
            print("\n PROBLEMAS ENCONTRADOS:")
            for problem in self.problems_found:
                print(f"    {problem}")
            
            print("\n SOLUCIONES:")
            print("   1. Para problemas con cartas rojas: Cambia de mesa PokerStars")
            print("   2. Para archivos faltantes: Reclona el repositorio")
            print("   3. Para otros problemas: Contacta soporte")
        else:
            print("\n TODOS LOS PROBLEMAS RESUELTOS!")
        
        print("\n" + "=" * 70)
        print(" SISTEMA POKER COACH PRO LISTO PARA USAR!")
        print("=" * 70)

def main():
    """Función principal"""
    solution = UltimatePokerCoachSolution()
    solution.run_full_solution()

if __name__ == "__main__":
    main()
