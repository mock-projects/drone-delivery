from collections.abc import Iterator
from typing import SupportsIndex, overload

from classes.order import Order


class Trip:
	'''This trip object tracks a list orders, ensureing they have no conflicting tags.'''

	def __init__(self, *orders: Order):
		# This is a list of orders, ordered by which orders should be processed first.
		self.orders: list[Order] = []
		self.add_orders(*orders) # Immediately add given orders to this trip.

	def __iter__(self) -> Iterator[Order]:
		return iter(self.orders)

	def __len__(self):
		return len(self.orders)

	@overload
	def __getitem__(self, index: SupportsIndex) -> Order: ...

	@overload
	def __getitem__(self, index: slice) -> list[Order]: ...

	def __getitem__(self, index: SupportsIndex | slice) -> Order | list[Order]:
		return self.orders[index]

	@property
	def has_hazardous_orders(self):
		return any(order.is_hazardous for order in self)

	@property
	def has_fragile_orders(self):
		return any(order.is_fragile for order in self)

	def order_is_compatible(self, order: Order):
		'''Returns true if the order is compatible with the trip, depending on tags.'''
		# TODO: Build a method that accepts or rejects an order into a trip.
		return True

	def add_order(self, order: Order, position: SupportsIndex | None = None):
		'''
		Adds the given Order to the Drone's list of Orders at a given position.
		Throws an exception if the order was not compatible with the trip.
		'''
		if position is None:
			position = len(self)
		if self.order_is_compatible(order):
			self.orders.insert(position, order)
		else:
			raise ValueError('Order was not compatible with Trip!')

	def add_orders(self, *orders: Order):
		'''
		Adds multiple given Orders to the Trip.
		This assumes that each new order is added at the end of the trip.
		'''
		for order in orders:
			self.add_order(order)
