#!/usr/bin/env python3
"""
Archivo: stealth_launcher.py
Ruta: scripts/stealth_launcher.py
Lanzador stealth para iniciar el Poker Coach de manera indetectable
"""

import os
import sys
import time
import random
import subprocess
import ctypes
import tempfile
import hashlib
from pathlib import Path

def is_admin():
    """Verificar si estamos ejecutando como administrador"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Relanzar como administrador"""
    if not is_admin():
        script = sys.argv[0]
        params = ' '.join([f'"{x}"' for x in sys.argv[1:]])
        
        # Relanzar como admin
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{script}" {params}', None, 1
        )
        sys.exit(0)

class StealthLauncher:
    """Lanzador stealth para el Poker Coach"""
    
    def __init__(self):
        self.temp_dir = None
        self.obfuscated_path = None
        self.original_path = os.path.abspath(sys.argv[0])
        
    def obfuscate_launcher(self):
        """Ofuscar el lanzador para evitar detección"""
        
        # Crear directorio temporal
        self.temp_dir = tempfile.mkdtemp(prefix="sys_")
        
        # Generar nombre aleatorio
        random_name = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        self.obfuscated_path = os.path.join(
            self.temp_dir, 
            f"{random_name}.exe"
        )
        
        # Copiar y ofuscar
        self.create_obfuscated_copy()
        
        return self.obfuscated_path
    
    def create_obfuscated_copy(self):
        """Crear copia ofuscada del ejecutable"""
        try:
            # Leer el ejecutable original
            with open(self.original_path, 'rb') as f:
                original_data = f.read()
            
            # Aplicar ofuscación simple (XOR)
            key = random.randint(1, 255)
            obfuscated_data = bytearray()
            for byte in original_data:
                obfuscated_data.append(byte ^ key)
            
            # Agregar stub de deofuscación
            stub = self.create_deobfuscation_stub(key)
            final_data = stub + obfuscated_data
            
            # Escribir archivo ofuscado
            with open(self.obfuscated_path, 'wb') as f:
                f.write(final_data)
            
            # Establecer atributos de archivo oculto
            ctypes.windll.kernel32.SetFileAttributesW(
                self.obfuscated_path, 
                0x02  # FILE_ATTRIBUTE_HIDDEN
            )
            
            print(f"[STEALTH] Launcher ofuscado creado en: {self.obfuscated_path}")
            
        except Exception as e:
            print(f"[STEALTH ERROR] Error ofuscando: {e}")
            self.obfuscated_path = self.original_path
    
    def create_deobfuscation_stub(self, key):
        """Crear stub de deofuscación"""
        # Stub simple que deofusca el resto del archivo
        # En implementación real sería más complejo
        stub = b'DECRYPT_STUB_' + str(key).encode()
        return stub
    
    def launch_with_stealth(self):
        """Lanzar con medidas stealth"""
        
        print("[STEALTH] Iniciando lanzamiento stealth...")
        
        # 1. Ofuscar lanzador
        launch_path = self.obfuscate_launcher()
        
        # 2. Crear proceso oculto
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        # 3. Argumentos de línea de comandos
        cmd_args = [sys.executable, "start_coach.py"]
        cmd_args.extend(sys.argv[1:])
        
        try:
            # 4. Lanzar proceso
            process = subprocess.Popen(
                cmd_args,
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW,
                cwd=os.path.dirname(self.original_path)
            )
            
            print(f"[STEALTH] Proceso lanzado con PID: {process.pid}")
            
            # 5. Limpiar rastros
            self.clean_traces(process.pid)
            
            return process
            
        except Exception as e:
            print(f"[STEALTH ERROR] Error lanzando: {e}")
            
            # Fallback a lanzamiento normal
            return self.launch_normal()
    
    def launch_normal(self):
        """Lanzamiento normal (fallback)"""
        cmd_args = [sys.executable, "start_coach.py"]
        cmd_args.extend(sys.argv[1:])
        
        return subprocess.Popen(
            cmd_args,
            cwd=os.path.dirname(self.original_path)
        )
    
    def clean_traces(self, pid):
        """Limpiar rastros del lanzamiento"""
        try:
            # Ocultar procesos relacionados
            self.hide_process_from_list(pid)
            
            # Limpiar logs temporales
            self.clean_temp_logs()
            
            # Modificar registros de evento
            self.clear_event_logs()
            
        except Exception as e:
            print(f"[STEALTH WARNING] Error limpiando rastros: {e}")
    
    def hide_process_from_list(self, pid):
        """Intentar ocultar proceso de listas"""
        # Técnica avanzada que requiere privilegios
        pass
    
    def clean_temp_logs(self):
        """Limpiar logs temporales"""
        temp_dir = tempfile.gettempdir()
        
        # Buscar y eliminar logs recientes
        for file in Path(temp_dir).glob("*poker*"):
            try:
                if file.is_file():
                    file.unlink()
            except:
                pass
    
    def clear_event_logs(self):
        """Limpiar registros de evento"""
        try:
            # Esto requiere privilegios de administrador
            pass
        except:
            pass
    
    def setup_persistence(self):
        """Configurar persistencia del sistema"""
        if not is_admin():
            print("[STEALTH] Se requieren privilegios de administrador para persistencia")
            return False
        
        try:
            # Crear entrada en registro para ejecución automática
            import winreg
            
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            key_name = "SystemMaintenance"
            
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                key_path,
                0, winreg.KEY_WRITE
            )
            
            winreg.SetValueEx(
                registry_key,
                key_name,
                0,
                winreg.REG_SZ,
                self.obfuscated_path or self.original_path
            )
            
            winreg.CloseKey(registry_key)
            
            print("[STEALTH] Persistencia configurada en registro")
            return True
            
        except Exception as e:
            print(f"[STEALTH ERROR] Error configurando persistencia: {e}")
            return False
    
    def remove_persistence(self):
        """Remover persistencia"""
        try:
            import winreg
            
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            key_name = "SystemMaintenance"
            
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                key_path,
                0, winreg.KEY_WRITE
            )
            
            try:
                winreg.DeleteValue(registry_key, key_name)
            except WindowsError:
                pass  # La clave no existe
            
            winreg.CloseKey(registry_key)
            
            print("[STEALTH] Persistencia removida")
            
        except Exception as e:
            print(f"[STEALTH ERROR] Error removiendo persistencia: {e}")

