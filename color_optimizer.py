# color_optimizer.py - Sistema avanzado de detección de color
import cv2
import numpy as np
import json
import os
from datetime import datetime

class ColorOptimizer:
    """Optimizador avanzado de detección de color"""
    
    def __init__(self):
        self.color_profiles = {}
        self.load_profiles()
    
    def load_profiles(self):
        """Cargar perfiles de color preconfigurados"""
        profiles_file = "config/color_profiles.json"
        
        if os.path.exists(profiles_file):
            with open(profiles_file, 'r') as f:
                self.color_profiles = json.load(f)
        else:
            # Perfiles por defecto para diferentes mesas PokerStars
            self.color_profiles = {
                "classic": {
                    "red_lower": [0, 100, 100],
                    "red_upper": [10, 255, 255],
                    "red_lower2": [160, 100, 100],
                    "red_upper2": [180, 255, 255],
                    "saturation_threshold": 50,
                    "brightness_threshold": 30
                },
                "dark": {
                    "red_lower": [0, 120, 40],
                    "red_upper": [15, 255, 200],
                    "red_lower2": [165, 120, 40],
                    "red_upper2": [180, 255, 200],
                    "saturation_threshold": 60,
                    "brightness_threshold": 40
                },
                "stealth": {
                    "red_lower": [0, 80, 30],
                    "red_upper": [20, 220, 180],
                    "red_lower2": [170, 80, 30],
                    "red_upper2": [180, 220, 180],
                    "saturation_threshold": 40,
                    "brightness_threshold": 50
                }
            }
            
            # Guardar perfiles
            self.save_profiles()
    
    def save_profiles(self):
        """Guardar perfiles en archivo"""
        os.makedirs("config", exist_ok=True)
        with open("config/color_profiles.json", 'w') as f:
            json.dump(self.color_profiles, f, indent=2)
    
    def auto_calibrate(self, sample_images, table_type="unknown"):
        """Calibración automática basada en imágenes de muestra"""
        print(f" CALIBRANDO PARA: {table_type}")
        
        all_red_pixels = []
        
        for img_path in sample_images:
            image = cv2.imread(img_path)
            if image is None:
                continue
                
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Detectar píxeles rojos usando método actual
            red_mask = self.detect_red(hsv, table_type)
            red_pixels = hsv[red_mask > 0]
            
            if len(red_pixels) > 0:
                all_red_pixels.extend(red_pixels)
        
        if len(all_red_pixels) == 0:
            print(" No se encontraron píxeles rojos para calibración")
            return False
        
        # Calcular estadísticas
        all_red_pixels = np.array(all_red_pixels)
        h_mean, s_mean, v_mean = np.mean(all_red_pixels, axis=0)
        h_std, s_std, v_std = np.std(all_red_pixels, axis=0)
        
        # Crear nuevo perfil
        new_profile = {
            "red_lower": [
                max(0, int(h_mean - 2 * h_std)),
                max(30, int(s_mean - 1.5 * s_std)),
                max(30, int(v_mean - 1.5 * v_std))
            ],
            "red_upper": [
                min(180, int(h_mean + 2 * h_std)),
                min(255, int(s_mean + 1.5 * s_std)),
                min(255, int(v_mean + 1.5 * v_std))
            ],
            "red_lower2": [
                max(160, int((h_mean + 90) % 180 - 2 * h_std)),
                max(30, int(s_mean - 1.5 * s_std)),
                max(30, int(v_mean - 1.5 * v_std))
            ],
            "red_upper2": [
                180,
                min(255, int(s_mean + 1.5 * s_std)),
                min(255, int(v_mean + 1.5 * v_std))
            ],
            "saturation_threshold": max(30, int(s_mean - s_std)),
            "brightness_threshold": max(30, int(v_mean - v_std)),
            "calibrated_at": datetime.now().isoformat(),
            "sample_count": len(all_red_pixels)
        }
        
        # Guardar perfil
        profile_name = table_type if table_type != "unknown" else f"custom_{len(self.color_profiles)}"
        self.color_profiles[profile_name] = new_profile
        self.save_profiles()
        
        print(f" Perfil '{profile_name}' calibrado con {len(all_red_pixels)} píxeles")
        return True
    
    def detect_red(self, hsv_image, table_type="classic"):
        """Detección optimizada de color rojo"""
        if table_type not in self.color_profiles:
            table_type = "classic"
        
        profile = self.color_profiles[table_type]
        
        # Crear máscaras para rojo (dos rangos en HSV)
        lower_red1 = np.array(profile["red_lower"])
        upper_red1 = np.array(profile["red_upper"])
        
        lower_red2 = np.array(profile["red_lower2"])
        upper_red2 = np.array(profile["red_upper2"])
        
        mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
        
        # Combinar máscaras
        red_mask = cv2.bitwise_or(mask1, mask2)
        
        # Aplicar filtros adicionales
        saturation = hsv_image[:, :, 1]
        value = hsv_image[:, :, 2]
        
        # Filtrar por saturación mínima
        sat_mask = saturation > profile["saturation_threshold"]
        # Filtrar por brillo mínimo
        val_mask = value > profile["brightness_threshold"]
        
        # Combinar todos los filtros
        final_mask = red_mask & sat_mask.astype(np.uint8) * 255 & val_mask.astype(np.uint8) * 255
        
        # Operaciones morfológicas para limpiar la máscara
        kernel = np.ones((3, 3), np.uint8)
        final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_OPEN, kernel)
        final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_CLOSE, kernel)
        
        return final_mask
    
    def test_on_samples(self, test_images, expected_red_percentage=30):
        """Probar detección en imágenes de prueba"""
        results = []
        
        for img_path in test_images:
            image = cv2.imread(img_path)
            if image is None:
                continue
            
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Probar cada perfil
            for profile_name in self.color_profiles.keys():
                mask = self.detect_red(hsv, profile_name)
                red_pixels = np.sum(mask > 0)
                total_pixels = mask.shape[0] * mask.shape[1]
                red_percentage = (red_pixels / total_pixels) * 100
                
                results.append({
                    "image": os.path.basename(img_path),
                    "profile": profile_name,
                    "red_pixels": red_pixels,
                    "red_percentage": red_percentage,
                    "effective": abs(red_percentage - expected_red_percentage) < 15
                })
        
        return results
    
    def interactive_calibration(self):
        """Calibración interactiva con GUI"""
        print("🎨 CALIBRADOR INTERACTIVO DE COLORES")
        print("=" * 60)
        
        # Verificar si hay imágenes de muestra
        sample_dir = "data/calibration_samples"
        if not os.path.exists(sample_dir):
            print(f" No hay directorio de muestras: {sample_dir}")
            print(" Crea el directorio y añade imágenes de mesas PokerStars")
            return
        
        # Buscar imágenes
        images = []
        for ext in ['*.png', '*.jpg', '*.jpeg']:
            images.extend(os.path.join(sample_dir, f) for f in os.listdir(sample_dir) 
                         if f.lower().endswith(ext.replace('*', '')))
        
        if not images:
            print(" No hay imágenes de calibración")
            print(" Captura algunas imágenes de mesas PokerStars y guárdalas en data/calibration_samples/")
            return
        
        print(f" Imágenes encontradas: {len(images)}")
        
        # Preguntar tipo de mesa
        print("\n TIPOS DE MESA DISPONIBLES:")
        print("1. Classic (mesa clásica verde)")
        print("2. Dark (tema oscuro)")
        print("3. Stealth (tema minimalista)")
        print("4. Personalizado")
        
        choice = input("\n Selecciona tipo (1-4): ").strip()
        
        table_types = {1: "classic", 2: "dark", 3: "stealth", 4: "custom"}
        selected_type = table_types.get(int(choice), "classic")
        
        # Ejecutar calibración
        success = self.auto_calibrate(images[:5], selected_type)
        
        if success:
            print(f"\n Calibración completada para '{selected_type}'")
            print(" Los perfiles se guardaron en config/color_profiles.json")
            
            # Probar calibración
            test_results = self.test_on_samples(images[:3])
            
            print("\n RESULTADOS DE PRUEBA:")
            for result in test_results:
                status = "" if result["effective"] else ""
                print(f"   {status} {result['image']:20} {result['profile']:10} {result['red_percentage']:5.1f}% rojo")
        
        return success

