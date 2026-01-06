import json
import socket
import time
import threading
from datetime import datetime
from enum import Enum

# ============================================================================
# SATELITE.PY - Simulación del Satélite con ventanas de paso o actividad
# ============================================================================

class EstadoBateria(Enum):
    """Estados de criticidad de batería"""
    NORMAL = "NORMAL"        # > 30%
    AVISO = "AVISO"          # 20-30%
    CRITICA = "CRITICA"      # 5-20%
    SUPERVIVENCIA = "SUPERVIVENCIA"  # < 5%


class Satelite:
    def __init__(self, host='localhost', puerto=5001, duracion_pass=120):
        self.host = host
        self.puerto = puerto
        self.socket = None
        self.duracion_pass = duracion_pass  # Segundos de ventana disponible
        
        # Estado interno
        self.estado = "INIT"
        self.bateria = 100
        self.temperatura = 25
        self.payload_activo = False
        self.timestamp = 0
        self.datos_a_descargar = 500  # MB de datos en buffer
        
        # Control de pasada
        self.conectado = False
        self.en_pasada = False
        self.tiempo_inicio_pasada = None
        self.lock = threading.Lock()
        
        # Historial de salud
        self.historial_salud = []
    
    def cambiar_estado(self, nuevo_estado):
        """Cambia el estado del satélite"""
        estados_validos = ["INIT", "STANDBY", "NOMINAL", "SAFE"]
        if nuevo_estado in estados_validos:
            with self.lock:
                self.estado = nuevo_estado
            print(f"[SATELITE] Estado cambiado a: {nuevo_estado}")
            return True
        return False
    
    def obtener_estado_bateria(self):
        """Clasifica el estado de criticidad de la batería"""
        if self.bateria >= 30:
            return EstadoBateria.NORMAL
        elif self.bateria >= 20:
            return EstadoBateria.AVISO
        elif self.bateria >= 5:
            return EstadoBateria.CRITICA
        else:
            return EstadoBateria.SUPERVIVENCIA
    
    def procesar_comando(self, comando):
        """Interpreta comandos desde la estación"""
        try:
            partes = comando.split()
            
            if partes[0] == "SET_MODE":
                nuevo_estado = partes[1]
                return self.cambiar_estado(nuevo_estado)
            
            elif partes[0] == "PAYLOAD_ON":
                if self.estado == "NOMINAL" and self.bateria > 20:
                    with self.lock:
                        self.payload_activo = True
                    print("[SATELITE] Payload encendido")
                    return True
                else:
                    razon = "no es NOMINAL" if self.estado != "NOMINAL" else "batería baja"
                    print(f"[SATELITE] ERROR: Payload no disponible ({razon})")
                    return False
            
            elif partes[0] == "PAYLOAD_OFF":
                with self.lock:
                    self.payload_activo = False
                print("[SATELITE] Payload apagado")
                return True
            
            return False
        except Exception as e:
            print(f"[SATELITE] Error procesando comando: {e}")
            return False
    
    def generar_telemetria(self):
        """Genera paquete de telemetría con simulación realista"""
        with self.lock:
            # Cambios de batería según estado
            consumo = 0
            if self.estado == "NOMINAL" and self.payload_activo:
                consumo = 2.5
            elif self.estado == "NOMINAL":
                consumo = 1.0
            elif self.estado == "SAFE":
                consumo = 0.3
            else:  # INIT, STANDBY
                consumo = 0.1
            
            self.bateria = max(0, self.bateria - consumo * (2/100))  # 2 seg
            
            # Cambios de temperatura
            if self.payload_activo:
                self.temperatura += 0.8
            else:
                self.temperatura -= 0.3
            
            self.temperatura = max(20, min(80, self.temperatura))
            
            # LÓGICA DE SEGURIDAD AUTOMÁTICA
            estado_bat = self.obtener_estado_bateria()
            
            # Respuesta ante batería crítica
            if estado_bat == EstadoBateria.CRITICA and self.estado != "SAFE":
                self.estado = "SAFE"
                self.payload_activo = False
                print("[SATELITE] ⚠️  ALERTA CRITICA: Batería baja, cambiando a SAFE")
            
            if estado_bat == EstadoBateria.SUPERVIVENCIA:
                self.payload_activo = False
                print("[SATELITE] 🔴 EMERGENCIA: Modo supervivencia activado")
            
            # Respuesta ante temperatura alta
            if self.temperatura > 60 and self.estado != "SAFE":
                self.estado = "SAFE"
                self.payload_activo = False
                print("[SATELITE] 🔥 ALERTA: Temperatura alta, cambiando a SAFE")
            
            # Descarga de datos si payload activo
            if self.payload_activo and self.datos_a_descargar > 0:
                self.datos_a_descargar -= 50  # MB/pass descargados
            
            telemetria = {
                "timestamp": self.timestamp,
                "datetime": datetime.now().isoformat(),
                "estado": self.estado,
                "bateria": round(self.bateria, 1),
                "bateria_estado": estado_bat.value,
                "temperatura": round(self.temperatura, 1),
                "payload": self.payload_activo,
                "datos_pendientes_mb": max(0, self.datos_a_descargar)
            }
            
            self.timestamp += 1
            self.historial_salud.append(telemetria)
            return telemetria
    
    def escuchar_comandos(self, conexion):
        """Escucha comandos de la estación"""
        try:
            while self.conectado and self.en_pasada:
                try:
                    datos = conexion.recv(1024).decode('utf-8')
                    if not datos:
                        break
                    
                    comando = datos.strip()
                    print(f"[SATELITE] Comando: {comando}")
                    resultado = self.procesar_comando(comando)
                    
                    respuesta = "OK" if resultado else "ERROR"
                    conexion.send(respuesta.encode('utf-8'))
                
                except socket.timeout:
                    continue
        except Exception as e:
            print(f"[SATELITE] Error escuchando: {e}")
        finally:
            pass
    
    def enviar_telemetria(self, conexion):
        """Envía telemetría durante la ventana de paso"""
        try:
            tiempo_elapsed = 0
            while self.conectado and self.en_pasada and tiempo_elapsed < self.duracion_pass:
                telem = self.generar_telemetria()
                mensaje = json.dumps(telem) + "\n"
                conexion.send(mensaje.encode('utf-8'))
                time.sleep(2)
                tiempo_elapsed += 2
            
            # Fin de la pasada
            self.en_pasada = False
            print(f"\n[SATELITE] 📡 FIN DE PASADA. Datos pendientes: {self.datos_a_descargar}MB")
        except Exception as e:
            print(f"[SATELITE] Error enviando telemetría: {e}")
    
    def simular_pasada(self):
        """Simula una ventana de paso del satélite"""
        print(f"\n[SATELITE] 🛰️  INICIO DE PASADA - Ventana disponible: {self.duracion_pass}s")
        print(f"           Batería: {self.bateria:.1f}% | Temperatura: {self.temperatura:.1f}°C")
        
        self.en_pasada = True
        self.tiempo_inicio_pasada = datetime.now()
    
    def iniciar(self):
        """Inicia el servidor TCP del satélite"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.puerto))
        self.socket.listen(1)
        
        print(f"[SATELITE] Esperando conexión en {self.host}:{self.puerto}...")
        print(f"[SATELITE] Ventana de paso: {self.duracion_pass} segundos")
        
        try:
            self.cambiar_estado("STANDBY")
            
            while True:
                # Esperar conexión de estación
                print("\n[SATELITE] Esperando estación terrena...")
                conexion, direccion = self.socket.accept()
                
                self.conectado = True
                conexion.settimeout(5)
                
                print(f"[SATELITE] Estación conectada desde {direccion}")
                
                # Simular pasada
                self.simular_pasada()
                
                # Threads para envío/recepción
                t_envio = threading.Thread(
                    target=self.enviar_telemetria,
                    args=(conexion,),
                    daemon=True
                )
                t_recepcion = threading.Thread(
                    target=self.escuchar_comandos,
                    args=(conexion,),
                    daemon=True
                )
                
                t_envio.start()
                t_recepcion.start()
                
                # Esperar a que termine la pasada
                t_envio.join()
                
                self.conectado = False
                self.en_pasada = False
                conexion.close()
                
                print("[SATELITE] Desconectado. Esperando próxima pasada...")
                time.sleep(5)  # Simular tiempo entre pasadas
        
        except KeyboardInterrupt:
            print("\n[SATELITE] Apagando...")
        finally:
            self.socket.close()
