#!/usr/bin/env python3
"""
Elimina duplicados del requirements.txt y deja solo versiones específicas.
"""

print("🔄 Corrigiendo duplicados en requirements.txt...")

with open("requirements.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Separar encabezados y paquetes
headers = []
packages = {}
current_header = ""

for line in lines:
    line = line.strip()
    if not line:
        continue
    
    if line.startswith("# "):
        current_header = line
        if current_header not in headers:
            headers.append(current_header)
    else:
        # Extraer nombre del paquete (sin versión)
        if ">=" in line:
            pkg_name = line.split(">=")[0].strip()
        elif "==" in line:
            pkg_name = line.split("==")[0].strip()
        else:
            pkg_name = line.strip()
        
        # Preferir la versión con >= si existe
        if pkg_name not in packages or ">=" in line:
            packages[pkg_name] = line

print(f"✅ Encontrados {len(packages)} paquetes únicos")

# Versiones específicas para compatibilidad con Python 3.11
RECOMMENDED_VERSIONS = {
    "opencv-python": "opencv-python>=4.8.0",
    "pillow": "pillow>=10.0.0",
    "numpy": "numpy>=1.24.0,<2.0.0",  # Evitar numpy 2.x por ahora
    "mss": "mss>=9.0.1",
    "pyautogui": "pyautogui>=0.9.54",
    "pytesseract": "pytesseract>=0.3.10",
    "colorama": "colorama>=0.4.6",
    "pyyaml": "pyyaml>=6.0",
    "tqdm": "tqdm>=4.66.0",
    "pandas": "pandas>=2.0.0,<2.2.0",
    "scikit-learn": "scikit-learn>=1.3.0",
    "matplotlib": "matplotlib>=3.7.0,<3.9.0",
}

# Actualizar con versiones recomendadas
for pkg, recommended in RECOMMENDED_VERSIONS.items():
    if pkg in packages:
        packages[pkg] = recommended
        print(f"  📦 Actualizado: {pkg} -> {recommended}")

# Escribir nuevo archivo organizado
with open("requirements.txt", "w", encoding="utf-8") as f:
    f.write("# DEPENDENCIAS POKER COACH PRO - PYTHON 3.11\n")
    f.write("# ==========================================\n")
    f.write("# Versiones compatibles con Python 3.11\n")
    f.write("# Generado automáticamente - NO EDITAR MANUALMENTE\n\n")
    
    f.write("# PROCESAMIENTO DE IMAGEN Y CAPTURA\n")
    image_pkgs = ["opencv-python", "pillow", "numpy", "mss", "pyautogui"]
    for pkg in image_pkgs:
        if pkg in packages:
            f.write(f"{packages[pkg]}\n")
    
    f.write("\n# OCR Y RECONOCIMIENTO\n")
    ocr_pkgs = ["pytesseract"]
    for pkg in ocr_pkgs:
        if pkg in packages:
            f.write(f"{packages[pkg]}\n")
    
    f.write("\n# UTILIDADES Y FRAMEWORKS\n")
    utility_pkgs = ["colorama", "pyyaml", "tqdm", "pandas", "scikit-learn", "matplotlib"]
    for pkg in utility_pkgs:
        if pkg in packages:
            f.write(f"{packages[pkg]}\n")
    
    # Paquetes adicionales no categorizados
    other_pkgs = [pkg for pkg in packages if pkg not in image_pkgs + ocr_pkgs + utility_pkgs]
    if other_pkgs:
        f.write("\n# OTRAS DEPENDENCIAS\n")
        for pkg in other_pkgs:
            f.write(f"{packages[pkg]}\n")

print(f"\n📄 requirements.txt final ({len(packages)} paquetes):")
print("=" * 60)
with open("requirements.txt", "r", encoding="utf-8") as f:
    print(f.read())
print("=" * 60)

print("\n✅ Listo! Ahora ejecuta el PowerShell simplificado.")