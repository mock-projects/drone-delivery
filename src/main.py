from classes.dispatch_server import DispatchServer
from tests.test_data import BACKLOG_ORDERS
from tests.test_suite import run_tests
from utilities.system_utils import create_argument_parser

def main():
	server = DispatchServer()
	server.add_orders(*BACKLOG_ORDERS)
	server.package_and_deliver_trips(use_better_trip=True)

def test():
	run_tests()

if __name__ == '__main__':
	args = create_argument_parser().parse_args() # Get command-line args.
	if args.test: test()
	else: main()
