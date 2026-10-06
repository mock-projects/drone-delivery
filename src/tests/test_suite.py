'''
A set of simple tests that you can use to help verify that your code is working
correctly.

These tests are not exhaustive and do not guarantee that your solutions are
fully correct. If you have time, add some tests of your own to help verify your
solutions.
'''

from classes.dispatch_server import DispatchServer
from classes.drone import Drone
from tests.test_data import (
	ADVANCED_ORDERS,
	BASIC_ORDER_1,
	BASIC_ORDER_2,
	LIGHT_ORDER,
	MIDSIZE_ORDER,
	OVERSIZE_ORDER,
	ZONE_12_ORDER,
	ZONE_5_ORDER
)

def run_tests():
	'''Runs all of the tests.'''
	print('\n~~~~~~~~~~~~~~~~~\n| Running Tests |\n~~~~~~~~~~~~~~~~~')

	# If you have time, add some tests of your own to help verify your solutions.

	# Task 1 tests
	print('\n~~~ Task 1: Drone Trip Simulations ~~~\n')
	test_simulate_trip_with_added_order()
	test_find_best_order_position()
	test_find_best_order_position_multizone()

	# Task 2 tests
	print('\n~~~ Task 2: Single-Zone Trips ~~~\n')
	test_build_trip()

	# Task 3 tests
	print('\n~~~ Task 3: Build Better Trip ~~~\n')
	test_build_better_trip()

def test_simulate_trip_with_added_order():
	'''Tests simulate_trip_with_added_order() with two orders.'''
	print('test_simulate_trip_with_added_order: ')
	test_drone = Drone()
	test_drone.add_orders_to_trip(BASIC_ORDER_1)

	battery_remaining = test_drone.simulate_trip_with_added_order(BASIC_ORDER_2, 1)

	correct_battery = 91.76896486023027
	if (battery_remaining == correct_battery):
		print('✅', battery_remaining, '\n')
	else:
		print('❌', battery_remaining, '\n')

def test_find_best_order_position():
	'''
	Tests find_best_order_position() with a single-zone delivery.
	The best position should be 0.
	'''
	print('test_find_best_order_position: ')
	test_drone = Drone()
	test_drone.add_orders_to_trip(BASIC_ORDER_1)

	best_position = test_drone.find_best_order_position(LIGHT_ORDER)

	if (best_position == 0):
		print('✅', 'best_position =', best_position, '\n')
	else:
		print('❌', 'best_position =', best_position, '\n')

def test_find_best_order_position_multizone():
	'''
	Tests test_find_best_order_position() with a multi-zone delivery.
	The best position should be 2.
	'''
	print('test_find_best_order_position_multizone: ')
	test_drone = Drone()
	test_drone.add_orders_to_trip(BASIC_ORDER_1, BASIC_ORDER_2, ZONE_12_ORDER)

	best_position = test_drone.find_best_order_position(ZONE_5_ORDER)

	if (best_position == 2):
		print('✅', 'best_position =', best_position, '\n')
	else:
		print('❌', 'best_position =', best_position, '\n')

def test_build_trip():
	'''
	Tests build_trip(). It should add orders from the given zone,
	based first on timestamp, then weight.
	'''
	print('test_build_trip: ')
	dispatch_server = DispatchServer()
	dispatch_server.add_orders(
		ZONE_5_ORDER,
		BASIC_ORDER_1,
		LIGHT_ORDER,
		MIDSIZE_ORDER,
		OVERSIZE_ORDER,
		BASIC_ORDER_2,
	)

	trip = dispatch_server.build_trip(zone=1)

	# Usually, new orders in the same zone are added to the beginning of the list
	expected_sort01 = [
		LIGHT_ORDER,
		MIDSIZE_ORDER,
		BASIC_ORDER_2,
		BASIC_ORDER_1,
	]

	# But it's okay if your orders were added to the end of the list
	expected_sort02 = [
		BASIC_ORDER_1,
		BASIC_ORDER_2,
		MIDSIZE_ORDER,
		LIGHT_ORDER,
	]

	# Compare every order
	either_match = (trip.orders == expected_sort01) or (trip.orders == expected_sort02)

	if either_match:
		print('✅', 'Trip built correctly.\n')
	else:
		print('❌', 'Trip built in wrong order.\n')

def test_build_better_trip():
	'''
	Tests build_better_trip() with a richer mix of perishable,
	fragile, hazardous, and expedited bundles.
	The trip should include a subset of the available orders, never duplicates,
	and should prioritize the most urgent bundle ordering rules.
	'''
	print('test_build_better_trip: ')
	dispatch_server = DispatchServer()
	dispatch_server.add_orders(*ADVANCED_ORDERS)

	trip = dispatch_server.build_better_trip()
	trip_ids = [order.order_id for order in trip]
	all_ids = {order.order_id for order in ADVANCED_ORDERS}

	# The trip should only contain valid orders from the test set and should not
	# contain duplicates.
	if not trip:
		print('❌', 'No trip data.\n')
		return
	if len(trip_ids) != len(set(trip_ids)):
		print('❌', 'Duplicate order IDs were used.\n')
		return
	if any(order_id not in all_ids for order_id in trip_ids):
		print('❌', 'Orphaned order IDs were found.\n')
		return

	# The first bundle should still include at least one is_perishable or premium item.
	first_order = trip[0]
	if not (
		first_order.is_expedited or
		first_order.is_perishable or
		first_order.is_fragile or
		first_order.is_hazardous
	):
		print('❌', 'A special item tag should be prioritized.\n')
		return

	print('✅', 'No issues found with trip.\n')
