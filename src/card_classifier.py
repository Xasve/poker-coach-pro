# card_classifier.py - Clasificador automático de cartas (VERSIÓN CORREGIDA)
import cv2
import numpy as np
import os
import json
import shutil
from pathlib import Path
from datetime import datetime

# Importar matplotlib condicionalmente (para evitar errores si no está instalado)
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("  Matplotlib no disponible. Los gráficos estarán desactivados.")

# Importar scikit-learn condicionalmente
try:
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("⚠️  scikit-learn no disponible. Clustering desactivado.")

class CardClassifier:
    """Clasificador automático de cartas"""
    
    def __init__(self, data_path="data/card_templates/auto_captured"):
        self.data_path = data_path
        self.sessions = self.find_sessions()
        
        # Mapeo de palos
        self.suit_colors = {
            'hearts': 'red',
            'diamonds': 'red',  
            'clubs': 'black',
            'spades': 'black'
        }
        
    def find_sessions(self):
        """Encontrar todas las sesiones de captura"""
        sessions = []
        if os.path.exists(self.data_path):
            for item in os.listdir(self.data_path):
                session_path = os.path.join(self.data_path, item)
                if os.path.isdir(session_path):
                    sessions.append({
                        "id": item,
                        "path": session_path,
                        "raw_captures": os.path.join(session_path, "raw_captures")
                    })
        
        print(f"📂 Sesiones encontradas: {len(sessions)}")
        return sessions
    
    def load_captured_cards(self, session_path):
        """Cargar cartas capturadas"""
        cards = []
        raw_path = os.path.join(session_path, "raw_captures")
        
        if not os.path.exists(raw_path):
            return cards
        
        for file in os.listdir(raw_path):
            if file.endswith('.png'):
                img_path = os.path.join(raw_path, file)
                json_path = img_path.replace('.png', '.json')
                
                img = cv2.imread(img_path)
                metadata = {}
                
                if os.path.exists(json_path):
                    with open(json_path, 'r') as f:
                        metadata = json.load(f)
                
                if img is not None:
                    cards.append({
                        "image": img,
                        "path": img_path,
                        "metadata": metadata,
                        "filename": file
                    })
        
        return cards
    
    def extract_color_features(self, image):
        """Extraer características de color"""
        if image is None or image.size == 0:
            return None
        
        # Convertir a HSV para detección de rojo
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Rangos para rojo (dos rangos por naturaleza circular de HSV)
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        
        # Máscaras para rojo
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        
        # Contar píxeles rojos
        red_pixels = cv2.countNonZero(mask_red)
        total_pixels = image.shape[0] * image.shape[1]
        red_ratio = red_pixels / total_pixels if total_pixels > 0 else 0
        
        # Características básicas de color
        mean_color = np.mean(image, axis=(0, 1))
        
        return {
            "red_ratio": float(red_ratio),
            "mean_b": float(mean_color[0]),
            "mean_g": float(mean_color[1]),
            "mean_r": float(mean_color[2]),
            "is_red_suit": red_ratio > 0.05  # Umbral
        }
    
    def classify_suit_simple(self, image):
        """Clasificación simple por color"""
        color_features = self.extract_color_features(image)
        
        if color_features is None:
            return "unknown"
        
        if color_features["is_red_suit"]:
            # Intentar diferenciar corazones vs diamantes
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            std_dev = np.std(gray)
            
            # Los corazones suelen tener más contraste interno
            if std_dev > 25:
                return "hearts"
            else:
                return "diamonds"
        else:
            # Tréboles vs picas
            mean_brightness = np.mean(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
            if mean_brightness > 100:
                return "clubs"
            else:
                return "spades"
    
    def auto_classify_session(self, session_id):
        """Clasificar automáticamente una sesión"""
        session = next((s for s in self.sessions if s["id"] == session_id), None)
        
        if not session:
            print(f"❌ Sesión no encontrada: {session_id}")
            return None
        
        print(f"\n🎯 CLASIFICANDO SESIÓN: {session_id}")
        
        # Cargar cartas
        cards = self.load_captured_cards(session["path"])
        
        if not cards:
            print("❌ No hay cartas para clasificar")
            return None
        
        # Clasificar cada carta
        results = []
        classified_count = 0
        
        for i, card in enumerate(cards):
            if i % 10 == 0:
                print(f"   Procesando... {i+1}/{len(cards)}", end='\r')
            
            # Clasificar palo
            suit = self.classify_suit_simple(card["image"])
            
            # Valor desconocido por ahora (requeriría OCR)
            value = "unknown"
            
            # Crear resultado
            result = {
                "filename": card["filename"],
                "suit": suit,
                "value": value,
                "confidence": 0.7,
                "features": self.extract_color_features(card["image"])
            }
            
            results.append(result)
            
            # Mover a carpeta correspondiente
            if self.move_to_classified_folder(card, suit, value):
                classified_count += 1
        
        print(f"\n✅ Clasificación completada: {classified_count}/{len(cards)} cartas")
        
        # Guardar resultados
        self.save_classification_results(results, session["path"])
        
        # Generar reporte si hay suficientes cartas
        if len(cards) >= 5 and SKLEARN_AVAILABLE:
            self.generate_clustering_report(session_id, cards)
        
        return results
    
    def move_to_classified_folder(self, card, suit, value):
        """Mover carta clasificada"""
        try:
            # Carpeta destino
            if value != "unknown":
                dest_folder = os.path.join("data/card_templates/pokerstars_real", 
                                          suit, value)
            else:
                dest_folder = os.path.join("data/card_templates/pokerstars_real", 
                                          suit)
            
            os.makedirs(dest_folder, exist_ok=True)
            
            # Nuevo nombre
            new_filename = f"{value}_{suit}_{card['filename']}"
            dest_path = os.path.join(dest_folder, new_filename)
            
            # Copiar archivo
            shutil.copy2(card["path"], dest_path)
            
            # Copiar metadata
            metadata_src = card["path"].replace('.png', '.json')
            metadata_dest = dest_path.replace('.png', '.json')
            
            if os.path.exists(metadata_src):
                shutil.copy2(metadata_src, metadata_dest)
            
            return True
        except Exception as e:
            print(f"❌ Error moviendo {card['filename']}: {e}")
            return False
    
    def save_classification_results(self, results, session_path):
        """Guardar resultados"""
        output_path = os.path.join(session_path, "classification_results.json")
        
        summary = {
            "total_cards": len(results),
            "classified_date": str(datetime.now()),
            "suits_count": {},
            "cards": results[:50]  # Solo guardar primeras 50 para no hacer archivo muy grande
        }
        
        # Contar palos
        for result in results:
            suit = result["suit"]
            summary["suits_count"][suit] = summary["suits_count"].get(suit, 0) + 1
        
        with open(output_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📊 Resultados guardados: {output_path}")
        
        # Mostrar resumen
        print("\n📈 DISTRIBUCIÓN DE PALOS:")
        for suit, count in summary["suits_count"].items():
            percentage = (count / len(results)) * 100
            print(f"   {suit.upper():10} {count:3} ({percentage:.1f}%)")
    
    def generate_clustering_report(self, session_id, cards):
        """Generar reporte visual (opcional)"""
        if not SKLEARN_AVAILABLE or not MATPLOTLIB_AVAILABLE:
            print("⚠️  Clustering no disponible (scikit-learn o matplotlib faltante)")
            return
        
        if len(cards) < 5:
            return
        
        try:
            # Extraer características
            features = []
            for card in cards:
                feat = self.extract_color_features(card["image"])
                if feat:
                    features.append([
                        feat["red_ratio"],
                        feat["mean_r"],
                        feat["mean_g"],
                        feat["mean_b"]
                    ])
            
            if len(features) < 5:
                return
            
            # Clustering con K-Means
            kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
            clusters = kmeans.fit_predict(features)
            
            # Reducción de dimensionalidad para visualización
            pca = PCA(n_components=2)
            features_2d = pca.fit_transform(features)
            
            # Crear gráfico
            plt.figure(figsize=(10, 6))
            scatter = plt.scatter(features_2d[:, 0], features_2d[:, 1], 
                                c=clusters, cmap='viridis', s=50, alpha=0.6)
            
            plt.title(f'Clustering de Cartas - {session_id}')
            plt.xlabel('Componente Principal 1')
            plt.ylabel('Componente Principal 2')
            plt.colorbar(scatter)
            plt.grid(True, alpha=0.3)
            
            # Guardar
            session = next((s for s in self.sessions if s["id"] == session_id), None)
            if session:
                plot_path = os.path.join(session["path"], "clustering_report.png")
                plt.savefig(plot_path, dpi=120, bbox_inches='tight')
                plt.close()
                print(f"📈 Gráfico de clustering: {plot_path}")
            
        except Exception as e:
            print(f"⚠️  Error generando clustering: {e}")

def main():
    """Función principal simplificada"""
    print("🎴 CLASIFICADOR DE CARTAS - VERSIÓN SIMPLIFICADA")
    print("=" * 60)
    
    classifier = CardClassifier()
    
    if not classifier.sessions:
        print("❌ No hay sesiones de captura")
        print("\n💡 Primero ejecuta el capturador automático")
        return
    
    print("📂 Sesiones disponibles:")
    for i, session in enumerate(classifier.sessions[:10]):  # Mostrar solo 10
        raw_path = os.path.join(session["path"], "raw_captures")
        card_count = len([f for f in os.listdir(raw_path) 
                         if f.endswith('.png')]) if os.path.exists(raw_path) else 0
        
        print(f"   {i+1}. {session['id']} ({card_count} cartas)")
    
    if len(classifier.sessions) > 10:
        print(f"   ... y {len(classifier.sessions) - 10} más")
    
    try:
        choice = input("\nSelecciona número o 'todos' para clasificar todo: ")
        
        if choice.lower() == 'todos':
            for session in classifier.sessions:
                classifier.auto_classify_session(session["id"])
        else:
            idx = int(choice) - 1
            if 0 <= idx < len(classifier.sessions):
                session_id = classifier.sessions[idx]["id"]
                classifier.auto_classify_session(session_id)
            else:
                print("❌ Selección inválida")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
