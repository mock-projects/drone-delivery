from typing import SupportsIndex

from classes.order import Order
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
		self.orders: list[Order] = []

	def insert_order(self, order: Order, position: SupportsIndex):
		'''Adds the given Order to the Drone's list of Orders at a given position.'''
		self.orders.insert(position, order)

	def add_orders(self, *orders: Order):
		'''
		Adds multiple given Orders to the Drone's list of Orders.
		This assumes that each new order is added at the end of the list.
		'''
		for order in orders:
			self.insert_order(order, -1)

	def deliver_orders(self):
		'''
		Deliver all of the Orders attached to the Drone. If the Drone's battery dies
		during the trip, it will throw a DeliveryException.
		'''
		self.battery_level = self.run_trip(self.orders, False)
		if self.battery_level < 0:
			raise DeliveryException('Drone battery died during trip!')

	def run_trip(self, orders: list[Order], use_simulated_trip: bool) -> float:
		'''
		Delivers a list of Orders attached to the Drone, returning the battery
		charge level remaining on the Drone after delivery. Returns -1 if the
		Drone's battery dies during the trip, or on its way back to the
		warehouse.

		NOTE:
		If simulated_trip is true, this method simulates a trip,
		rather than actually sending the Drone out. This can be useful for
		determining whether the Drone would be able to complete a trip, given a
		particular list of orders.
		'''
		current_location: ZoneId = 0
		payload_weight = 0
		battery_level = 0
		for order in orders:
			payload_weight += order.weight

		if use_simulated_trip:
			# We'll be simulating the trip, so we can assume a fully charged drone
			battery_level = 100
		else:
			# Actually deliver the orders, using the drone's current charge
			battery_level = self.battery_level
			print('Headed out for delivery:')

		delivered_order_count = 0
		for order in orders:
			if not use_simulated_trip:
				print(
					f'  Delivering Order #{order.order_id}'
					+ f' to zone {order.delivery_zone}...'
				)

			# Update drone battery, payload weight, and previous desination after
			# delivering the order
			distance = distance_between(current_location, order.delivery_zone)
			battery_level -= self.get_battery_usage(payload_weight, distance)
			payload_weight -= order.weight
			current_location = order.delivery_zone

			# Exit the loop if the battery dies during the trip
			if battery_level < 0:
				return -1
			if not use_simulated_trip:
				order.was_delivered = True
				delivered_order_count += 1
				print('    Complete!')

		# If this is a real trip, remove delivered orders from the list
		if not use_simulated_trip:
			for _ in range(delivered_order_count):
				orders.pop(0)

		battery_level -= self.get_battery_usage(
			0, distance_between(current_location, 0)
		)

		if battery_level < 0:
			return -1
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
