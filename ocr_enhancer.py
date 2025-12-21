# ocr_enhancer.py - Mejora del sistema OCR con data augmentation
import cv2
import numpy as np
import os
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
import albumentations as A

class OCR_Enhancer:
    """Sistema de mejora del OCR con data augmentation"""
    
    def __init__(self):
        self.augmentations = self.get_augmentation_pipeline()
        self.dataset_stats = {}
    
    def get_augmentation_pipeline(self):
        """Crear pipeline de aumentación de datos"""
        return A.Compose([
            # Transformaciones geométricas
            A.Rotate(limit=15, border_mode=cv2.BORDER_CONSTANT, value=0, p=0.3),
            A.Perspective(scale=(0.01, 0.1), keep_size=True, p=0.2),
            A.Affine(scale=(0.9, 1.1), translate_percent=(-0.05, 0.05), p=0.3),
            
            # Transformaciones de color
            A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
            A.RandomGamma(gamma_limit=(80, 120), p=0.3),
            A.HueSaturationValue(hue_shift_limit=10, sat_shift_limit=20, val_shift_limit=10, p=0.3),
            
            # Ruido y desenfoque
            A.GaussianBlur(blur_limit=(1, 3), p=0.2),
            A.GaussNoise(var_limit=(10, 30), p=0.2),
            A.ISONoise(color_shift=(0.01, 0.05), intensity=(0.1, 0.3), p=0.2),
            
            # Calidad de imagen
            A.ImageCompression(quality_lower=85, quality_upper=95, p=0.2),
            A.Downscale(scale_min=0.5, scale_max=0.9, interpolation=cv2.INTER_LINEAR, p=0.2),
        ])
    
    def analyze_dataset(self, dataset_path):
        """Analizar distribución del dataset"""
        print(f" ANALIZANDO DATASET: {dataset_path}")
        
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        stats = {
            'total_images': 0,
            'by_suit': {suit: 0 for suit in suits},
            'by_value': {value: 0 for value in values},
            'suit_distribution': {},
            'value_distribution': {}
        }
        
        # Contar imágenes por categoría
        for suit in suits:
            suit_path = os.path.join(dataset_path, suit)
            if not os.path.exists(suit_path):
                continue
            
            for value in values:
                value_patterns = [
                    f"{value}*",
                    f"{value.lower()}*",
                    f"{value}_*"
                ]
                
                count = 0
                for pattern in value_patterns:
                    count += len(list(Path(suit_path).glob(pattern + ".png")))
                    count += len(list(Path(suit_path).glob(pattern + ".jpg")))
                
                if count > 0:
                    stats['by_suit'][suit] += count
                    stats['by_value'][value] += count
                    stats['total_images'] += count
        
        # Calcular distribuciones
        if stats['total_images'] > 0:
            for suit in suits:
                stats['suit_distribution'][suit] = (stats['by_suit'][suit] / stats['total_images']) * 100
            
            for value in values:
                stats['value_distribution'][value] = (stats['by_value'][value] / stats['total_images']) * 100
        
        self.dataset_stats = stats
        return stats
    
    def balance_dataset(self, source_path, target_path, target_count_per_class=50):
        """Balancear dataset usando data augmentation"""
        print(f"  BALANCEANDO DATASET")
        print(f"   Fuente: {source_path}")
        print(f"   Destino: {target_path}")
        print(f"   Objetivo: {target_count_per_class} por clase")
        
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        # Crear estructura de directorios
        os.makedirs(target_path, exist_ok=True)
        for suit in suits:
            os.makedirs(os.path.join(target_path, suit), exist_ok=True)
        
        augmented_count = 0
        
        for suit in suits:
            for value in values:
                # Buscar imágenes originales
                original_images = []
                suit_path = os.path.join(source_path, suit)
                
                if os.path.exists(suit_path):
                    patterns = [
                        f"{value}*.png", f"{value}*.jpg",
                        f"{value.lower()}*.png", f"{value.lower()}*.jpg",
                        f"{value}_*.png", f"{value}_*.jpg"
                    ]
                    
                    for pattern in patterns:
                        for img_path in Path(suit_path).glob(pattern):
                            original_images.append(str(img_path))
                
                if not original_images:
                    continue
                
                print(f"\n {value}{suit[0]}: {len(original_images)} originales")
                
                # Copiar originales
                for i, img_path in enumerate(original_images):
                    img = cv2.imread(img_path)
                    if img is None:
                        continue
                    
                    # Guardar original
                    new_name = f"{value}_{suit}_{i:03d}_original.png"
                    new_path = os.path.join(target_path, suit, new_name)
                    cv2.imwrite(new_path, img)
                
                # Calcular cuántas augmentaciones necesitamos
                needed = max(0, target_count_per_class - len(original_images))
                
                if needed > 0:
                    print(f"   Generando {needed} augmentaciones...")
                    
                    for aug_idx in range(needed):
                        # Seleccionar imagen base aleatoria
                        base_img_path = np.random.choice(original_images)
                        base_img = cv2.imread(base_img_path)
                        
                        if base_img is None:
                            continue
                        
                        # Aplicar augmentación
                        augmented = self.augmentations(image=base_img)
                        augmented_img = augmented['image']
                        
                        # Guardar imagen augmentada
                        new_name = f"{value}_{suit}_{aug_idx:03d}_augmented.png"
                        new_path = os.path.join(target_path, suit, new_name)
                        cv2.imwrite(new_path, augmented_img)
                        
                        augmented_count += 1
        
        print(f"\n Dataset balanceado creado")
        print(f"   Total augmentaciones: {augmented_count}")
        print(f"   Destino: {target_path}")
        
        # Analizar nuevo dataset
        new_stats = self.analyze_dataset(target_path)
        
        return new_stats
    
    def create_training_validation_split(self, dataset_path, validation_split=0.2):
        """Crear split entrenamiento/validación"""
        print(f"\n CREANDO SPLIT ENTRENAMIENTO/VALIDACIÓN")
        
        # Recopilar todas las imágenes
        all_images = []
        labels = []
        
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        value_to_idx = {v: i for i, v in enumerate(values)}
        suit_to_idx = {s: i for i, s in enumerate(suits)}
        
        for suit in suits:
            suit_path = os.path.join(dataset_path, suit)
            if not os.path.exists(suit_path):
                continue
            
            for value in values:
                # Buscar imágenes para este valor
                for ext in ['.png', '.jpg']:
                    pattern = f"{value}_*{ext}"
                    for img_path in Path(suit_path).glob(pattern):
                        # Crear label combinado (valor + palo)
                        label = value_to_idx[value] * 4 + suit_to_idx[suit]
                        
                        all_images.append(str(img_path))
                        labels.append(label)
        
        if not all_images:
            print(" No se encontraron imágenes")
            return None
        
        print(f"   Total imágenes: {len(all_images)}")
        print(f"   Classes únicas: {len(set(labels))}")
        
        # Crear split
        train_images, val_images, train_labels, val_labels = train_test_split(
            all_images, labels, test_size=validation_split, random_state=42, stratify=labels
        )
        
        print(f"   Entrenamiento: {len(train_images)} imágenes")
        print(f"   Validación: {len(val_images)} imágenes")
        
        # Guardar splits
        split_dir = "data/training_splits"
        os.makedirs(split_dir, exist_ok=True)
        
        with open(os.path.join(split_dir, "train_split.json"), 'w') as f:
            json.dump({
                "images": train_images,
                "labels": train_labels,
                "label_map": {str(i): v for i, v in enumerate(values)}
            }, f, indent=2)
        
        with open(os.path.join(split_dir, "val_split.json"), 'w') as f:
            json.dump({
                "images": val_images,
                "labels": val_labels,
                "label_map": {str(i): v for i, v in enumerate(values)}
            }, f, indent=2)
        
        print(f" Splits guardados en: {split_dir}")
        
        return {
            "train_count": len(train_images),
            "val_count": len(val_images),
            "total_classes": len(set(labels)),
            "split_dir": split_dir
        }
    
    def test_ocr_improvement(self, original_dataset, augmented_dataset):
        """Probar mejora del OCR"""
        print("\n PROBANDO MEJORA DEL OCR")
        print("=" * 60)
        
        # Analizar datasets
        orig_stats = self.analyze_dataset(original_dataset)
        aug_stats = self.analyze_dataset(augmented_dataset)
        
        print("\n COMPARACIÓN DE DATASETS:")
        print(f"{'Métrica':25} {'Original':>12} {'Aumentado':>12} {'Mejora':>10}")
        print("-" * 60)
        
        print(f"{'Total imágenes':25} {orig_stats['total_images']:12} {aug_stats['total_images']:12} {aug_stats['total_images'] - orig_stats['total_images']:10}")
        
        # Distribución por palo
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        for suit in suits:
            orig_pct = orig_stats['suit_distribution'].get(suit, 0)
            aug_pct = aug_stats['suit_distribution'].get(suit, 0)
            print(f"{'  ' + suit:25} {orig_pct:11.1f}% {aug_pct:11.1f}% {aug_pct - orig_pct:9.1f}%")
        
        return {
            "original": orig_stats,
            "augmented": aug_stats,
            "improvement": {
                "total_images": aug_stats['total_images'] - orig_stats['total_images'],
                "balance_score": self.calculate_balance_score(aug_stats)
            }
        }
    
    def calculate_balance_score(self, stats):
        """Calcular score de balance del dataset"""
        if stats['total_images'] == 0:
            return 0
        
        # Calcular varianza en la distribución
        suit_dist = list(stats['suit_distribution'].values())
        value_dist = list(stats['value_distribution'].values())
        
        suit_variance = np.var(suit_dist) if suit_dist else 100
        value_variance = np.var(value_dist) if value_dist else 100
        
        # Score ideal: baja varianza = más balanceado
        balance_score = 100 / (1 + suit_variance + value_variance)
        
        return min(100, balance_score * 10)

