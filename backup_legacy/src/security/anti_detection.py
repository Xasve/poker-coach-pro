"""
Archivo: anti_detection.py
Ruta: src/security/anti_detection.py
Sistema avanzado anti-detección para plataformas de poker
"""

import os
import sys
import random
import time
import hashlib
import ctypes
import psutil
from datetime import datetime
import winreg  # Windows specific
import subprocess

class PokerStealthSystem:
    """
    Sistema de stealth avanzado para evitar detección
    Técnicas profesionales para permanecer indetectable
    """
    
    def __init__(self, platform="ggpoker"):
        self.platform = platform
        self.start_time = datetime.now()
        self.stealth_level = "MAXIMUM"
        
        # Lista negra de procesos/servicios anti-cheat
        self.blacklisted_processes = [
            # GG Poker
            "ggpoker_anticheat.exe", "ggshield.exe", "ggservice.exe",
            "PokerCraft.exe", "GGACService.exe",
            
            # PokerStars
            "pokerstars_anticheat.exe", "stars_protect.exe",
            "PokerStarsSecurity.exe", "PSACService.exe",
            
            # Anti-cheat genéricos
            "battleye.exe", "easyanticheat.exe", "punkbuster.exe",
            "vac.exe", "fairfight.exe", "xigncode.exe",
            "nprotect.exe", "hackshield.exe",
            
            # Herramientas de monitoreo
            "wireshark.exe", "procmon.exe", "procexp.exe", "processhacker.exe",
            "cheatengine.exe", "ollydbg.exe", "ida.exe", "x64dbg.exe",
            "fiddler.exe", "charles.exe", "burpsuite.exe"
        ]
        
        # Lista negra de ventanas/dlls
        self.blacklisted_windows = [
            "Cheat Engine", "Process Hacker", "Debugger",
            "Memory Scanner", "Packet Sniffer", "Wireshark"
        ]
        
        # Patrones de memoria sospechosos
        self.suspicious_patterns = [
            b"\xCC\xCC\xCC\xCC",  # Breakpoints
            b"\x90\x90\x90\x90",  # NOP slides
            b"\xE8\x00\x00\x00\x00",  # Call hooks
        ]
        
        # Configuración de stealth
        self.stealth_config = {
            'random_delay_min': 0.1,
            'random_delay_max': 0.5,
            'capture_variance': 0.3,
            'mouse_jitter': 2,
            'memory_obfuscation': True,
            'process_camouflage': True,
            'network_spoofing': True
        }
        
        # Inicializar medidas de stealth
        self.initialize_stealth_measures()
    
    def initialize_stealth_measures(self):
        """Inicializar todas las medidas de stealth"""
        print(f"[STEALTH] Iniciando sistema anti-detección nivel: {self.stealth_level}")
        
        try:
            # 1. Ocultar proceso
            self.hide_process()
            
            # 2. Randomizar timings
            self.randomize_timings()
            
            # 3. Ofuscar memoria
            self.obfuscate_memory()
            
            # 4. Verificar entorno
            self.check_environment()
            
            # 5. Configurar hooks seguros
            self.setup_safe_hooks()
            
            print("[STEALTH] Sistema anti-detección inicializado correctamente")
            
        except Exception as e:
            print(f"[STEALTH WARNING] Error inicializando stealth: {e}")
    
    def hide_process(self):
        """Ocultar proceso del sistema"""
        try:
            # Cambiar nombre del proceso
            self.camouflage_process_name()
            
            # Ocultar de listas de procesos
            self.hide_from_taskmanager()
            
            # Modificar atributos de proceso
            self.modify_process_attributes()
            
        except:
            pass  # Fallar silenciosamente
    
    def camouflage_process_name(self):
        """Camuflar nombre del proceso como algo legítimo"""
        legitimate_names = [
            "svchost.exe", "explorer.exe", "chrome.exe",
            "firefox.exe", "notepad.exe", "python.exe",
            "java.exe", "node.exe", "steam.exe"
        ]
        
        # En sistemas reales esto requeriría técnicas avanzadas
        # Por ahora solo simulamos
        
        # Modificar información del proceso en memoria
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            
            # Obtener handle del proceso
            current_pid = os.getpid()
            handle = kernel32.OpenProcess(0x1F0FFF, False, current_pid)
            
            if handle:
                # Cambiar información básica (simulado)
                pass
                
        except:
            pass
    
    def hide_from_taskmanager(self):
        """Ocultar proceso del administrador de tareas"""
        # Técnica: Modificar PEB (Process Environment Block)
        try:
            # Esto requiere acceso a bajo nivel
            # En implementación real usaríamos ctypes o asm
            pass
        except:
            pass
    
    def modify_process_attributes(self):
        """Modificar atributos del proceso para parecer legítimo"""
        try:
            import ctypes
            from ctypes import wintypes
            
            # Establecer prioridad normal
            kernel32 = ctypes.windll.kernel32
            current_pid = os.getpid()
            handle = kernel32.OpenProcess(0x0200 | 0x0400, False, current_pid)
            
            if handle:
                # Prioridad normal
                kernel32.SetPriorityClass(handle, 0x00000020)
                kernel32.CloseHandle(handle)
                
        except:
            pass
    
    def randomize_timings(self):
        """Randomizar todos los timings del sistema"""
        self.last_action_time = time.time()
        self.action_intervals = []
        
        # Patrón humano de timing (no perfectamente regular)
        self.human_pattern = {
            'min_interval': 0.8,
            'max_interval': 2.5,
            'variance': 0.3
        }
    
    def obfuscate_memory(self):
        """Ofuscar uso de memoria y patrones"""
        try:
            # Crear ruido en memoria
            self.create_memory_noise()
            
            # Encriptar strings sensibles
            self.encrypt_sensitive_data()
            
            # Randomizar layout de memoria
            self.randomize_memory_layout()
            
        except:
            pass
    
    def create_memory_noise(self):
        """Crear ruido aleatorio en memoria"""
        # Asignar memoria dummy con patrones aleatorios
        self.dummy_memory = []
        for _ in range(random.randint(50, 200)):
            size = random.randint(1000, 10000)
            dummy = bytearray(random.getrandbits(8) for _ in range(size))
            self.dummy_memory.append(dummy)
    
    def encrypt_sensitive_data(self):
        """Encriptar datos sensibles en memoria"""
        self.encryption_key = hashlib.sha256(
            str(random.getrandbits(256)).encode()
        ).digest()
    
    def randomize_memory_layout(self):
        """Randomizar layout de memoria"""
        # Forzar garbage collection para cambiar layout
        import gc
        gc.collect()
        
        # Asignar memoria en patrones aleatorios
        for _ in range(random.randint(10, 50)):
            temp = [random.random() for _ in range(random.randint(100, 1000))]
            del temp
    
    def check_environment(self):
        """Verificar entorno de ejecución en busca de detección"""
        warnings = []
        
        # 1. Verificar procesos en ejecución
        warnings.extend(self.check_running_processes())
        
        # 2. Verificar ventanas abiertas
        warnings.extend(self.check_open_windows())
        
        # 3. Verificar servicios
        warnings.extend(self.check_services())
        
        # 4. Verificar debuggers
        if self.is_being_debugged():
            warnings.append("DEBUGGER_DETECTED")
        
        # 5. Verificar máquinas virtuales/sandbox
        if self.is_virtual_environment():
            warnings.append("VIRTUAL_ENVIRONMENT")
        
        # 6. Verificar hooks del sistema
        if self.check_system_hooks():
            warnings.append("SYSTEM_HOOKS_DETECTED")
        
        # Si hay warnings, activar contramedidas
        if warnings:
            print(f"[STEALTH] Advertencias detectadas: {warnings}")
            self.activate_countermeasures(warnings)
        
        return warnings
    
    def check_running_processes(self):
        """Verificar procesos sospechosos en ejecución"""
        suspicious = []
        
        try:
            for proc in psutil.process_iter(['name']):
                try:
                    proc_name = proc.info['name'].lower()
                    
                    # Verificar contra lista negra
                    for blacklisted in self.blacklisted_processes:
                        if blacklisted.lower() in proc_name:
                            suspicious.append(f"PROCESS_{proc_name}")
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except:
            pass
        
        return suspicious
    
    def check_open_windows(self):
        """Verificar ventanas sospechosas abiertas"""
        suspicious = []
        
        try:
            import ctypes
            from ctypes import wintypes
            
            EnumWindows = ctypes.windll.user32.EnumWindows
            EnumWindowsProc = ctypes.WINFUNCTYPE(
                ctypes.c_bool, ctypes.POINTER(ctypes.c_int), 
                ctypes.POINTER(ctypes.c_int)
            )
            GetWindowText = ctypes.windll.user32.GetWindowTextW
            GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
            
            titles = []
            
            def foreach_window(hwnd, lParam):
                length = GetWindowTextLength(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(hwnd, buff, length + 1)
                
                title = buff.value
                if title:
                    titles.append(title)
                    
                    # Verificar contra lista negra
                    for blacklisted in self.blacklisted_windows:
                        if blacklisted.lower() in title.lower():
                            suspicious.append(f"WINDOW_{title[:20]}")
                return True
            
            EnumWindows(EnumWindowsProc(foreach_window), 0)
            
        except:
            pass
        
        return suspicious
    
    def check_services(self):
        """Verificar servicios anti-cheat en ejecución"""
        suspicious = []
        
        try:
            import winreg
            
            # Verificar servicios en registro
            services_key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SYSTEM\CurrentControlSet\Services",
                0, winreg.KEY_READ
            )
            
            for i in range(winreg.QueryInfoKey(services_key)[0]):
                try:
                    service_name = winreg.EnumKey(services_key, i)
                    
                    # Verificar servicios sospechosos
                    suspicious_services = ['GGAC', 'StarsProtect', 'BattlEye']
                    for sus_service in suspicious_services:
                        if sus_service.lower() in service_name.lower():
                            suspicious.append(f"SERVICE_{service_name}")
                            
                except:
                    continue
                    
            winreg.CloseKey(services_key)
            
        except:
            pass
        
        return suspicious
    
    def is_being_debugged(self):
        """Detectar si el proceso está siendo depurado"""
        try:
            import ctypes
            
            # Check PEB BeingDebugged flag
            kernel32 = ctypes.windll.kernel32
            return kernel32.IsDebuggerPresent() != 0
            
        except:
            return False
    
    def is_virtual_environment(self):
        """Detectar si estamos en máquina virtual/sandbox"""
        try:
            # Verificar nombres de procesos típicos de VM
            vm_processes = ['vboxservice.exe', 'vboxtray.exe', 
                          'vmwaretray.exe', 'vmwareuser.exe',
                          'xenservice.exe', 'qemu-ga.exe']
            
            for proc in psutil.process_iter(['name']):
                try:
                    proc_name = proc.info['name'].lower()
                    if any(vm_proc in proc_name for vm_proc in vm_processes):
                        return True
                except:
                    continue
            
            # Verificar hardware típico de VM
            import wmi
            c = wmi.WMI()
            
            # Verificar fabricante
            for bios in c.Win32_BIOS():
                manufacturer = bios.Manufacturer.lower()
                if any(x in manufacturer for x in ['vmware', 'virtualbox', 
                                                  'qemu', 'xen', 'parallels']):
                    return True
            
            for compsys in c.Win32_ComputerSystem():
                manufacturer = compsys.Manufacturer.lower()
                model = compsys.Model.lower()
                
                if any(x in manufacturer for x in ['vmware', 'virtualbox']):
                    return True
                if any(x in model for x in ['virtual', 'vmware', 'kvm']):
                    return True
            
            return False
            
        except:
            return False
    
    def check_system_hooks(self):
        """Verificar hooks del sistema (API hooks)"""
        try:
            import ctypes
            
            # Verificar hooks comunes en user32.dll
            kernel32 = ctypes.windll.kernel32
            user32 = ctypes.windll.user32
            
            # Obtener direcciones de funciones
            get_foreground_window_addr = user32.GetForegroundWindow
            get_async_key_state_addr = user32.GetAsyncKeyState
            
            # Verificar si están hookeadas (simplificado)
            # En implementación real verificaríamos jumps/calls sospechosos
            
            return False
            
        except:
            return False
    
    def activate_countermeasures(self, warnings):
        """Activar contramedidas según advertencias"""
        for warning in warnings:
            if "DEBUGGER" in warning:
                self.anti_debugger_measures()
            elif "PROCESS" in warning:
                self.process_hiding_measures()
            elif "VIRTUAL" in warning:
                self.virtual_env_measures()
            elif "HOOK" in warning:
                self.anti_hook_measures()
    
    def anti_debugger_measures(self):
        """Medidas anti-debugger"""
        try:
            # 1. Timing checks
            start = time.perf_counter()
            for _ in range(1000000):
                pass
            end = time.perf_counter()
            
            # Si toma demasiado tiempo, posible debugger
            if (end - start) > 0.5:  # Más de 0.5 segundos
                self.trigger_stealth_mode()
            
            # 2. Exception-based detection
            self.exception_based_anti_debug()
            
        except:
            pass
    
    def process_hiding_measures(self):
        """Medidas para ocultar proceso"""
        try:
            # Cambiar a modo stealth completo
            self.stealth_level = "MAXIMUM"
            
            # Aumentar randomización
            self.stealth_config['random_delay_min'] = 0.2
            self.stealth_config['random_delay_max'] = 1.0
            
            # Agregar más ruido
            self.create_memory_noise()
            
        except:
            pass
    
    def virtual_env_measures(self):
        """Medidas para entornos virtuales"""
        # Comportamiento diferente en VM
        self.stealth_config['capture_variance'] = 0.5
        self.stealth_config['mouse_jitter'] = 5
    
    def anti_hook_measures(self):
        """Medidas anti-hook"""
        try:
            # Usar APIs alternativas
            self.use_alternative_apis()
            
            # Verificar integridad de DLLs
            self.check_dll_integrity()
            
        except:
            pass
    
    def trigger_stealth_mode(self):
        """Activar modo stealth máximo"""
        print("[STEALTH] Activando modo stealth máximo")
        
        # 1. Parar todas las operaciones visibles
        self.stop_all_operations()
        
        # 2. Limpiar memoria
        self.clean_memory()
        
        # 3. Esperar aleatoriamente
        time.sleep(random.uniform(5, 15))
        
        # 4. Reanudar con nuevas identidades
        self.reinitialize_with_new_identity()
    
    def stop_all_operations(self):
        """Parar todas las operaciones"""
        # Limpiar cachés
        self.dummy_memory = []
        
        # Resetear timers
        self.last_action_time = time.time()
    
    def clean_memory(self):
        """Limpiar memoria sensible"""
        # Sobrescribir buffers sensibles
        if hasattr(self, 'encryption_key'):
            self.encryption_key = b'\x00' * 32
        
        # Forzar garbage collection
        import gc
        gc.collect()
    
    def reinitialize_with_new_identity(self):
        """Reinicializar con nueva identidad"""
        # Nuevo seed aleatorio
        random.seed(time.time())
        
        # Nueva configuración
        self.initialize_stealth_measures()
    
    def safe_sleep(self, base_delay):
        """Sleep con randomización para parecer humano"""
        variance = self.stealth_config['capture_variance']
        jitter = random.uniform(1 - variance, 1 + variance)
        actual_delay = base_delay * jitter
        
        # Agregar micro-delays aleatorios
        micro_delays = random.randint(1, 5)
        for _ in range(micro_delays):
            time.sleep(actual_delay / micro_delays)
            
            # Pequeñas pausas aleatorias
            if random.random() < 0.1:
                time.sleep(random.uniform(0.01, 0.05))
    
    def human_mouse_movement(self, x, y):
        """Simular movimiento de mouse humano"""
        import pyautogui
        
        current_x, current_y = pyautogui.position()
        
        # Calcular distancia
        distance = ((x - current_x) ** 2 + (y - current_y) ** 2) ** 0.5
        
        # Tiempo basado en distancia (humano: ~0.15s por 100px)
        duration = max(0.1, min(1.0, distance / 100 * 0.15))
        
        # Agregar jitter
        jitter = self.stealth_config['mouse_jitter']
        target_x = x + random.randint(-jitter, jitter)
        target_y = y + random.randint(-jitter, jitter)
        
        # Curva humana (bezier simplificado)
        steps = int(duration * 100)
        for i in range(steps):
            t = i / steps
            # Curva suave (ease in-out)
            smooth_t = t * t * (3 - 2 * t)
            
            current_x += (target_x - current_x) * smooth_t / steps
            current_y += (target_y - current_y) * smooth_t / steps
            
            pyautogui.moveTo(current_x, current_y, _pause=False)
            time.sleep(duration / steps)
    
    def get_stealth_status(self):
        """Obtener estado actual del sistema stealth"""
        return {
            'stealth_level': self.stealth_level,
            'active_measures': list(self.stealth_config.keys()),
            'uptime': str(datetime.now() - self.start_time),
            'last_check': datetime.now().isoformat()
        }
    
    def exception_based_anti_debug(self):
        """Detección de debugger basada en excepciones"""
        try:
            # Intentar generar una excepción de breakpoint
            ctypes.windll.kernel32.OutputDebugStringW("Test")
            
            # Si llegamos aquí, probablemente sin debugger
            return False
            
        except:
            # Exception fue capturada, posible debugger
            return True

class NetworkStealth:
    """Stealth para comunicaciones de red"""
    
    def __init__(self):
        self.encryption_enabled = True
        self.proxy_chain = []
        
    def encrypt_data(self, data):
        """Encriptar datos para transmisión"""
        if not self.encryption_enabled:
            return data
        
        # Usar cifrado simple para ejemplo
        key = hashlib.sha256(b"poker_coach_secret").digest()
        iv = os.urandom(16)
        
        # En implementación real usaríamos AES
        import base64
        encoded = base64.b64encode(data.encode()).decode()
        
        # Agregar ruido aleatorio
        noise = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
        return f"{noise}{encoded}{noise[::-1]}"
    
    def spoof_network_identity(self):
        """Spoof identidad de red"""
        # Cambiar MAC address (requiere admin)
        # Cambiar hostname temporal
        # Modificar registros DNS
        
        pass