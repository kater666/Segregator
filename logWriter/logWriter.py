import logging

LOG_FILENAME = 'TC3268_1032.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

for i in range(0, 100):
    logging.debug("THIS IS RANDOM LINE THAT CAN APPEAR IN FILELOG.")

logging.info("Test case: 'ZSUBUNTU_TEST_MG_46' result: failed'")

for j in range(0, 25):
    logging.debug("THIS IS RANDOM LINE THAT CAN APPEAR IN FILELOG.")
