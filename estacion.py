import threading
import json
import socket
import time
from pathlib import Path
# ============================================================================
# ESTACION_TERRENA.PY - Control desde Tierra
# ============================================================================

class ProcedimientoPasada:
    """Define el procedimiento automático durante una pasada"""
    ESPERA = "ESPERA"
    ADQUISICION = "ADQUISICION"
    MONITOREO = "MONITOREO"
    RESPUESTA_BATERIA = "RESPUESTA_BATERIA"
    PERDIDA_SENAL = "PERDIDA_SENAL"


class EstacionTerrena:
    def __init__(self, host='localhost', puerto=5001, archivo_historial='historial.json'):
        self.host = host
        self.puerto = puerto
        self.socket = None
        self.conectado = False
        self.historial = []
        self.archivo_historial = archivo_historial
        self.lock = threading.Lock()
        
        self.procedimiento = ProcedimientoPasada.ESPERA
        self.pasada_activa = False
        self.alertas = []
        
        self.cargar_historial()
    
    def cargar_historial(self):
        """Carga el historial desde JSON"""
        if Path(self.archivo_historial).exists():
            try:
                with open(self.archivo_historial, 'r') as f:
                    self.historial = json.load(f)
                print(f"[ESTACION] Historial cargado ({len(self.historial)} registros)")
            except Exception as e:
                print(f"[ESTACION] Error cargando historial: {e}")
    
    def guardar_historial(self):
        """Guarda el historial en JSON"""
        try:
            with open(self.archivo_historial, 'w') as f:
                json.dump(self.historial, f, indent=2)
        except Exception as e:
            print(f"[ESTACION] Error guardando historial: {e}")
    
    def conectar(self):
        """Conecta con el satélite"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.puerto))
            self.socket.settimeout(5)
            self.conectado = True
            print(f"[ESTACION] ✅ Conectada al satélite")
            self.procedimiento = ProcedimientoPasada.ADQUISICION
            return True
        except Exception as e:
            print(f"[ESTACION] ❌ Error conectando: {e}")
            return False
    
    def enviar_comando(self, comando):
        """Envía un comando"""
        if not self.conectado:
            return False
        
        try:
            self.socket.send(comando.encode('utf-8'))
            respuesta = self.socket.recv(1024).decode('utf-8')
            return respuesta == "OK"
        except:
            return False
    
    def procesar_telemetria(self, telem):
        """Procesa telemetría y ejecuta procedimiento de pasada"""
        with self.lock:
            self.historial.append(telem)
        
        # Estado de batería
        estado_bat = telem['bateria_estado']
        bateria = telem['bateria']
        temp = telem['temperatura']
        
        # PROCEDIMIENTO DE MONITOREO DURANTE PASADA
        if self.procedimiento == ProcedimientoPasada.ADQUISICION:
            print(f"\n[PROCEDIMIENTO] Fase 1: ADQUISICION")
            print(f"                Señal adquirida OK")
            self.procedimiento = ProcedimientoPasada.MONITOREO
            time.sleep(1)
        
        # Mostrar telemetría
        self._mostrar_telemetria(telem)
        
        # MONITOREO Y RESPUESTA AUTOMATICA
        if self.procedimiento == ProcedimientoPasada.MONITOREO:
            # Verificar criticidad
            if estado_bat == "CRITICA" or estado_bat == "SUPERVIVENCIA":
                print(f"\n⚠️  ALERTA DE BATERIA: {estado_bat}")
                self.procedimiento = ProcedimientoPasada.RESPUESTA_BATERIA
                self._ejecutar_respuesta_bateria_baja(telem)
            
            elif temp > 60:
                print(f"\n🔥 ALERTA DE TEMPERATURA: {temp}°C")
                print("[PROCEDIMIENTO] ABORTANDO operaciones")
                self.enviar_comando("PAYLOAD_OFF")
            
            elif bateria >= 30 and temp < 60:
                # Condiciones NOMINALES - activar payload
                if telem['payload'] == False and telem['estado'] == "STANDBY":
                    print(f"\n[PROCEDIMIENTO] Condiciones OK")
                    time.sleep(1)
        # Guardar periódicamente
        if telem['timestamp'] % 10 == 0:
            self.guardar_historial()
    
    def _mostrar_telemetria(self, telem):
        """Muestra telemetría formateada"""
        bat = telem['bateria']
        bat_bar = "█" * int(bat/5) + "░" * (20 - int(bat/5))
        
        temp = telem['temperatura']
        temp_bar = "█" * int(temp/3) + "░" * (20 - int(temp/3))
        
        payload_str = "🟢 ON" if telem['payload'] else "⚫ OFF"
        
        print(f"  [{telem['timestamp']:3}] {telem['estado']:8} | Payload {payload_str} | "
              f"Datos: {telem['datos_pendientes_mb']}MB")
        print(f"  Bat:  {bat_bar} {bat:5.1f}% ({telem['bateria_estado']})")
        print(f"  Temp: {temp_bar} {temp:5.1f}°C")
    
    def _ejecutar_respuesta_bateria_baja(self, telem):
        """Procedimiento automático ante batería baja"""
        print(f"\n[PROCEDIMIENTO] Fase 3: RESPUESTA A BATERIA BAJA")
        print(f"[PROCEDIMIENTO] Detener carga de datos")
        self.enviar_comando("PAYLOAD_OFF")
        
        print(f"[PROCEDIMIENTO] Confirmar estado SAFE")
        self.enviar_comando("SET_MODE SAFE")
        
        print(f"[PROCEDIMIENTO] Guardando datos críticos...")
        time.sleep(2)
        
        print(f"[PROCEDIMIENTO] ⚠️  Se recomienda cambio a batería solar en próxima órbita")
    
    def mostrar_resumen_pasada(self):
        """Muestra resumen de la pasada"""
        if not self.historial:
            return
        
        ultimos = self.historial[-30:]
        
        print("\n" + "="*70)
        print("RESUMEN DE PASADA")
        print("="*70)
        
        bateria_inicial = ultimos[0]['bateria']
        bateria_final = ultimos[-1]['bateria']
        consumo = bateria_inicial - bateria_final
        
        temp_max = max(t['temperatura'] for t in ultimos)
        datos_descargados = ultimos[0]['datos_pendientes_mb'] - ultimos[-1]['datos_pendientes_mb']
        print(f"Batería:      {bateria_inicial:.1f}% → {bateria_final:.1f}% (consumo: {consumo:.1f}%)")
        print(f"Temperatura:  Máx {temp_max:.1f}°C")
        print(f"Datos descargados:  {datos_descargados:.0f}MB")
        print(f"Duracion:     {len(ultimos) * 2}s")
    
    def menu_interactivo(self):
        """Interfaz manual"""
        print("\n" + "="*70)
        print("ESTACION TERRENA - OPERACIONES DE SATELITE")
        print("="*70)
        print("Comandos: SET_MODE <NOMINAL|SAFE>, PAYLOAD_ON/OFF, STATS, SALIR")
        print("="*70)
        
        while True:
            try:
                cmd = input("\n> ").strip()
                
                if cmd == "SALIR":
                    print("[ESTACION] Guardando historial...")
                    self.guardar_historial()
                    break
                elif cmd == "STATS":
                    self.mostrar_resumen_pasada()
                elif cmd.startswith("SET_MODE") or cmd.startswith("PAYLOAD"):
                    if self.conectado:
                        self.enviar_comando(cmd)
                    else:
                        print("[ESTACION] No conectada")
            except KeyboardInterrupt:
                self.guardar_historial()
                break
    
    def recibir_telemetria(self):
        """Recibe telemetría continuamente"""
        buffer = ""
        
        try:
            while self.conectado:
                try:
                    datos = self.socket.recv(4096).decode('utf-8')
                    if not datos:
                        self.conectado = False
                        break
                    
                    buffer += datos
                    while '\n' in buffer:
                        linea, buffer = buffer.split('\n', 1)
                        if linea.strip():
                            telem = json.loads(linea)
                            self.procesar_telemetria(telem)
                
                except socket.timeout:
                    continue
        
        except Exception as e:
            print(f"[ESTACION] Error: {e}")
        finally:
            self.conectado = False
            self.mostrar_resumen_pasada()
