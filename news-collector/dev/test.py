import logging

debug = False
logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(message)s")

if debug: logging.debug('This is a log message.')


print("EOP")