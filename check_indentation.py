# check_indentation.py - Verificar indentación del código
import sys

def check_file_indentation(filename):
    """Verificar indentación de un archivo"""
    print(f" VERIFICANDO: {filename}")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f" Error leyendo archivo: {e}")
        return False
    
    errors = []
    for i, line in enumerate(lines, 1):
        # Verificar mezcla de tabs y espacios
        if '\t' in line:
            errors.append((i, "Contiene tabs (debe usar solo espacios)"))
        
        # Verificar indentación inconsistente
        stripped = line.lstrip(' ')
        indent_level = len(line) - len(stripped)
        if indent_level % 4 != 0 and stripped:  # No vacío
            errors.append((i, f"Indentación no múltiplo de 4: {indent_level} espacios"))
        
        # Verificar líneas que deberían tener indentación
        if i > 1 and lines[i-2].strip().endswith(':'):
            # Línea después de dos puntos debería estar indentada
            if stripped and indent_level == 0:
                errors.append((i, "Debe estar indentada después de ':'"))
    
    if not errors:
        print(" Indentación correcta")
        return True
    else:
        print(f" {len(errors)} errores de indentación:")
        for line_num, error in errors[:10]:  # Mostrar solo primeros 10
            print(f"   Línea {line_num}: {error}")
        if len(errors) > 10:
            print(f"   ... y {len(errors) - 10} errores más")
        return False

def main():
    """Función principal"""
    print(" VERIFICADOR DE INDENTACIÓN - POKER COACH PRO")
    print("=" * 70)
    
    files_to_check = [
        "start_auto_capture.py",
        "start_auto_capture_fixed.py",
        "manage_sessions.py",
        "src/session_manager.py",
        "src/auto_capture_system.py"
    ]
    
    all_ok = True
    for filename in files_to_check:
        import os
        if os.path.exists(filename):
            if not check_file_indentation(filename):
                all_ok = False
            print()
        else:
            print(f" Archivo no existe: {filename}\n")
    
    print("=" * 70)
    if all_ok:
        print(" Todos los archivos tienen indentación correcta!")
    else:
        print(" Algunos archivos tienen problemas de indentación")
        print("\n RECOMENDACIONES:")
        print("   1. Usa solo espacios (no tabs)")
        print("   2. Usa 4 espacios por nivel de indentación")
        print("   3. Verifica después de cada ':'")
        print("   4. Usa un editor con verificación de indentación")

if __name__ == "__main__":
    main()
