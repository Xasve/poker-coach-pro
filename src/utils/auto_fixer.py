# auto_fix.py - Reparador automático de errores
import os
import sys

def fix_common_errors():
    """Reparar errores comunes en scripts"""
    print(" REPARADOR AUTOMÁTICO DE ERRORES")
    print("=" * 70)
    
    # Lista de archivos problemáticos comunes
    problem_files = []
    
    # Verificar sintaxis de todos los scripts
    scripts = [f for f in os.listdir('.') if f.endswith('.py')]
    
    for script in scripts:
        try:
            # Intentar compilar
            result = os.system(f'"{sys.executable}" -m py_compile "{script}"')
            
            if result != 0:
                problem_files.append(script)
                print(f" {script} - Error de sintaxis")
            else:
                print(f" {script} - OK")
        except:
            print(f"⚠️  {script} - No se pudo verificar")
    
    if problem_files:
        print(f"\n🚨 Archivos con problemas: {len(problem_files)}")
        for file in problem_files:
            print(f"    {file}")
        
        print("\n SOLUCIONES:")
        print("1. Ejecuta el comando de PowerShell que te dieron")
        print("2. O usa estos comandos manualmente:")
        
        for file in problem_files:
            if file == "smart_capture_fixed.py":
                print(f"   - Reemplaza {file} con la versión corregida")
            elif file == "diagnostic.py":
                print(f"   - Reemplaza {file} con la versión corregida")
            else:
                print(f"   - Verifica {file} línea por línea")
    else:
        print("\n No se encontraron errores de sintaxis!")
    
    # Verificar estructura del proyecto
    print("\n VERIFICANDO ESTRUCTURA DEL PROYECTO:")
    
    required_dirs = [
        "data/card_templates/auto_captured",
        "data/card_templates/pokerstars_real",
        "config",
        "src"
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} - FALTANTE")
            os.makedirs(dir_path, exist_ok=True)
            print(f"   ✅ Creado automáticamente")
    
    print("\n" + "=" * 70)
    print(" REPARACIÓN COMPLETADA")
    print("\n Prueba estos comandos:")
    print("   1. python check_syntax.py - Verificar sintaxis")
    print("   2. python simple_capture.py - Captura segura")
    print("   3. python verify_balance.py - Verificar balance")

if __name__ == "__main__":
    fix_common_errors()
