# test_simple.py - Versión mínima para prueba
print(" PRUEBA MÍNIMA DEL SISTEMA")
print("=" * 50)

# Solo probar el menú básico
def test_menu():
    print("\n1. Sistema Completo")
    print("2. Captura Rápida")
    print("3. Clasificar")
    print("4. Ver Sesiones")
    print("5. Gestionar")
    print("6. Verificar")
    print("7. Reportes")
    print("8. Ayuda")
    print("9. Salir")
    
    try:
        choice = int(input("\nOpción: "))
        print(f"Seleccionaste: {choice}")
        
        if choice == 9:
            print("Saliendo...")
            return False
        else:
            print("(Función no implementada en prueba)")
            return True
    except:
        print("Entrada inválida")
        return True

# Bucle simple
while test_menu():
    input("\nPresiona Enter para continuar...")

print("\n Prueba completada")
