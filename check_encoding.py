# check_encoding.py
import os

def check_file_encoding(filepath):
    """Verificar encoding de un archivo"""
    print(f"\n🔍 Verificando: {filepath}")
    
    try:
        # Intentar con UTF-8
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"  ✅ UTF-8: OK ({len(content)} caracteres)")
            return True
    except UnicodeDecodeError:
        pass
    
    try:
        # Intentar con latin-1
        with open(filepath, 'r', encoding='latin-1') as f:
            content = f.read()
            print(f"  ✅ Latin-1: OK ({len(content)} caracteres)")
            
            # Verificar caracteres problemáticos
            problem_chars = [c for c in content if ord(c) > 127]
            if problem_chars:
                print(f"  ⚠️  Caracteres no-ASCII: {set(problem_chars)}")
            
            return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    print("=== VERIFICACIÓN DE ENCODING ===")
    
    # Archivos críticos
    critical_files = [
        "src/platforms/pokerstars_adapter.py",
        "src/screen_capture/stealth_capture.py",
        "src/core/poker_engine.py",
        "src/integration/poker_coach_integrator.py",
    ]
    
    all_ok = True
    
    for file in critical_files:
        if os.path.exists(file):
            if not check_file_encoding(file):
                all_ok = False
        else:
            print(f"\n❌ No encontrado: {file}")
            all_ok = False
    
    print("\n" + "=" * 50)
    if all_ok:
        print("✅ Encoding verificado")
    else:
        print("⚠️  Problemas de encoding detectados")

if __name__ == "__main__":
    main()