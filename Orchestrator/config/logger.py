import logging

def init_logging():
    "Initializes the main logger"
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logging.info("Logging initialized")