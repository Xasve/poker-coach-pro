#!/usr/bin/env python3
print("="*60)
print(" REPARACIÓN RÁPIDA ULTIMATE")
print("="*60)

import os

# 1. Reparar pokerstars_adapter.py
adapter = "src/platforms/pokerstars_adapter.py"
if os.path.exists(adapter):
    with open(adapter, "r", encoding="utf-8") as f:
        txt = f.read()
    
    print(" Aplicando correcciones...")
    
    # TableDetector
    txt = txt.replace('TableDetector("pokerstars")', 'TableDetector()')
    print(" TableDetector corregido")
    
    # CardRecognizer  
    txt = txt.replace('CardRecognizer(self.platform, self.stealth_level)', 'CardRecognizer(platform=self.platform)')
    print(" CardRecognizer corregido")
    
    # TextOCR
    txt = txt.replace('TextOCR(self.stealth_level)', 'TextOCR()')
    txt = txt.replace('TextOCR(self.platform, self.stealth_level)', 'TextOCR()')
    txt = txt.replace('TextOCR("pokerstars")', 'TextOCR()')
    print(" TextOCR corregido")
    
    with open(adapter, "w", encoding="utf-8") as f:
        f.write(txt)
    
    print(" Archivo guardado")
else:
    print(" Archivo no encontrado")

print("\n Reparaciones aplicadas")
print("\n Ahora ejecuta: python test_pokerstars.py")
print("="*60)
