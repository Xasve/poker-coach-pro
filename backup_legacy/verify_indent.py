# verify_indent.py - Verificar indentación específica
import sys

def check_specific_lines(filename, line_numbers):
    """Verificar líneas específicas"""
    print(f" VERIFICANDO LÍNEAS ESPECÍFICAS EN {filename}")
    print("-" * 50)
    
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print(f" Error leyendo archivo: {e}")
        return False
    
    for line_num in line_numbers:
        if line_num <= len(lines):
            line = lines[line_num - 1]
            print(f"Línea {line_num}: {repr(line.rstrip())}")
            
            # Verificar indentación
            leading_spaces = len(line) - len(line.lstrip())
            if leading_spaces % 4 != 0 and line.strip():
                print(f"    Indentación: {leading_spaces} espacios (debe ser múltiplo de 4)")
            
            # Verificar si es código válido después de if/elif/else
            if line_num > 1:
                prev_line = lines[line_num - 2]
                if prev_line.strip().endswith(':'):
                    if leading_spaces == 0 and line.strip():
                        print(f"    DEBE estar indentada después de ':' en línea {line_num-1}")
    
    return True

def main():
    """Función principal"""
    print(" VERIFICADOR DE INDENTACIÓN ESPECÍFICA")
    print("=" * 60)
    
    # Verificar las líneas problemáticas (alrededor de 150-151)
    check_specific_lines("start_auto_capture.py", [145, 146, 147, 148, 149, 150, 151, 152, 153])
    
    print("\n" + "=" * 60)
    print(" Si hay problemas, usa:")
    print("   python -m tabnanny start_auto_capture.py")
    print("   python -m py_compile start_auto_capture.py")

if __name__ == "__main__":
    main()
