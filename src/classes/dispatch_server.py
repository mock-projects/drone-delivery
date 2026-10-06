from datetime import datetime

from classes.drone import DeliveryException, Drone
from classes.order import Order
from classes.trip import Trip
from utilities.delivery_utils import bundle_orders_by_customer

class DispatchServer:
	'''The warehouse server that handles order packaging and deliveries.'''

	def __init__(self):
		self.pending_orders: list[Order] = []
		self.delivery_drone = Drone()

	def add_orders(self, *orders: Order):
		'''Adds one or many orders to the server.'''
		self.pending_orders.extend(orders)

	def package_and_deliver_trips(self, use_better_trip: bool):
		'''
		Uses build_trip (or build_better_trip) to organize the
		pending Orders into a list of packaged trips.
		'''
		trips: list[Trip] = []

		while self.pending_orders:
			trip = Trip()

			# Build a trip
			if use_better_trip:
				trip = self.build_better_trip()
			else:
				earliest_order = self.pending_orders[0]
				trip = self.build_trip(earliest_order.delivery_zone)

			# Exit the loop if no orders are added to the trip
			if not trip:
				break

			for order in trip:
				self.pending_orders.remove(order)

			trips.append(trip)

		self.deliver_orders(trips)

		print(f'\n{len(self.pending_orders)} Undelivered Orders:')
		for order in self.pending_orders:
			print('\t▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄')
			order.print_details()
			print('\t▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀')

	def deliver_orders(self, trips: list[Trip]):
		'''Uses the delivery_drone to process all drone trips.'''
		while trips:
			trip = trips[0]
			self.delivery_drone.add_orders_to_trip(*trip)
			try:
				trips.pop(0)
				self.delivery_drone.run_trip() # Release the drone!
			except DeliveryException as e:
				print(e)
				return
			self.delivery_drone.recharge_battery()

	def build_trip(self, zone: int) -> Trip:
		'''
		Returns a Trip object with as many oldest pending Orders in the zone as
		possible without the Drone's battery dying. Once an Order that can't be
		accommodated is encountered, any remaining capacity should be filled
		with other Orders destined for this same zone from heaviest to lightest
		(regardless of when the Order was placed).
		'''
		test_drone = Drone() # Create test drone.
		orders = [*self.pending_orders] # Copy unpackaged orders list.

		# First, filter our orders by zone.
		orders = filter(lambda x: x.delivery_zone == zone, orders)

		# Then sort by timestamp (oldest orders first).
		orders = sorted(orders, key=lambda x: x.timestamp)
		orders = test_drone.plan_trip(orders, exit_on_mismatch=True)

		# Next sort by order weight (heaviest orders first) and fill.
		orders = sorted(orders, key=lambda x: x.weight, reverse=True)
		orders = test_drone.plan_trip(orders, exit_on_mismatch=False)

		# Finally, return the trip.
		return test_drone.trip

	def build_better_trip(self) -> Trip:
		'''Returns a trip that addresses some of our customer concerns.'''

		def calc_expedited_ratio(bundle: list[Order]) -> float:
			'''Customers with a higher ratio of premium orders are served first.'''
			count = sum(order.is_expedited for order in bundle)
			total = len(bundle)
			if total == 0: return 0
			else: return count / total

		def is_perishable(bundle: list[Order]) -> bool:
			'''Customers with perishable orders are served with the highest priority.'''
			# This can be exploited in some cases.
			# For example, a customer can order an apple with a video game
			# to prioritize it.
			return any(order.is_perishable for order in bundle)

		test_drone = Drone() # Create test drone.
		orders = [*self.pending_orders] # Copy unpackaged orders list.

		# Sort our orders by timestamp (oldest orders first).
		orders = sorted(orders, key=lambda order: order.timestamp)

		# Create bundles of orders based on customer ID, and sort them.
		bundles = bundle_orders_by_customer(orders)
		bundles = list(bundles.values())
		bundles = sorted(
			bundles,
			key=lambda bundle: (
				# (1) Perishable items are prioritized above all else.
				not is_perishable(bundle),

				# (2) Premium expedited bundles are prioritize secondly.
				# We 'usually' expect all orders or no orders in a bundle to be premium,
				# but sometimes users subscribe or unsubscribe, impacting their ratio.
				# TODO: Could this cause a negative user experience for new subscribers?
				-calc_expedited_ratio(bundle),

				# (3) Tiebreakers (there should be many) are dealt with by timestamp.
				bundle[0].timestamp if bundle else datetime.max,
			),
		)

		# Flatten the matrix and fill the trip with this special sorted list.
		orders = sum(bundles, [])
		test_drone.plan_trip(orders)

		# Finally, get the orders, and clear the payload test drone.
		return test_drone.trip
