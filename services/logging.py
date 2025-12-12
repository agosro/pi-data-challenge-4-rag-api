# ========================================
# LOGGING - services/logging.py
# ========================================
# Configuración del sistema de logs
# Registra eventos importantes en la consola
# ========================================

# Importar el módulo logging de Python
import logging

# Crear un logger con nombre "rag_api"
# Un logger es como un "canal" para enviar mensajes de log
logger = logging.getLogger("rag_api")

# Establecer el nivel mínimo de logs a INFO
# Niveles (de menor a mayor): DEBUG < INFO < WARNING < ERROR < CRITICAL
# Con INFO, se mostrarán mensajes INFO, WARNING, ERROR y CRITICAL
logger.setLevel(logging.INFO)

# Verificar si el logger ya tiene handlers (para no duplicar)
if not logger.handlers:
    # Crear un handler que imprime en la consola (StreamHandler)
    h = logging.StreamHandler()
    
    # Crear un formateador para definir cómo se ven los mensajes
    # %(asctime)s = fecha y hora
    # %(levelname)s = nivel (INFO, ERROR, etc.)
    # %(message)s = el mensaje en sí
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    
    # Asignar el formateador al handler
    h.setFormatter(fmt)
    
    # Agregar el handler al logger
    logger.addHandler(h)

# Ahora otros archivos pueden importar y usar este logger:
# from services.logging import logger
# logger.info("Algo sucedió")  # Aparecerá en consola
