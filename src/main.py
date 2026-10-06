from classes.dispatch_server import DispatchServer
from tests.test_data import BASIC_ORDERS
from tests.test_suite import run_tests
from utilities.system_utils import create_argument_parser

def main():
	server = DispatchServer()
	server.add_orders(*BASIC_ORDERS)
	server.package_and_deliver_trips(use_better_trip=True)

def test():
	run_tests()

def print_intro():
	print('\nWelcome to the Drone Delivery codebase!')
	print('Start by reading through the README file for your instructions,')
	print('then familiarize yourself with the rest of the files in the codebase.')
	print('When you\'re ready, start tackling the TODOs in the codebase.\n')


if __name__ == '__main__':
	print_intro() # Print introductory text on-run.
	args = create_argument_parser().parse_args()
	if args.test: test()
	else: main()
