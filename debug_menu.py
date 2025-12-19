# debug_menu.py - Diagnóstico del menú
import sys
import os

def test_menu_parsing():
    """Probar el parsing del menú"""
    print(" DIAGNÓSTICO DEL MENÚ - start_auto_capture.py")
    print("=" * 70)
    
    # Leer el archivo
    try:
        with open("start_auto_capture.py", "r", encoding="utf-8") as f:
            content = f.read()
    except:
        print("❌ No se puede leer el archivo")
        return
    
    # Buscar la función show_menu
    import re
    pattern = r'def show_menu\(\):.*?return choice'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print(" No se encontró la función show_menu")
        return
    
    menu_text = match.group(0)
    print("✅ Función show_menu encontrada")
    
    # Buscar números de opción
    option_pattern = r'print\("(\d+)\.'
    options = re.findall(option_pattern, menu_text)
    
    if options:
        print(f"\n OPCIONES ENCONTRADAS: {options}")
        
        # Verificar que sean números válidos
        valid_options = []
        for opt in options:
            if opt.isdigit():
                valid_options.append(int(opt))
        
        print(f" Opciones numéricas: {valid_options}")
        
        # Verificar continuidad
        expected = list(range(1, len(valid_options) + 1))
        if valid_options == expected:
            print("✅ Opciones bien numeradas (1-{})".format(len(valid_options)))
        else:
            print("❌ Problema con la numeración")
            print(f"   Esperado: {expected}")
            print(f"   Encontrado: {valid_options}")
    else:
        print("❌ No se encontraron opciones numeradas")
    
    # Buscar caracteres problemáticos
    print("\n ANÁLISIS DE CARACTERES:")
    
    # Verificar caracteres no ASCII
    non_ascii = []
    for i, char in enumerate(menu_text):
        if ord(char) > 127:
            non_ascii.append((i, char, ord(char)))
    
    if non_ascii:
        print("  Caracteres no ASCII encontrados:")
        for pos, char, code in non_ascii[:10]:
            line_num = menu_text[:pos].count('\n') + 1
            print(f"   Posición {pos} (línea ~{line_num}): '{char}' (U+{code:04X})")
    else:
        print(" Solo caracteres ASCII")
    
    # Buscar la parte de manejo de opciones
    print("\n BUSCANDO MANEJO DE OPCIONES:")
    handling_pattern = r'if choice == 1:.*?else:.*?print'
    handling_match = re.search(handling_pattern, content, re.DOTALL)
    
    if handling_match:
        print("✅ Sección de manejo de opciones encontrada")
        
        # Extraer las condiciones
        conditions = []
        lines = handling_match.group(0).split('\n')
        for line in lines:
            if 'elif choice ==' in line:
                # Extraer número
                import re
                num_match = re.search(r'choice == (\d+)', line)
                if num_match:
                    conditions.append(int(num_match.group(1)))
        
        print(f" Condiciones encontradas: {conditions}")
        
        # Verificar coherencia
        if set(conditions) == set(valid_options) - {len(valid_options)}:  # Restar la última opción (salir)
            print(" Coherencia entre menú y manejo de opciones")
        else:
            print("❌ Discrepancia entre menú y manejo")
            print(f"   Menú: {valid_options}")
            print(f"   Manejo: {conditions}")
    else:
        print(" No se encontró manejo de opciones")

def test_input_parsing():
    """Probar parsing de entrada"""
    print("\n" + "=" * 70)
    print(" PRUEBA DE PARSING DE ENTRADA")
    print("=" * 70)
    
    test_inputs = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "0", "10", "a", "5 ", " 5", "5.0", "五"
    ]
    
    for test in test_inputs:
        try:
            result = int(test)
            print(f" '{test}'  {result} (válido)")
        except ValueError:
            print(f" '{test}'  Error (no es número entero)")

def main():
    """Función principal"""
    print(" DIAGNÓSTICO DEL SISTEMA DE MENÚS")
    print("=" * 70)
    
    print("Este script ayuda a diagnosticar problemas con los menús")
    print("y el parsing de opciones en el sistema.")
    
    test_menu_parsing()
    test_input_parsing()
    
    print("\n" + "=" * 70)
    print("💡 RECOMENDACIONES:")
    print("   1. Usar solo números 1-9 en los menús")
    print("   2. Evitar caracteres especiales/emojis problemáticos")
    print("   3. Verificar que cada opción tenga su manejo correspondiente")
    print("   4. Probar con diferentes tipos de entrada")
    
    print("\n PARA PROBAR:")
    print("   Ejecuta: python start_auto_capture.py")
    print("   Prueba seleccionando opción 5")

if __name__ == "__main__":
    main()