def main():
    """Función principal del mejorador OCR"""
    enhancer = OCR_Enhancer()
    
    print(" MEJORADOR OCR - POKER COACH PRO")
    print("=" * 70)
    
    # Verificar estructura
    dataset_path = "data/card_templates/pokerstars_real"
    if not os.path.exists(dataset_path):
        print(f" Dataset no encontrado: {dataset_path}")
        print(" Primero organiza tus templates con session_manager.py")
        return
    
    print("\n OPCIONES:")
    print("1. Analizar dataset actual")
    print("2. Balancear dataset con data augmentation")
    print("3. Crear split entrenamiento/validación")
    print("4. Probar augmentaciones en imágenes")
    
    choice = input("\n Selecciona opción (1-4): ").strip()
    
    if choice == "1":
        stats = enhancer.analyze_dataset(dataset_path)
        
        print(f"\n ESTADÍSTICAS DEL DATASET:")
        print(f"   Total imágenes: {stats['total_images']}")
        
        print(f"\n DISTRIBUCIÓN POR PALO:")
        for suit, count in stats['by_suit'].items():
            if count > 0:
                percentage = stats['suit_distribution'].get(suit, 0)
                print(f"   {suit:10} {count:4} imágenes ({percentage:5.1f}%)")
        
        print(f"\n SCORE DE BALANCE: {enhancer.calculate_balance_score(stats):.1f}/100")
        
        if stats['total_images'] < 100:
            print(f"\n  ADVERTENCIA: Dataset pequeño (<100 imágenes)")
            print(" Considera capturar más imágenes o usar data augmentation")
    
    elif choice == "2":
        target_path = "data/card_templates/augmented_dataset"
        target_count = int(input("Objetivo por clase (default 50): ") or "50")
        
        stats = enhancer.balance_dataset(dataset_path, target_path, target_count)
        
        print(f"\n Dataset balanceado creado")
        print(f"   Nuevo total: {stats['total_images']} imágenes")
        print(f"   Score de balance: {enhancer.calculate_balance_score(stats):.1f}/100")
        
        # Probar mejora
        comparison = enhancer.test_ocr_improvement(dataset_path, target_path)
        
    elif choice == "3":
        split_info = enhancer.create_training_validation_split(dataset_path)
        
        if split_info:
            print(f"\n Split creado exitosamente")
            print(f"   Entrenamiento: {split_info['train_count']} imágenes")
            print(f"   Validación: {split_info['val_count']} imágenes")
            print(f"   Classes: {split_info['total_classes']}")
    
    elif choice == "4":
        # Probar augmentaciones en una imagen de muestra
        sample_images = list(Path(dataset_path).glob("*/*.png"))[:1]
        
        if not sample_images:
            print(" No hay imágenes de muestra")
            return
        
        sample_path = str(sample_images[0])
        print(f"\n Probando augmentaciones en: {os.path.basename(sample_path)}")
        
        import matplotlib.pyplot as plt
        
        original = cv2.imread(sample_path)
        original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        
        # Crear subplots
        fig, axes = plt.subplots(2, 3, figsize=(12, 8))
        axes = axes.flatten()
        
        # Mostrar original
        axes[0].imshow(original)
        axes[0].set_title("Original")
        axes[0].axis('off')
        
        # Mostrar 5 augmentaciones
        for i in range(1, 6):
            augmented = enhancer.augmentations(image=original)['image']
            axes[i].imshow(augmented)
            axes[i].set_title(f"Augmentation {i}")
            axes[i].axis('off')
        
        plt.tight_layout()
        plt.show()
        
        print(" Augmentaciones generadas exitosamente")
    
    else:
        print(" Opción no válida")

if __name__ == "__main__":
    main()
