# setup.py - Instalación simplificada
import os
import sys
import subprocess

def run_command(command, description):
    """Ejecutar comando con descripción"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completado")
            return True
        else:
            print(f"❌ Error en {description}:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error ejecutando {description}: {e}")
        return False

def main():
    """Instalación principal"""
    print("🎴 POKER COACH PRO - INSTALACIÓN SIMPLIFICADA")
    print("=" * 70)
    
    # 1. Verificar Python
    print("\n1️⃣ VERIFICANDO PYTHON...")
    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 11:
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print(f"⚠️  Python {python_version.major}.{python_version.minor} - Se recomienda 3.11+")
    
    # 2. Crear/activar entorno virtual
    if not os.path.exists("venv"):
        print("\n2️⃣ CREANDO ENTORNO VIRTUAL...")
        run_command(f"{sys.executable} -m venv venv", "Crear entorno virtual")
    
    # Determinar script de activación
    activate_script = "venv\\Scripts\\activate" if os.name == 'nt' else "venv/bin/activate"
    
    # 3. Instalar dependencias básicas
    print("\n3️⃣ INSTALANDO DEPENDENCIAS BÁSICAS...")
    
    # Lista de paquetes básicos (siempre necesarios)
    basic_packages = [
        "numpy==1.24.4",
        "opencv-python==4.9.0.80",
        "mss==9.0.1",
        "pillow==10.3.0",
        "pyyaml==6.0.1",
        "colorama==0.4.6"
    ]
    
    all_success = True
    for package in basic_packages:
        cmd = f"venv\\Scripts\\pip install {package}" if os.name == 'nt' else f"./venv/bin/pip install {package}"
        success = run_command(cmd, f"Instalando {package}")
        if not success:
            all_success = False
    
    # 4. Preguntar por dependencias avanzadas
    print("\n4️⃣ DEPENDENCIAS AVANZADAS (OPCIONAL)")
    print("Estas dependencias son para funciones de Machine Learning:")
    print("   • Clasificación automática de cartas")
    print("   • Generación de reportes gráficos")
    print("   • Análisis avanzado")
    
    response = input("\n¿Instalar dependencias avanzadas? (s/n): ")
    
    if response.lower() == 's':
        advanced_packages = [
            "scikit-learn==1.3.2",
            "matplotlib==3.8.2"
        ]
        
        for package in advanced_packages:
            cmd = f"venv\\Scripts\\pip install {package}" if os.name == 'nt' else f"./venv/bin/pip install {package}"
            run_command(cmd, f"Instalando {package}")
    
    # 5. Crear estructura de directorios
    print("\n5️⃣ CREANDO ESTRUCTURA...")
    
    directories = [
        "data/card_templates/pokerstars_real",
        "data/card_templates/pokerstars_real/hearts",
        "data/card_templates/pokerstars_real/diamonds",
        "data/card_templates/pokerstars_real/clubs",
        "data/card_templates/pokerstars_real/spades",
        "data/card_templates/auto_captured",
        "config",
        "logs",
        "debug",
        "models"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 {directory}")
    
    # 6. Verificar archivos esenciales
    print("\n6️⃣ VERIFICANDO ARCHIVOS...")
    
    essential_files = [
        "main.py",
        "detect_coords.py",
        "start_auto_capture.py",
        "src/card_detector.py",
        "src/auto_template_capturer.py"
    ]
    
    missing_files = []
    for file in essential_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Faltan {len(missing_files)} archivos esenciales")
        print("�� Asegúrate de tener todos los archivos del repositorio")
    
    # 7. Resumen
    print("\n" + "=" * 70)
    print("🎉 ¡INSTALACIÓN COMPLETADA!")
    print("=" * 70)
    
    if all_success:
        print("\n✅ Todas las dependencias básicas instaladas")
    else:
        print("\n⚠️  Algunas dependencias pueden no estar instaladas")
    
    print("\n🚀 PARA COMENZAR:")
    print("   1. Activa el entorno virtual:")
    print("      Windows: venv\\Scripts\\activate")
    print("      Linux/Mac: source venv/bin/activate")
    print("\n   2. Configura PokerStars:")
    print("      python detect_coords.py")
    print("\n   3. Ejecuta el sistema:")
    print("      python start_auto_capture.py")
    
    print("\n📚 MÁS INFORMACIÓN:")
    print("   • Revisa README.md para instrucciones detalladas")
    print("   • Ejecuta check_system.py para verificar instalación")
    
    print("\n⚠️  RECUERDA:")
    print("   • Este sistema es para APRENDIZAJE")
    print("   • Verifica los Términos de PokerStars")
    print("   • Úsalo de manera responsable")

if __name__ == "__main__":
    try:
        main()
        input("\nPresiona Enter para salir...")
    except KeyboardInterrupt:
        print("\n\n⏹️  Instalación interrumpida")