def main():
    """Función principal del lanzador stealth"""
    
    print("""
    ╔══════════════════════════════════════════════╗
    ║      POKER COACH PRO - STEALTH LAUNCHER      ║
    ║      Sistema anti-detección activado         ║
    ╚══════════════════════════════════════════════╝
    """)
    
    # Verificar argumentos
    if "--remove-persistence" in sys.argv:
        launcher = StealthLauncher()
        launcher.remove_persistence()
        return
    
    # Lanzar con stealth
    launcher = StealthLauncher()
    process = launcher.launch_with_stealth()
    
    # Configurar persistencia si se solicita
    if "--persistent" in sys.argv:
        launcher.setup_persistence()
    
    print("[STEALTH] Sistema iniciado en modo stealth")
    print("[STEALTH] Usa Ctrl+C en esta ventana para detener")
    
    try:
        # Mantener lanzador vivo
        while True:
            time.sleep(1)
            
            # Verificar si proceso hijo aún está vivo
            if process.poll() is not None:
                print("[STEALTH] Proceso hijo terminado. Saliendo...")
                break
                
    except KeyboardInterrupt:
        print("\n[STEALTH] Detenido por usuario")
        
        # Terminar proceso hijo
        process.terminate()
        process.wait(timeout=5)

if __name__ == "__main__":
    # Verificar si necesitamos elevar privilegios
    if "--admin" in sys.argv and not is_admin():
        run_as_admin()
    
    main()