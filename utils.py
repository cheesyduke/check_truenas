import logging

def setup_logging(debug_logging):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if debug_logging else logging.CRITICAL)
