# setup_tesseract_complete.py
import os
import sys
import subprocess
import tempfile
from pathlib import Path

def check_tesseract_installed():
    """Verificar si Tesseract está instalado"""
    print("🔍 Buscando Tesseract OCR...")
    
    # Rutas comunes en Windows
    common_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe".format(os.getenv('USERNAME')),
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            print(f"✅ Tesseract encontrado en: {path}")
            return path
    
    # Buscar en PATH
    try:
        result = subprocess.run(['where', 'tesseract'], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            path = result.stdout.strip().split('\n')[0]
            print(f"✅ Tesseract encontrado en PATH: {path}")
            return path
    except:
        pass
    
    print("❌ Tesseract no encontrado")
    return None

def install_tesseract_windows():
    """Instrucciones para instalar Tesseract en Windows"""
    print("\n📥 INSTALACIÓN DE TESSERACT OCR")
    print("=" * 50)
    
    print("1. Descarga Tesseract desde:")
    print("   https://github.com/UB-Mannheim/tesseract/wiki")
    print("\n2. Ejecuta el instalador:")
    print("   tesseract-ocr-w64-setup-5.3.3.20231005.exe")
    print("\n3. Durante la instalación:")
    print("   ✓ Marca 'Add to PATH'")
    print("   ✓ Instala idiomas necesarios (inglés, español)")
    print("\n4. Reinicia PowerShell/CMD después de instalar")
    
    return False

def test_pytesseract():
    """Probar pytesseract después de instalación"""
    print("\n🧪 PROBANDO PYTESSERACT...")
    
    try:
        import pytesseract
        
        # Verificar si tesseract_cmd está configurado
        if hasattr(pytesseract, 'pytesseract') and hasattr(pytesseract.pytesseract, 'tesseract_cmd'):
            tesseract_path = pytesseract.pytesseract.tesseract_cmd
            if os.path.exists(tesseract_path):
                print(f"✅ Tesseract configurado en: {tesseract_path}")
            else:
                print(f"⚠️  Ruta configurada no existe: {tesseract_path}")
        else:
            print("⚠️  tesseract_cmd no configurado")
        
        # Intentar obtener versión
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✅ Versión Tesseract: {version}")
            return True
        except:
            print("⚠️  No se pudo obtener versión")
            
            # Configurar manualmente
            tesseract_path = check_tesseract_installed()
            if tesseract_path:
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
                print(f"✅ Tesseract configurado manualmente")
                
                # Probar nuevamente
                try:
                    version = pytesseract.get_tesseract_version()
                    print(f"✅ Versión Tesseract: {version}")
                    return True
                except Exception as e:
                    print(f"❌ Error probando Tesseract: {e}")
    
    except ImportError as e:
        print(f"❌ pytesseract no instalado: {e}")
        print("\n💡 Instala con: pip install pytesseract==0.3.10")
    
    return False

def create_test_image():
    """Crear imagen de prueba para OCR"""
    print("\n🖼️ Creando imagen de prueba...")
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        import numpy as np
        
        # Crear imagen blanca
        img = Image.new('RGB', (400, 100), color='white')
        d = ImageDraw.Draw(img)
        
        # Intentar usar fuente simple
        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except:
            font = ImageFont.load_default()
        
        # Texto de prueba
        text = "Poker Coach Pro Test 123"
        d.text((20, 30), text, fill='black', font=font)
        
        # Guardar
        test_path = "debug/ocr_test.png"
        os.makedirs("debug", exist_ok=True)
        img.save(test_path)
        print(f"✅ Imagen de prueba creada: {test_path}")
        
        return test_path
        
    except Exception as e:
        print(f"⚠️  No se pudo crear imagen: {e}")
        return None

def test_ocr_functionality():
    """Probar funcionalidad OCR completa"""
    print("\n🔤 TEST DE FUNCIONALIDAD OCR")
    
    test_image = create_test_image()
    
    if not test_image or not os.path.exists(test_image):
        print("⚠️  No hay imagen para probar OCR")
        return False
    
    try:
        import pytesseract
        from PIL import Image
        
        # Configurar Tesseract si es necesario
        tesseract_path = check_tesseract_installed()
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        # Probar OCR
        print(f"📖 Procesando imagen: {test_image}")
        image = Image.open(test_image)
        text = pytesseract.image_to_string(image)
        
        print(f"✅ OCR funcionando!")
        print(f"📝 Texto reconocido: '{text.strip()}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en OCR: {type(e).__name__}: {e}")
        return False

def main():
    print("🔤 CONFIGURACIÓN COMPLETA DE TESSERACT OCR")
    print("=" * 60)
    
    # 1. Verificar/instalar pytesseract
    print("\n1. VERIFICANDO PYTESSERACT...")
    try:
        import pytesseract
        print("✅ pytesseract ya instalado")
    except ImportError:
        print("❌ pytesseract no instalado")
        print("\n💡 Instalando pytesseract...")
        os.system("pip install pytesseract==0.3.10")
        
        # Reintentar import
        try:
            import pytesseract
            print("✅ pytesseract instalado correctamente")
        except ImportError:
            print("❌ Falló la instalación de pytesseract")
            return False
    
    # 2. Verificar Tesseract OCR
    tesseract_path = check_tesseract_installed()
    
    if not tesseract_path:
        print("\n❌ TESSERACT OCR NO INSTALADO")
        install_tesseract_windows()
        
        # Preguntar si se instaló
        input("\n📌 Presiona Enter después de instalar Tesseract...")
        
        # Verificar nuevamente
        tesseract_path = check_tesseract_installed()
        if not tesseract_path:
            print("❌ Tesseract aún no encontrado")
            print("💡 Asegúrate de reiniciar PowerShell después de instalar")
            return False
    
    # 3. Configurar pytesseract
    print("\n2. CONFIGURANDO PYTESSERACT...")
    try:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        # Probar configuración
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract configurado: versión {version}")
        
    except Exception as e:
        print(f"❌ Error configurando pytesseract: {e}")
        return False
    
    # 4. Probar OCR
    print("\n3. PROBANDO OCR...")
    ocr_working = test_ocr_functionality()
    
    if ocr_working:
        print("\n" + "=" * 60)
        print("🎉 ¡TESSERACT OCR CONFIGURADO CORRECTAMENTE!")
        
        # Crear archivo de configuración
        config_code = f'''
# tesseract_config.py
import pytesseract
import os

# Configuración automática de Tesseract
TESSERACT_PATH = r"{tesseract_path}"

def setup_tesseract():
    """Configurar Tesseract para el proyecto"""
    if os.path.exists(TESSERACT_PATH):
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
        print(f"✅ Tesseract configurado: {TESSERACT_PATH}")
        return True
    else:
        print(f"⚠️  Tesseract no encontrado en: {TESSERACT_PATH}")
        return False

if __name__ == "__main__":
    setup_tesseract()
'''
        
        with open("tesseract_config.py", "w") as f:
            f.write(config_code)
        
        print(f"\n📁 Configuración guardada en: tesseract_config.py")
        print("💡 Importa este archivo en tu proyecto para configurar Tesseract")
        
    else:
        print("\n⚠️  OCR tiene problemas, pero Tesseract está instalado")
    
    return ocr_working

if __name__ == "__main__":
    success = main()
    print("\n✅ Configuración completada" if success else "❌ Configuración incompleta")