def main():
    """Función principal del optimizador de color"""
    optimizer = ColorOptimizer()
    
    print(" OPTIMIZADOR DE DETECCIÓN DE COLOR - POKER COACH PRO")
    print("=" * 70)
    
    print("\n OPCIONES:")
    print("1. Calibración interactiva")
    print("2. Probar perfiles existentes")
    print("3. Ver perfiles guardados")
    print("4. Crear muestras de calibración")
    
    choice = input("\n Selecciona opción (1-4): ").strip()
    
    if choice == "1":
        optimizer.interactive_calibration()
    elif choice == "2":
        # Buscar imágenes de prueba
        test_dir = "data/calibration_samples"
        if os.path.exists(test_dir):
            images = []
            for ext in ['*.png', '*.jpg', '*.jpeg']:
                images.extend(os.path.join(test_dir, f) for f in os.listdir(test_dir) 
                             if f.lower().endswith(ext.replace('*', '')))
            
            if images:
                results = optimizer.test_on_samples(images[:5])
                
                print("\n RESULTADOS DE PRUEBA:")
                print("-" * 60)
                for result in results:
                    status = "" if result["effective"] else " "
                    print(f"{status} {result['image']:25} {result['profile']:12} {result['red_percentage']:6.1f}%")
            else:
                print(" No hay imágenes de prueba")
        else:
            print(f" Directorio no encontrado: {test_dir}")
    elif choice == "3":
        print("\n PERFILES DE COLOR GUARDADOS:")
        print("-" * 60)
        for profile_name, profile_data in optimizer.color_profiles.items():
            print(f"\n {profile_name}:")
            if "calibrated_at" in profile_data:
                print(f"   Calibrado: {profile_data['calibrated_at'][:19]}")
            print(f"   Rango 1: {profile_data.get('red_lower', [])} - {profile_data.get('red_upper', [])}")
            print(f"   Rango 2: {profile_data.get('red_lower2', [])} - {profile_data.get('red_upper2', [])}")
    elif choice == "4":
        create_calibration_samples()
    else:
        print(" Opción no válida")

