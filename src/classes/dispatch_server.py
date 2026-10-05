from classes.drone import DeliveryException, Drone
from classes.order import Order

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
		trips = []

		while self.pending_orders:
			trip = []

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

	def deliver_orders(self, trips: list[list[Order]]):
		'''Uses the delivery_drone to deliver all of the packaged trips.'''
		while trips:
			trip = trips[0]
			self.delivery_drone.add_orders(*trip)
			try:
				trips.pop(0)
				self.delivery_drone.deliver_orders()  # Release the drone!
			except DeliveryException as e:
				print(e)
				return
			self.delivery_drone.recharge_battery()

	def build_trip(self, zone: int) -> list[Order]:
		'''
		Returns a list of as many of the oldest pending Orders in the zone as
		possible without the Drone's battery dying. Once an Order that can't be
		accommodated is encountered, any remaining capacity should be filled
		with other Orders destined for this same zone from heaviest to lightest
		(regardless of when the Order was placed).
		'''
		# TODO: Implement this function. See the README for details.
		return []

	def build_better_trip(self) -> list[Order]:
		'''Returns a trip that addresses some of our customer concerns.'''
		# TODO: Implement this function. See the README for details.
		return []
