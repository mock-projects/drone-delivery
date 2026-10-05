from classes.drone import DeliveryException, Drone

class DispatchServer:
	'''The warehouse server that handles order packaging and deliveries.'''

	def __init__(self):
		self.unpackaged_orders = []
		self.delivery_drone = Drone()
		self.payload_test_drone = Drone()

	def add_order(self, order):
		self.unpackaged_orders.append(order)

	def package_and_deliver_trips(self, better_trip):
		'''
		Uses build_trip (or build_better_trip) to organize the
		unpackaged Orders into a list of packaged trips.
		'''
		trips = []

		while self.unpackaged_orders:
			trip = []

			# Build a trip
			if better_trip:
				trip = self.build_better_trip()
			else:
				earliest_order = self.unpackaged_orders[0]
				trip = self.build_trip(earliest_order.get_delivery_zone())

			# Exit the loop if no orders are added to the trip
			if not trip:
				break

			for order in trip:
				self.unpackaged_orders.remove(order)

			trips.append(trip)

		self.deliver_orders(trips)

	def deliver_orders(self, trips):
		'''Uses the delivery_drone to deliver all of the packaged trips.'''
		while trips:
			trip = trips[0]
			for order in trip:
				self.delivery_drone.add_order(
					order, len(self.delivery_drone.get_orders())
				)
			try:
				trips.pop(0)
				self.delivery_drone.deliver_orders()  # Release the drone!
			except DeliveryException as e:
				print(e)
				return
			self.delivery_drone.recharge()

	def build_trip(self, zone):
		'''
		Returns a list of as many of the oldest unpackaged Orders in the zone as
		possible without the Drone's battery dying. Once an Order that can't be
		accommodated is encountered, any remaining capacity should be filled
		with other Orders destined for this same zone from heaviest to lightest
		(regardless of when the Order was placed).
		'''
		# TODO: Implement this function. See the README for details.
		return []

	def build_better_trip(self):
		'''Returns a trip that addresses some of our customer concerns.'''
		# TODO: Implement this function. See the README for details.
		return []