def create_calibration_samples():
    """Crear muestras de calibración"""
    print("\n CREANDO MUESTRAS DE CALIBRACIÓN")
    print("=" * 60)
    
    # Crear directorio
    sample_dir = "data/calibration_samples"
    os.makedirs(sample_dir, exist_ok=True)
    
    print(" Este script te ayudará a capturar imágenes de diferentes mesas PokerStars")
    print(" Necesitas tener PokerStars abierto y configurado")
    
    import pyautogui
    import time
    
    input("\n Prepara PokerStars y presiona Enter para comenzar...")
    
    count = 0
    try:
        while True:
            print(f"\n Captura #{count + 1}")
            print("   Asegúrate de que la mesa sea visible...")
            
            # Contar regresivo
            for i in range(3, 0, -1):
                print(f"   Capturando en {i}...")
                time.sleep(1)
            
            # Capturar pantalla
            screenshot = pyautogui.screenshot()
            
            # Guardar
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(sample_dir, f"table_{timestamp}.png")
            screenshot.save(filename)
            
            print(f"    Guardado: {filename}")
            count += 1
            
            # Preguntar si continuar
            if count >= 5:
                print("\n Capturar otra imagen? (s/n): ")
                if input().strip().lower() != 's':
                    break
            else:
                print("   Esperando 2 segundos...")
                time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n Captura interrumpida")
    
    print(f"\n Se capturaron {count} imágenes en {sample_dir}")
    print(" Ahora puedes usar la calibración interactiva")

if __name__ == "__main__":
    main()
