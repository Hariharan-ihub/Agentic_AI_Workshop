import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def log_phase(phase, data):
    logging.info(f"[{phase.upper()}] {data}")