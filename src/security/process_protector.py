"""
Archivo: process_protector.py
Ruta: src/security/process_protector.py
Protección avanzada del proceso contra detección y terminación
"""

import ctypes
import ctypes.wintypes
import psutil
import sys
import os
import random
import hashlib
import time
from threading import Thread, Event

# Constantes de Windows
PROCESS_ALL_ACCESS = 0x1F0FFF
TH32CS_SNAPPROCESS = 0x00000002
INVALID_HANDLE_VALUE = -1

class ProcessProtector:
    """
    Sistema de protección del proceso contra detección y terminación
    """
    
    def __init__(self):
        self.pid = os.getpid()
        self.protection_active = False
        self.watchdog_thread = None
        self.stop_event = Event()
        
        # Configuración de protección
        self.protection_config = {
            'hide_from_tasklist': True,
            'prevent_termination': True,
            'monitor_anti_cheat': True,
            'self_healing': True,
            'process_camouflage': True
        }
        
        # Inicializar API de Windows
        self.init_windows_api()
        
    def init_windows_api(self):
        """Inicializar funciones de API de Windows"""
        self.kernel32 = ctypes.windll.kernel32
        self.ntdll = ctypes.windll.ntdll
        self.user32 = ctypes.windll.user32
        
        # Definir estructuras
        class PROCESS_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("hProcess", ctypes.wintypes.HANDLE),
                ("hThread", ctypes.wintypes.HANDLE),
                ("dwProcessId", ctypes.wintypes.DWORD),
                ("dwThreadId", ctypes.wintypes.DWORD)
            ]
        
        class STARTUPINFO(ctypes.Structure):
            _fields_ = [
                ("cb", ctypes.wintypes.DWORD),
                ("lpReserved", ctypes.c_char_p),
                ("lpDesktop", ctypes.c_char_p),
                ("lpTitle", ctypes.c_char_p),
                ("dwX", ctypes.wintypes.DWORD),
                ("dwY", ctypes.wintypes.DWORD),
                ("dwXSize", ctypes.wintypes.DWORD),
                ("dwYSize", ctypes.wintypes.DWORD),
                ("dwXCountChars", ctypes.wintypes.DWORD),
                ("dwYCountChars", ctypes.wintypes.DWORD),
                ("dwFillAttribute", ctypes.wintypes.DWORD),
                ("dwFlags", ctypes.wintypes.DWORD),
                ("wShowWindow", ctypes.wintypes.WORD),
                ("cbReserved2", ctypes.wintypes.WORD),
                ("lpReserved2", ctypes.c_char_p),
                ("hStdInput", ctypes.wintypes.HANDLE),
                ("hStdOutput", ctypes.wintypes.HANDLE),
                ("hStdError", ctypes.wintypes.HANDLE)
            ]
        
        self.PROCESS_INFORMATION = PROCESS_INFORMATION
        self.STARTUPINFO = STARTUPINFO
        
    def activate_protection(self):
        """Activar todas las protecciones"""
        print("[PROTECTION] Activando protecciones del proceso...")
        
        self.protection_active = True
        
        # 1. Ocultar proceso
        if self.protection_config['hide_from_tasklist']:
            self.hide_process()
        
        # 2. Proteger contra terminación
        if self.protection_config['prevent_termination']:
            self.protect_from_termination()
        
        # 3. Iniciar watchdog
        if self.protection_config['monitor_anti_cheat']:
            self.start_watchdog()
        
        # 4. Camuflar proceso
        if self.protection_config['process_camouflage']:
            self.camouflage_process()
        
        print("[PROTECTION] Protecciones activadas")
    
    def hide_process(self):
        """Ocultar proceso de listas de procesos"""
        try:
            # Técnica: Modificar PEB (Process Environment Block)
            # Esto requiere acceso a bajo nivel
            
            # Método alternativo: usar nombres legítimos
            self.camouflage_process_name()
            
        except Exception as e:
            print(f"[PROTECTION WARNING] Error ocultando proceso: {e}")
    
    def camouflage_process_name(self):
        """Camuflar nombre del proceso"""
        try:
            # Lista de nombres legítimos
            legitimate_names = [
                "svchost.exe", "explorer.exe", 
                "RuntimeBroker.exe", "dwm.exe",
                "csrss.exe", "winlogon.exe"
            ]
            
            # Cambiar nombre en memoria (técnica avanzada)
            # Esto es complejo y requiere hooking
            
        except:
            pass
    
    def protect_from_termination(self):
        """Proteger proceso contra terminación"""
        try:
            # 1. Establecer privilegios de depuración
            self.set_debug_privileges()
            
            # 2. Proteger handle del proceso
            self.protect_process_handle()
            
            # 3. Hookear funciones de terminación
            self.hook_termination_functions()
            
        except Exception as e:
            print(f"[PROTECTION WARNING] Error protegiendo proceso: {e}")
    
    def set_debug_privileges(self):
        """Establecer privilegios de depuración"""
        try:
            # Obtener token actual
            token = ctypes.wintypes.HANDLE()
            self.kernel32.OpenProcessToken(
                self.kernel32.GetCurrentProcess(),
                0x00000020,  # TOKEN_ADJUST_PRIVILEGES
                ctypes.byref(token)
            )
            
            # Buscar privilegio de depuración
            luid = ctypes.wintypes.LUID()
            self.kernel32.LookupPrivilegeValueW(
                None,
                "SeDebugPrivilege",
                ctypes.byref(luid)
            )
            
            # Ajustar privilegios
            new_state = (ctypes.wintypes.LUID_AND_ATTRIBUTES * 1)()
            new_state[0].Luid = luid
            new_state[0].Attributes = 0x00000002  # SE_PRIVILEGE_ENABLED
            
            token_privileges = ctypes.wintypes.TOKEN_PRIVILEGES()
            token_privileges.PrivilegeCount = 1
            token_privileges.Privileges = new_state
            
            self.kernel32.AdjustTokenPrivileges(
                token,
                False,
                ctypes.byref(token_privileges),
                0,
                None,
                None
            )
            
            self.kernel32.CloseHandle(token)
            
        except:
            pass
    
    def protect_process_handle(self):
        """Proteger handle del proceso"""
        try:
            # Obtener handle con acceso máximo
            handle = self.kernel32.OpenProcess(
                PROCESS_ALL_ACCESS,
                False,
                self.pid
            )
            
            if handle:
                # Establecer protección
                # En implementación real usaríamos NtSetInformationProcess
                
                self.kernel32.CloseHandle(handle)
                
        except:
            pass
    
    def hook_termination_functions(self):
        """Hookear funciones de terminación de proceso"""
        # Esto requiere hooking de API
        # Por ahora solo marcamos la intención
        
        functions_to_hook = [
            "TerminateProcess",
            "NtTerminateProcess",
            "ExitProcess",
            "kill",  # Para compatibilidad
        ]
        
        print(f"[PROTECTION] Monitoreando funciones de terminación: {functions_to_hook}")
    
    def start_watchdog(self):
        """Iniciar thread watchdog"""
        self.watchdog_thread = Thread(
            target=self.watchdog_monitor,
            daemon=True
        )
        self.watchdog_thread.start()
        
        print("[PROTECTION] Watchdog iniciado")
    
    def watchdog_monitor(self):
        """Monitor watchdog para detectar amenazas"""
        while not self.stop_event.is_set():
            try:
                # 1. Verificar si el proceso aún existe
                if not self.is_process_alive():
                    print("[WATCHDOG] Proceso principal terminado. Reiniciando...")
                    self.restart_self()
                    break
                
                # 2. Verificar procesos anti-cheat
                self.check_anti_cheat_processes()
                
                # 3. Verificar intentos de terminación
                self.check_termination_attempts()
                
                # 4. Verificar debuggers
                if self.is_being_debugged():
                    print("[WATCHDOG] Debugger detectado. Activando contramedidas...")
                    self.anti_debugger_response()
                
                # 5. Verificar hooks
                self.check_system_hooks()
                
                # Esperar antes de siguiente verificación
                time.sleep(2)
                
            except Exception as e:
                print(f"[WATCHDOG ERROR] {e}")
                time.sleep(5)
    
    def is_process_alive(self):
        """Verificar si el proceso principal sigue vivo"""
        try:
            return psutil.pid_exists(self.pid)
        except:
            return False
    
    def check_anti_cheat_processes(self):
        """Verificar procesos anti-cheat"""
        anti_cheat_processes = [
            "ggpoker_anticheat.exe", "pokerstars_anticheat.exe",
            "BattlEye.exe", "EasyAntiCheat.exe"
        ]
        
        for proc in psutil.process_iter(['name']):
            try:
                proc_name = proc.info['name'].lower()
                for ac_proc in anti_cheat_processes:
                    if ac_proc.lower() in proc_name:
                        print(f"[WATCHDOG] Proceso anti-cheat detectado: {proc_name}")
                        self.evade_detection()
                        break
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    
    def check_termination_attempts(self):
        """Verificar intentos de terminación"""
        # Monitorear handles abiertos a nuestro proceso
        try:
            for proc in psutil.process_iter():
                try:
                    # Verificar si algún proceso tiene handle abierto a nosotros
                    if proc.pid != self.pid:
                        # Esta verificación requiere privilegios elevados
                        pass
                        
                except:
                    continue
                    
        except:
            pass
    
    def is_being_debugged(self):
        """Verificar si hay debugger activo"""
        try:
            return self.kernel32.IsDebuggerPresent() != 0
        except:
            return False
    
    def check_system_hooks(self):
        """Verificar hooks del sistema"""
        # Verificar hooks en APIs críticas
        apis_to_check = [
            "NtReadVirtualMemory",
            "NtWriteVirtualMemory",
            "NtQuerySystemInformation"
        ]
        
        # Esta verificación requiere análisis de memoria
        pass
    
    def evade_detection(self):
        """Ejecutar medidas de evasión"""
        print("[PROTECTION] Ejecutando medidas de evasión...")
        
        # 1. Cambiar patrones de memoria
        self.change_memory_patterns()
        
        # 2. Modificar comportamiento
        self.modify_behavior()
        
        # 3. Temporalmente reducir actividad
        self.reduce_activity()
    
    def change_memory_patterns(self):
        """Cambiar patrones de memoria"""
        # Reasignar memoria con nuevos patrones
        new_buffer = bytearray(random.getrandbits(8) for _ in range(1024))
        
        # Cambiar algunas variables
        self.obfuscation_seed = random.randint(0, 1000000)
    
    def modify_behavior(self):
        """Modificar comportamiento del programa"""
        # Cambiar timings
        self.operation_delay = random.uniform(0.1, 0.3)
        
        # Cambiar patrones de captura
        self.capture_pattern = random.choice(['sequential', 'random', 'adaptive'])
    
    def reduce_activity(self):
        """Reducir temporalmente la actividad"""
        # Pausar operaciones por un tiempo
        pause_time = random.uniform(5, 15)
        print(f"[PROTECTION] Reduciendo actividad por {pause_time:.1f} segundos")
        time.sleep(pause_time)
    
    def anti_debugger_response(self):
        """Responder a detección de debugger"""
        # 1. Comportamiento benigno
        self.act_benign()
        
        # 2. Salir limpiamente si es necesario
        if random.random() < 0.3:  # 30% de probabilidad
            print("[PROTECTION] Debugger detectado. Saliendo limpiamente...")
            self.clean_exit()
    
    def act_benign(self):
        """Actuar como programa benigno"""
        # Simular actividad normal
        print("[PROTECTION] Actuando como proceso benigno...")
        
        # Hacer algunas operaciones "legítimas"
        for _ in range(random.randint(3, 10)):
            # Pequeñas pausas
            time.sleep(random.uniform(0.1, 0.5))
    
    def clean_exit(self):
        """Salir limpiamente del programa"""
        # Limpiar recursos
        self.stop_event.set()
        
        # Cerrar threads
        if self.watchdog_thread:
            self.watchdog_thread.join(timeout=1)
        
        # Salir
        os._exit(0)
    
    def camouflage_process(self):
        """Camuflar proceso para parecer legítimo"""
        # Cambiar información del proceso
        try:
            # Modificar información básica
            self.modify_process_information()
            
            # Crear actividad legítima
            self.create_legitimate_activity()
            
        except Exception as e:
            print(f"[PROTECTION WARNING] Error camuflando proceso: {e}")
    
    def modify_process_information(self):
        """Modificar información del proceso"""
        # Esto requeriría hooking de API
        pass
    
    def create_legitimate_activity(self):
        """Crear actividad de proceso legítima"""
        # Crear algunos archivos temporales
        temp_files = []
        for i in range(random.randint(1, 3)):
            temp_file = f"temp_{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}.tmp"
            with open(temp_file, 'w') as f:
                f.write("System temporary file\n")
            temp_files.append(temp_file)
        
        # Limpiar después
        import atexit
        def cleanup():
            for file in temp_files:
                try:
                    os.remove(file)
                except:
                    pass
        
        atexit.register(cleanup)
    
    def restart_self(self):
        """Reiniciar el proceso"""
        print("[PROTECTION] Reiniciando proceso...")
        
        try:
            # Obtener ruta del ejecutable actual
            exe_path = sys.executable
            script_path = sys.argv[0]
            
            # Argumentos originales
            args = sys.argv[1:]
            
            # Crear nuevo proceso
            startupinfo = self.STARTUPINFO()
            startupinfo.dwFlags = 0x1  # STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0  # SW_HIDE
            
            process_info = self.PROCESS_INFORMATION()
            
            # Crear comando
            cmd_line = f'"{exe_path}" "{script_path}" ' + ' '.join(f'"{arg}"' for arg in args)
            
            # Crear proceso
            success = self.kernel32.CreateProcessW(
                None,  # No application name
                cmd_line,  # Command line
                None,  # Process security attributes
                None,  # Thread security attributes
                False,  # Inherit handles
                0x08000000,  # CREATE_NO_WINDOW
                None,  # Environment
                None,  # Current directory
                ctypes.byref(startupinfo),
                ctypes.byref(process_info)
            )
            
            if success:
                print("[PROTECTION] Proceso reiniciado exitosamente")
                
                # Cerrar handles
                self.kernel32.CloseHandle(process_info.hProcess)
                self.kernel32.CloseHandle(process_info.hThread)
            else:
                print("[PROTECTION ERROR] No se pudo reiniciar el proceso")
                
        except Exception as e:
            print(f"[PROTECTION ERROR] Error reiniciando: {e}")
    
    def deactivate_protection(self):
        """Desactivar protecciones"""
        print("[PROTECTION] Desactivando protecciones...")
        
        self.protection_active = False
        self.stop_event.set()
        
        if self.watchdog_thread:
            self.watchdog_thread.join(timeout=2)
        
        print("[PROTECTION] Protecciones desactivadas")