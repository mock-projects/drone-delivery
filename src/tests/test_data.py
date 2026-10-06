from pathlib import Path

from utilities.system_utils import read_orders_from_csv

_DATA_DIRECTORY = Path(__file__).parent.parent / 'data/'
BASIC_TEST_ORDERS = read_orders_from_csv(_DATA_DIRECTORY / 'basic-orders.csv')

BASIC_ORDER_1 = BASIC_TEST_ORDERS[0]
BASIC_ORDER_2 = BASIC_TEST_ORDERS[1]
OVERSIZE_ORDER = BASIC_TEST_ORDERS[2]
LIGHT_ORDER = BASIC_TEST_ORDERS[3]
MIDSIZE_ORDER = BASIC_TEST_ORDERS[4]
ZONE_5_ORDER = BASIC_TEST_ORDERS[5]
ZONE_12_ORDER = BASIC_TEST_ORDERS[6]
