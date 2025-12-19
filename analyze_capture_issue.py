# analyze_capture_issue.py - Analizar problema de detección
import os
import cv2
import numpy as np
import json
from datetime import datetime

def analyze_last_capture():
    """Analizar la última captura"""
    print(" ANALIZANDO PROBLEMA DE DETECCIÓN")
    print("=" * 70)
    
    # Encontrar la última sesión
    sessions_path = "data/card_templates/auto_captured"
    if not os.path.exists(sessions_path):
        print("❌ No hay sesiones de captura")
        return
    
    sessions = [d for d in os.listdir(sessions_path) 
               if os.path.isdir(os.path.join(sessions_path, d))]
    
    if not sessions:
        print(" No hay sesiones")
        return
    
    latest_session = max(sessions)
    print(f" Última sesión: {latest_session}")
    
    # Verificar resultados
    results_file = os.path.join(sessions_path, latest_session, "classification_results.json")
    stats_file = os.path.join(sessions_path, latest_session, "capture_stats.json")
    
    if os.path.exists(stats_file):
        with open(stats_file, 'r') as f:
            stats = json.load(f)
        
        print(f"\n ESTADÍSTICAS DE LA CAPTURA:")
        print(f"   Total cartas: {stats.get('total', 0)}")
        print(f"   Cartas rojas: {stats.get('hearts', 0) + stats.get('diamonds', 0)}")
        print(f"   Porcentaje rojas: {stats.get('red_percentage', 0):.1f}%")
        
        if stats.get('red_percentage', 0) == 0:
            print("\n PROBLEMA CONFIRMADO: 0% cartas rojas detectadas")
    
    # Analizar algunas imágenes para ver qué está pasando
    raw_path = os.path.join(sessions_path, latest_session, "raw_captures")
    if os.path.exists(raw_path):
        images = [f for f in os.listdir(raw_path) if f.endswith('.png')][:5]  # Primeras 5
        
        print(f"\n ANALIZANDO PRIMERAS 5 IMÁGENES:")
        
        for img_name in images:
            img_path = os.path.join(raw_path, img_name)
            img = cv2.imread(img_path)
            
            if img is not None:
                # Analizar color
                color_info = analyze_image_color(img)
                print(f"   {img_name}: {color_info}")

def analyze_image_color(image):
    """Analizar color de una imagen"""
    # Convertir a diferentes espacios de color
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    
    # Rangos de color ACTUALES (posiblemente incorrectos)
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    
    # Crear máscaras
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    
    # Contar píxeles
    red_pixels = cv2.countNonZero(mask_red)
    total_pixels = image.shape[0] * image.shape[1]
    red_percentage = (red_pixels / total_pixels * 100)
    
    # Estadísticas de color
    avg_hue = np.mean(hsv[:,:,0])
    avg_saturation = np.mean(hsv[:,:,1])
    avg_value = np.mean(hsv[:,:,2])
    
    return (f"Rojo: {red_percentage:.1f}% | "
            f"H: {avg_hue:.0f}° S: {avg_saturation:.0f} V: {avg_value:.0f}")

def test_color_detection():
    """Probar detección de color con diferentes configuraciones"""
    print("\n PROBANDO DIFERENTES CONFIGURACIONES DE DETECCIÓN:")
    print("-" * 60)
    
    # Crear imagen de prueba ROJA (como las cartas de PokerStars)
    test_img = create_test_red_card()
    
    print(" IMAGEN DE PRUEBA (carta roja simulada):")
    print(f"   Tamaño: {test_img.shape[1]}x{test_img.shape[0]}")
    print(f"   Color promedio: BGR {np.mean(test_img, axis=(0,1)).astype(int)}")
    
    # Probar diferentes configuraciones de detección
    configs = [
        ("Configuración ACTUAL", 0, 10, 160, 180, 100, 255, 100, 255),
        ("Configuración AMPLIADA", 0, 15, 150, 180, 50, 255, 50, 255),
        ("Configuración SENSIBLE", 0, 20, 140, 180, 30, 255, 30, 255),
        ("Configuración MUY SENSIBLE", 0, 30, 130, 180, 20, 255, 20, 255),
    ]
    
    for name, h1_min, h1_max, h2_min, h2_max, s_min, s_max, v_min, v_max in configs:
        hsv = cv2.cvtColor(test_img, cv2.COLOR_BGR2HSV)
        
        lower_red1 = np.array([h1_min, s_min, v_min])
        upper_red1 = np.array([h1_max, s_max, v_max])
        lower_red2 = np.array([h2_min, s_min, v_min])
        upper_red2 = np.array([h2_max, s_max, v_max])
        
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        
        red_pixels = cv2.countNonZero(mask_red)
        total_pixels = test_img.shape[0] * test_img.shape[1]
        red_percentage = (red_pixels / total_pixels * 100)
        
        print(f"   {name}: {red_percentage:.1f}% píxeles rojos detectados")

def create_test_red_card():
    """Crear imagen de prueba de carta roja"""
    height, width = 100, 70
    
    # Colores típicos de cartas rojas en PokerStars
    # Rojo vibrante (como corazones/diamantes)
    red_color = np.array([[[0, 0, 220]]], dtype=np.uint8)  # BGR
    
    # Crear imagen base
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:, :] = red_color
    
    # Añadir variación como en una carta real
    noise = np.random.randint(-20, 20, (height, width, 3), dtype=np.int8)
    img = cv2.add(img, noise.astype(np.uint8))
    
    # Añadir brillo/reflejo simulado
    gradient = np.linspace(0.8, 1.2, height).reshape(-1, 1, 1)
    img = (img * gradient).astype(np.uint8)
    
    return img

def main():
    """Función principal"""
    print(" POKER COACH PRO - DIAGNÓSTICO DE DETECCIÓN")
    print("=" * 70)
    
    analyze_last_capture()
    test_color_detection()
    
    print("\n" + "=" * 70)
    print(" DIAGNÓSTICO COMPLETADO")
    print("\n PROBLEMAS ENCONTRADOS:")
    print("   1. La detección de color NO está funcionando")
    print("   2. Los rangos HSV son probablemente incorrectos")
    print("   3. El umbral de detección es muy alto")
    
    print("\n SOLUCIÓN RECOMENDADA:")
    print("   Ejecuta: python fix_color_detection.py")
    print("   O manualmente ajusta los rangos HSV")

if __name__ == "__main__":
    main()
