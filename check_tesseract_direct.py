# check_tesseract_direct.py
import sys
import os

print("=== VERIFICACION DIRECTA DE TESSERACT ===")

try:
    import pytesseract
    print("[OK] pytesseract importado")
    
    # Buscar Tesseract en rutas comunes
    paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    
    username = os.getenv('USERNAME')
    if username:
        paths.append(rf"C:\Users\{username}\AppData\Local\Tesseract-OCR\tesseract.exe")
    
    found = False
    for path in paths:
        if os.path.exists(path):
            print(f"[OK] Tesseract encontrado en: {path}")
            pytesseract.pytesseract.tesseract_cmd = path
            found = True
            break
    
    if not found:
        # Buscar en PATH
        import shutil
        tesseract_cmd = shutil.which('tesseract')
        if tesseract_cmd:
            print(f"[OK] Tesseract en PATH: {tesseract_cmd}")
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
            found = True
    
    if found:
        try:
            version = pytesseract.get_tesseract_version()
            print(f"[OK] Version Tesseract: {version}")
            
            # Crear y probar imagen simple
            print("\n--- Probando OCR ---")
            try:
                from PIL import Image, ImageDraw, ImageFont
                
                # Crear imagen de prueba
                img = Image.new('RGB', (300, 50), color='white')
                d = ImageDraw.Draw(img)
                
                try:
                    font = ImageFont.truetype("arial.ttf", 20)
                except:
                    font = ImageFont.load_default()
                
                d.text((10, 10), "Test OCR: 12345", fill='black', font=font)
                
                # Probar OCR
                text = pytesseract.image_to_string(img)
                print(f"[OK] OCR funcionando. Texto reconocido: '{text.strip()}'")
                
            except Exception as img_error:
                print(f"[INFO] No se pudo crear imagen de prueba: {img_error}")
                
        except Exception as ver_error:
            print(f"[ERROR] No se pudo obtener version: {ver_error}")
    else:
        print("[ERROR] Tesseract no encontrado")
        print("\n[INSTALACION] Descarga Tesseract OCR desde:")
        print("https://github.com/UB-Mannheim/tesseract/wiki")
        print("\n[NOTA] Instala y marca 'Add to PATH'")
        
except ImportError as e:
    print(f"[ERROR] pytesseract no instalado: {e}")
    print("\n[SOLUCION] Ejecuta: pip install pytesseract==0.3.10")
except Exception as e:
    print(f"[ERROR] Inesperado: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n=== VERIFICACION COMPLETADA ===")