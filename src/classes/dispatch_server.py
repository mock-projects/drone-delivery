from classes.drone import DeliveryException, Drone
from classes.order import Order
from classes.trip import Trip

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
		# TODO: Implement this function. See the README for details.
		return Trip()
