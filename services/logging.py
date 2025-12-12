# Configura el sistema de logs (registros) de la aplicación para que se muestren en la consola con un formato específico (hora, nivel, mensaje).
import logging

logger = logging.getLogger("rag_api")
logger.setLevel(logging.INFO)

if not logger.handlers:
    h = logging.StreamHandler()
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    h.setFormatter(fmt)
    logger.addHandler(h)
