# setup_ocr_simple.py
import os
import sys
import subprocess

def run_command(cmd):
    """Ejecutar comando y mostrar resultado"""
    print(f"🚀 Ejecutando: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        if result.stdout:
            print(f"📋 {result.stdout.strip()}")
        return True
    else:
        print(f"❌ Error: {result.stderr}")
        return False

def main():
    print("🔤 CONFIGURACIÓN SIMPLIFICADA DE OCR")
    print("=" * 60)
    
    print("1. Instalando pytesseract...")
    if not run_command("pip install pytesseract==0.3.10"):
        print("⚠️  Intenta manualmente: pip install pytesseract==0.3.10")
        return False
    
    print("\n2. Verificando instalación...")
    run_command("pip show pytesseract")
    
    print("\n3. Buscando Tesseract OCR...")
    
    # Usar un nuevo proceso Python para verificar
    check_script = '''
import sys
try:
    import pytesseract
    print("✅ pytesseract importado correctamente")
    
    # Buscar Tesseract
    import os
    paths = [
        r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
        r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe",
        r"C:\\Users\\{}\\AppData\\Local\\Tesseract-OCR\\tesseract.exe".format(os.getenv('USERNAME')),
    ]
    
    found = False
    for path in paths:
        if os.path.exists(path):
            print(f"✅ Tesseract encontrado: {path}")
            pytesseract.pytesseract.tesseract_cmd = path
            found = True
            break
    
    if not found:
        # Buscar en PATH
        import shutil
        tesseract_cmd = shutil.which('tesseract')
        if tesseract_cmd:
            print(f"✅ Tesseract en PATH: {tesseract_cmd}")
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
            found = True
    
    if found:
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✅ Versión Tesseract: {version}")
        except:
            print("⚠️  No se pudo obtener versión")
    else:
        print("❌ Tesseract no encontrado")
        print("📥 Descarga desde: https://github.com/UB-Mannheim/tesseract/wiki")
        
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
'''
    
    # Guardar y ejecutar script en nuevo proceso
    with open("temp_check_ocr.py", "w") as f:
        f.write(check_script)
    
    run_command("python temp_check_ocr.py")
    
    # Limpiar
    if os.path.exists("temp_check_ocr.py"):
        os.remove("temp_check_ocr.py")
    
    print("\n" + "=" * 60)
    print("✅ Configuración completada")
    print("\n💡 Si Tesseract no está instalado, descárgalo e instálalo:")
    print("https://github.com/UB-Mannheim/tesseract/wiki")
    
    return True

if __name__ == "__main__":
    main()