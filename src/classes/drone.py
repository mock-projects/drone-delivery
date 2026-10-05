from typing import SupportsIndex

from classes.order import Order
from classes.trip import Trip
from classes.zone import ZoneId
from utilities.delivery_utils import distance_between

class Drone:
	'''
	A delivery drone.

	A Drone carries a list of Orders and delivers them to their intended
	destinations. Our Drones are electric, so we must ensure that a Drone's
	battery has enough charge to deliver all of its Orders and return safely
	to the warehouse before we send it out on a delivery trip.
	'''

	def __init__(self):
		self.battery_level: float = 100
		self.trip = Trip()

	def insert_order_into_trip(self, order: Order, position: SupportsIndex):
		'''Adds the given Order to the Drone's Trip at a given position.'''
		self.trip.add_order(order, position)

	def add_orders_to_trip(self, *orders: Order):
		'''
		Adds multiple given Orders to the Drone's Trip.
		This assumes that each new order is added at the end of the trip.
		'''
		self.trip.add_orders(*orders)

	def run_trip(self, simulated_trip: Trip | None = None) -> float:
		'''
		Delivers a list of Orders attached to the Drone, returning the battery
		charge level remaining on the Drone after delivery. Returns -1 if the
		Drone's battery dies during the trip, or on its way back to the
		warehouse.

		NOTE:
		If a simulated_trip is given, this method simulates a trip,
		rather than actually sending the Drone out. This can be useful for
		determining whether the Drone would be able to complete a trip, given a
		particular list of orders.

		NOTE:
		If a simulated_trip is not given and the Drone's battery dies during the
		trip, then it will throw a DeliveryException.
		'''
		# Determine whether this trip was simulated.
		use_simulated_trip = False
		trip = self.trip
		if simulated_trip is not None:
			use_simulated_trip = True
			trip = Trip(*simulated_trip)

		# Initialize drone payload weight.
		payload_weight = 0
		for order in trip:
			payload_weight += order.weight

		# Initialize drone battery levels.
		battery_level = 0
		if use_simulated_trip:
			# We'll be simulating the trip, so we can assume a fully charged drone
			battery_level = 100
		else:
			# Actually deliver the orders, using the drone's current charge
			battery_level = self.battery_level
			print('\nHeaded out for delivery:')

		# Initialize the warehouse location.
		warehouse_zone: ZoneId = 0
		current_zone = warehouse_zone

		# Deliver orders.
		for order in trip:
			if not use_simulated_trip:
				print('\t▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄')
				print('\t█ Delivering Order...')
				order.print_details()

			# Update drone battery, payload weight,
			# and previous desination after delivering the order.
			next_zone: ZoneId = order.delivery_zone
			distance = distance_between(current_zone, next_zone)
			battery_level -= self.get_battery_usage(payload_weight, distance)
			payload_weight -= order.weight

			# Update the current location with the next one.
			current_zone = next_zone

			# Exit the loop if the battery dies during the trip.
			if battery_level < 0 and not use_simulated_trip:
				raise DeliveryException
			if battery_level < 0:
				return -1
			if not use_simulated_trip:
				order.was_delivered = True
				print('\t█ ...Success!')
				print('\t▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀')

		final_stretch = distance_between(current_zone, warehouse_zone)
		battery_level -= self.get_battery_usage(0, final_stretch)

		if battery_level < 0 and not use_simulated_trip:
			raise DeliveryException
		if battery_level < 0:
			return -1
		if not use_simulated_trip:
			self.trip = Trip() # Clear the trip and prepare a new run.
		return battery_level

	def simulate_trip_with_added_order(
		self,
		new_order: Order,
		position: SupportsIndex
	) -> float:
		'''
		Uses run_trip() to calculate the resulting battery charge if the Drone were to
		deliver all of the Orders already in its Order list, plus the given new_order
		(which would be added to the Order list at the given position).
		'''
		# TODO: Implement this function. See the README for details.
		return -1

	def find_best_order_position(self, new_order: Order) -> SupportsIndex:
		'''
		Returns the index of the best position to add an Order to the Drone's
		existing Order list. The best position is the one where the Drone returns
		to the warehouse with the greatest remaining battery charge. If there are
		no positions where the Order can be added without the Drone failing its
		trip, returns -1.
		'''
		# TODO: Implement this function. See the README for details.
		return -1

	def recharge_battery(self):
		'''Sets the battery to full (100).'''
		self.battery_level = 100

	def get_battery_usage(self, weight, distance) -> float:
		'''
		Given a payload weight in grams and a distance in kilometers, returns
		the percent of the Drone's range that this flight would consume.

		A value of 1 indicates that the Drone's entire battery is consumed.
		'''
		empty_overhead = 512
		consumption_factor = 367.39
		return distance * (weight + empty_overhead) / consumption_factor

class DeliveryException(Exception):
	pass
