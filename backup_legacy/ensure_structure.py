# ensure_structure.py
import os

def ensure_structure():
    """Asegurar que toda la estructura de directorios existe"""
    
    print("=== VERIFICANDO ESTRUCTURA DEL PROYECTO ===")
    
    directories = [
        'src',
        'src/screen_capture',
        'src/platforms',
        'src/core',
        'src/integration',
        'src/utils',
        'src/overlay',
        'config',
        'data',
        'data/card_templates/pokerstars',
        'debug',
        'logs',
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ {directory}/")
    
    # Verificar archivos críticos
    critical_files = [
        ('src/__init__.py', '# Package initialization'),
        ('src/screen_capture/__init__.py', '# Screen capture modules'),
        ('src/platforms/__init__.py', '# Platform adapters'),
        ('src/core/__init__.py', '# Core engine modules'),
        ('src/integration/__init__.py', '# Integration modules'),
        ('src/utils/__init__.py', '# Utility modules'),
        ('src/overlay/__init__.py', '# Overlay modules'),
    ]
    
    print("\n=== VERIFICANDO ARCHIVOS CRÍTICOS ===")
    
    for file_path, default_content in critical_files:
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(default_content)
            print(f"📄 Creado: {file_path}")
        else:
            print(f"✅ Existe: {file_path}")
    
    print("\n=== ESTRUCTURA COMPLETADA ===")
    print("✅ Proyecto listo para ejecución")

if __name__ == "__main__":
    ensure_structure()