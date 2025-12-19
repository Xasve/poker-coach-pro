import psutil, time, sys, os

print(" OPTIMIZADOR DE PERFORMANCE - POKER COACH PRO")
print("="*60)

def optimize_system():
    # Verificar recursos
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    print(f" RECURSOS DEL SISTEMA:")
    print(f"   CPU: {cpu_percent}% utilizado")
    print(f"   RAM: {memory.percent}% utilizado ({memory.used//1024//1024} MB)")
    
    # Recomendaciones basadas en recursos
    recommendations = []
    
    if cpu_percent > 80:
        recommendations.append("Reducir intervalo de captura a 2+ segundos")
        recommendations.append("Desactivar capturas de depuración")
    
    if memory.percent > 85:
        recommendations.append("Reducir calidad de imágenes capturadas")
        recommendations.append("Limitar caché del motor GTO")
    
    # Configuración optimizada
    optimized_config = {
        "capture_interval": 2.0 if cpu_percent > 70 else 1.5,
        "debug_save": False if memory.percent > 80 else True,
        "image_quality": "medium" if memory.percent > 75 else "high",
        "gto_cache_size": 50 if memory.percent > 70 else 100,
        "use_multiprocessing": cpu_percent < 60 and psutil.cpu_count() >= 4
    }
    
    print(f"\n CONFIGURACIÓN OPTIMIZADA:")
    for key, value in optimized_config.items():
        print(f"   {key}: {value}")
    
    if recommendations:
        print(f"\n RECOMENDACIONES:")
        for rec in recommendations:
            print(f"    {rec}")
    
    return optimized_config

if __name__ == "__main__":
    config = optimize_system()
    
    # Guardar configuración optimizada
    import json
    with open("config/optimized_settings.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"\n Configuración guardada: config/optimized_settings.json")
