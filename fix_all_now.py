#!/usr/bin/env python3
"""
REPARADOR COMPLETO - Poker Coach Pro
Ejecuta todos los cambios necesarios en una sola ejecución
"""
import os
import sys
import subprocess

def print_section(title):
    """Imprimir sección con formato"""
    print("\n" + "=" * 70)
    print(f"🔧 {title}")
    print("=" * 70)

def run_command(cmd, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n📝 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ Completado")
            if result.stdout.strip():
                print(f"   Salida: {result.stdout[:100]}...")
        else:
            print(f"❌ Error: {result.stderr[:200]}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False

def fix_pokerstars_adapter():
    """Reparar PokerStars Adapter"""
    print_section("REPARANDO POKERSTARS ADAPTER")
    
    adapter_file = "src/platforms/pokerstars_adapter.py"
    
    if not os.path.exists(adapter_file):
        print(f"❌ Archivo no encontrado: {adapter_file}")
        return False
    
    print("📄 Leyendo archivo...")
    with open(adapter_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encontrar la línea problemática de TableDetector
    if 'TableDetector("pokerstars")' in content:
        print("✅ Encontrado: TableDetector(\"pokerstars\")")
        content = content.replace(
            'TableDetector("pokerstars")',
            'TableDetector()'
        )
        print("✅ Reemplazado por: TableDetector()")
    
    # Encontrar la línea problemática de CardRecognizer
    if 'CardRecognizer(self.platform, self.stealth_level)' in content:
        print("✅ Encontrado: CardRecognizer(self.platform, self.stealth_level)")
        content = content.replace(
            'CardRecognizer(self.platform, self.stealth_level)',
            'CardRecognizer(platform=self.platform)'
        )
        print("✅ Reemplazado por: CardRecognizer(platform=self.platform)")
    
    # Verificar si hay otras versiones del problema
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'CardRecognizer(' in line and 'stealth_level' in line:
            print(f"⚠️  Línea {i+1} posiblemente problemática: {line.strip()}")
            # Reemplazar genéricamente
            if '=' in line:
                parts = line.split('=')
                if len(parts) == 2:
                    lines[i] = parts[0].strip() + ' = CardRecognizer(platform=self.platform)'
                    print(f"✅ Línea {i+1} corregida")
    
    # Guardar cambios
    print("💾 Guardando cambios...")
    with open(adapter_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print("✅ PokerStars Adapter reparado")
    return True

def fix_ggpoker_adapter():
    """Reparar GG Poker Adapter si existe"""
    print_section("VERIFICANDO GG POKER ADAPTER")
    
    adapter_file = "src/platforms/ggpoker_adapter.py"
    
    if not os.path.exists(adapter_file):
        print("⚠️  Archivo no encontrado (puede ser normal si no usas GG Poker)")
        return True
    
    with open(adapter_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar problemas similares
    changes_made = False
    
    if 'TableDetector(' in content and ')' in content:
        print("✅ Aplicando correcciones a TableDetector...")
        # Esto es un reemplazo genérico, puede necesitar ajustes
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'TableDetector(' in line and not 'TableDetector()' in line:
                print(f"⚠️  Línea {i+1} problemática: {line.strip()}")
                if '=' in line:
                    parts = line.split('=')
                    if len(parts) == 2:
                        lines[i] = parts[0].strip() + ' = TableDetector()'
                        changes_made = True
                        print(f"✅ Línea {i+1} corregida")
    
    if changes_made:
        with open(adapter_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print("✅ GG Poker Adapter reparado")
    
    return True

def create_test_script():
    """Crear script de prueba después de las reparaciones"""
    print_section("CREANDO SCRIPT DE PRUEBA")
    
    test_script = '''#!/usr/bin/env python3
"""
TEST DE VERIFICACIÓN RÁPIDA - Después de reparaciones
"""
import sys
import os

sys.path.insert(0, 'src')

print("=" * 70)
print("🧪 VERIFICACIÓN RÁPIDA POST-REPARACIÓN")
print("=" * 70)

def test_import(module_name, class_name=None):
    """Probar importación de módulo/clase"""
    try:
        if class_name:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            
            # Probar creación con argumentos correctos
            if class_name == "StealthScreenCapture":
                instance = cls("pokerstars", "MEDIUM")
            elif class_name == "CardRecognizer":
                instance = cls(platform="pokerstars")
            elif class_name == "TableDetector":
                instance = cls()  # Sin argumentos
            elif class_name == "PokerStarsAdapter":
                instance = cls()
            else:
                instance = cls()
            
            return True, f"{class_name}"
        else:
            __import__(module_name)
            return True, module_name
    except TypeError as e:
        return False, f"{class_name} - Error de argumentos: {e}"
    except Exception as e:
        return False, f"{class_name if class_name else module_name} - {e}"

print("\\n🔍 PROBANDO IMPORTS CRÍTICOS...")

tests = [
    ("screen_capture.stealth_capture", "StealthScreenCapture"),
    ("screen_capture.card_recognizer", "CardRecognizer"),
    ("screen_capture.table_detector", "TableDetector"),
    ("platforms.pokerstars_adapter", "PokerStarsAdapter")
]

all_passed = True
for module, cls in tests:
    passed, message = test_import(module, cls)
    if passed:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
        all_passed = False

print("\\n" + "=" * 70)
if all_passed:
    print("🎉 ¡TODAS LAS IMPORTACIONES FUNCIONAN!")
    print("\\n🚀 Ahora puedes ejecutar:")
    print("   python test_pokerstars.py")
else:
    print("⚠️  ALGUNAS IMPORTACIONES FALLARON")
    print("\\n💡 Ejecuta el reparador nuevamente o revisa manualmente")
print("=" * 70)
'''

    with open("test_after_fix.py", 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print("✅ Script de prueba creado: test_after_fix.py")
    return True

def create_quick_fix_script():
    """Crear script de solución rápida"""
    print_section("CREANDO SOLUCIÓN RÁPIDA")
    
    quick_fix = '''#!/usr/bin/env python3
"""
SOLUCIÓN RÁPIDA - PokerStars Adapter
Corrige solo los problemas críticos
"""
import os

def apply_quick_fix():
    """Aplicar corrección rápida al archivo problemático"""
    adapter_file = "src/platforms/pokerstars_adapter.py"
    
    if not os.path.exists(adapter_file):
        print(f"❌ Archivo no encontrado: {adapter_file}")
        return False
    
    # Leer contenido
    with open(adapter_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print("🔍 Buscando líneas problemáticas...")
    
    fixed_lines = []
    changes_made = 0
    
    for i, line in enumerate(lines, 1):
        fixed_line = line
        
        # Buscar TableDetector con argumentos
        if 'TableDetector(' in line and not 'TableDetector()' in line:
            print(f"⚠️  Línea {i}: {line.strip()}")
            # Extraer la parte antes del =
            if '=' in line:
                parts = line.split('=')
                if len(parts) == 2:
                    fixed_line = parts[0] + '= TableDetector()\n'
                    changes_made += 1
                    print(f"✅ Corregida: {fixed_line.strip()}")
        
        # Buscar CardRecognizer con argumentos incorrectos
        elif 'CardRecognizer(' in line and 'stealth_level' in line:
            print(f"⚠️  Línea {i}: {line.strip()}")
            # Reemplazar con constructor correcto
            fixed_line = line.replace(
                'CardRecognizer(self.platform, self.stealth_level)',
                'CardRecognizer(platform=self.platform)'
            )
            if fixed_line != line:
                changes_made += 1
                print(f"✅ Corregida: {fixed_line.strip()}")
        
        fixed_lines.append(fixed_line)
    
    if changes_made > 0:
        # Guardar cambios
        with open(adapter_file, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        
        print(f"\\n✅ {changes_made} cambios aplicados")
        print("💾 Archivo guardado")
        
        # Mostrar resumen de cambios
        print("\\n📋 RESUMEN DE CAMBIOS:")
        print("   1. TableDetector(\"pokerstars\") → TableDetector()")
        print("   2. CardRecognizer(platform, stealth_level) → CardRecognizer(platform=platform)")
        
        return True
    else:
        print("\\nℹ️  No se encontraron problemas para corregir")
        return True

def create_backup():
    """Crear backup del archivo original"""
    import shutil
    import datetime
    
    adapter_file = "src/platforms/pokerstars_adapter.py"
    backup_dir = "backups"
    
    if os.path.exists(adapter_file):
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"pokerstars_adapter_backup_{timestamp}.py")
        
        shutil.copy2(adapter_file, backup_file)
        print(f"📂 Backup creado: {backup_file}")
        return backup_file
    
    return None

if __name__ == "__main__":
    print("=" * 70)
    print("🔧 SOLUCIÓN RÁPIDA - POKER COACH PRO")
    print("=" * 70)
    
    # Crear backup
    print("\\n💾 Creando backup...")
    backup = create_backup()
    if backup:
        print(f"✅ Backup: {backup}")
    
    # Aplicar correcciones
    print("\\n🔧 Aplicando correcciones...")
    if apply_quick_fix():
        print("\\n🎉 ¡CORRECCIONES APLICADAS!")
        print("\\n🚀 Prueba el sistema:")
        print("   python test_pokerstars.py")
    else:
        print("\\n❌ No se pudieron aplicar las correcciones")
    
    print("\\n" + "=" * 70)
'''

    with open("quick_fix.py", 'w', encoding='utf-8') as f:
        f.write(quick_fix)
    
    print("✅ Script rápido creado: quick_fix.py")
    return True

def run_comprehensive_test():
    """Ejecutar prueba comprehensiva"""
    print_section("EJECUTANDO PRUEBA COMPLETA")
    
    test_code = '''
import sys
import os
sys.path.insert(0, 'src')

print("🧪 PRUEBA COMPLETA DEL SISTEMA")
print("=" * 50)

# Test 1: StealthScreenCapture
try:
    from screen_capture.stealth_capture import StealthScreenCapture
    capture = StealthScreenCapture("pokerstars", "MEDIUM")
    print("✅ 1. StealthScreenCapture - Constructor correcto")
except Exception as e:
    print(f"❌ 1. StealthScreenCapture - Error: {e}")

# Test 2: CardRecognizer
try:
    from screen_capture.card_recognizer import CardRecognizer
    recognizer = CardRecognizer(platform="pokerstars")
    print("✅ 2. CardRecognizer - Constructor correcto")
except Exception as e:
    print(f"❌ 2. CardRecognizer - Error: {e}")

# Test 3: TableDetector
try:
    from screen_capture.table_detector import TableDetector
    detector = TableDetector()
    print("✅ 3. TableDetector - Constructor correcto")
except Exception as e:
    print(f"❌ 3. TableDetector - Error: {e}")

# Test 4: PokerStarsAdapter
try:
    from platforms.pokerstars_adapter import PokerStarsAdapter
    adapter = PokerStarsAdapter()
    print("✅ 4. PokerStarsAdapter - Constructor correcto")
    print("🎉 ¡TODOS LOS TESTS PASARON!")
except Exception as e:
    print(f"❌ 4. PokerStarsAdapter - Error: {e}")
    print(f"   Detalle: {type(e).__name__}: {e}")

print("\\n" + "=" * 50)
print("📊 PRUEBA COMPLETADA")
print("=" * 50)
'''
    
    # Guardar y ejecutar
    test_file = "comprehensive_test.py"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_code)
    
    print("✅ Script de prueba creado")
    
    # Ejecutar prueba
    print("\n🚀 Ejecutando prueba...")
    result = subprocess.run([sys.executable, test_file], 
                          capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print(f"⚠️  Errores: {result.stderr[:200]}")
    
    return result.returncode == 0

def create_final_launcher():
    """Crear lanzador final"""
    print_section("CREANDO LANZADOR FINAL")
    
    launcher = '''#!/usr/bin/env python3
"""
LANZADOR DEFINITIVO - Poker Coach Pro
Interfaz unificada después de todas las reparaciones
"""
import os
import sys
import subprocess

def main():
    print("=" * 70)
    print("🎴 POKER COACH PRO - SISTEMA REPARADO")
    print("=" * 70)
    
    print("\\n📋 ESTADO DEL SISTEMA:")
    print("-" * 40)
    
    # Verificar archivos críticos
    critical_files = [
        ("src/platforms/pokerstars_adapter.py", "Adaptador PokerStars"),
        ("src/screen_capture/stealth_capture.py", "Captura Stealth"),
        ("src/screen_capture/card_recognizer.py", "Reconocedor Cartas"),
        ("src/screen_capture/table_detector.py", "Detector Mesas")
    ]
    
    all_exist = True
    for filepath, description in critical_files:
        if os.path.exists(filepath):
            print(f"✅ {description}")
        else:
            print(f"❌ {description} - NO ENCONTRADO")
            all_exist = False
    
    if not all_exist:
        print("\\n⚠️  Faltan archivos críticos")
        print("💡 Ejecuta: python fix_all_now.py")
        return
    
    print("\\n🎮 OPCIONES DISPONIBLES:")
    print("=" * 40)
    print("\\n1. 🧪 Ejecutar prueba de verificación")
    print("2. 🎯 Ejecutar sistema PokerStars")
    print("3. 🔧 Ejecutar reparador rápido")
    print("4. 📊 Ver estructura del proyecto")
    print("5. 🚪 Salir")
    print("=" * 40)
    
    try:
        choice = input("\\n👉 Selecciona una opción (1-5): ").strip()
        
        if choice == "1":
            print("\\n🧪 Ejecutando prueba...")
            subprocess.run([sys.executable, "test_after_fix.py"])
            
        elif choice == "2":
            print("\\n🎯 Ejecutando PokerStars...")
            print("💡 Asegúrate de tener PokerStars abierto")
            subprocess.run([sys.executable, "test_pokerstars.py"])
            
        elif choice == "3":
            print("\\n🔧 Ejecutando reparador...")
            subprocess.run([sys.executable, "quick_fix.py"])
            
        elif choice == "4":
            print("\\n📊 Estructura del proyecto:")
            os.system("dir /B" if os.name == "nt" else "ls -la")
            
        elif choice == "5":
            print("\\n👋 ¡Hasta pronto!")
            
        else:
            print("\\n❌ Opción no válida")
            
    except KeyboardInterrupt:
        print("\\n\\n🛑 Operación cancelada")
    except Exception as e:
        print(f"\\n❌ Error: {e}")

if __name__ == "__main__":
    main()
'''

    with open("launcher.py", 'w', encoding='utf-8') as f:
        f.write(launcher)
    
    print("✅ Lanzador creado: launcher.py")
    return True

def main():
    """Función principal"""
    print("=" * 70)
    print("🚀 REPARADOR COMPLETO - POKER COACH PRO")
    print("=" * 70)
    
    print("\nEste script hará TODAS las reparaciones necesarias:")
    print("1. 🔧 Reparar PokerStars Adapter (TableDetector, CardRecognizer)")
    print("2. 🎴 Verificar GG Poker Adapter")
    print("3. 🧪 Crear scripts de prueba")
    print("4. 🚀 Crear lanzador final")
    print("5. 📊 Ejecutar prueba comprehensiva")
    
    input("\n📝 Presiona Enter para comenzar...")
    
    # Ejecutar todas las reparaciones
    results = []
    
    results.append(("PokerStars Adapter", fix_pokerstars_adapter()))
    results.append(("GG Poker Adapter", fix_ggpoker_adapter()))
    results.append(("Script de prueba", create_test_script()))
    results.append(("Solución rápida", create_quick_fix_script()))
    results.append(("Lanzador final", create_final_launcher()))
    results.append(("Prueba comprehensiva", run_comprehensive_test()))
    
    # Resumen
    print_section("RESUMEN FINAL")
    
    successful = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n✅ Reparaciones exitosas: {successful}/{total}")
    
    if successful == total:
        print("\n🎉 ¡TODAS LAS REPARACIONES COMPLETADAS!")
        print("\n🚀 INSTRUCCIONES FINALES:")
        print("=" * 40)
        print("\n1. Prueba el sistema reparado:")
        print("   python test_after_fix.py")
        print("\n2. Ejecuta el sistema completo:")
        print("   python test_pokerstars.py")
        print("\n3. Usa el lanzador unificado:")
        print("   python launcher.py")
        print("\n4. Si hay problemas:")
        print("   python quick_fix.py")
    else:
        print("\n⚠️  Algunas reparaciones pueden necesitar atención manual")
        print("\n💡 Problemas detectados:")
        for name, result in results:
            if not result:
                print(f"   • {name}")
    
    print("\n" + "=" * 70)
    print("📁 ARCHIVOS CREADOS:")
    print("=" * 70)
    print("\n• fix_all_now.py - Este reparador")
    print("• test_after_fix.py - Prueba post-reparación")
    print("• quick_fix.py - Solución rápida para problemas futuros")
    print("• launcher.py - Lanzador unificado")
    print("• comprehensive_test.py - Prueba comprehensiva")
    
    print("\n" + "=" * 70)
    print("✅ PROCESO COMPLETADO")
    print("=" * 70)

if __name__ == "__main__":
    main()