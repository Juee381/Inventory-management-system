import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s | %(levelname)-8s [%(filename)s:%(funcName)s:lineno:%(lineno)-d] | %(message)-8s',
                    filename='logs.txt', datefmt='%d-%m-%Y %H:%M:%S', filemode='w')

logger = logging.getLogger('Inventory')
