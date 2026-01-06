from satelite import Satelite
from estacion import EstacionTerrena
import threading
# ============================================================================
# MAIN.PY - Ejecución
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "satelite":
        satelite = Satelite(duracion_pass=120)  # 2 minutos de ventana
        satelite.iniciar()
    else:
        estacion = EstacionTerrena()
        
        if estacion.conectar():
            t_recepcion = threading.Thread(
                target=estacion.recibir_telemetria,
                daemon=True
            )
            t_recepcion.start()
            estacion.menu_interactivo()
        else:
            print("No se pudo conectar")