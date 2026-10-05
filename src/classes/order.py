from datetime import datetime

from classes.user import UserId
from classes.zone import ZoneId

type OrderId = str

class Order:
	'''
	An Order is a single user-purchased item to be delivered.

	We always try to bundle multiple orders together into a single delivery trip,
	to maximize efficiency.

	Note: An order's timestamp represents the time that the order was placed, not
	the time that it was first packaged and added to the DispatchServer, which
	could happen much later.
	'''

	def __init__(
		self,
		order_id: OrderId,
		user_id: UserId,
		delivery_zone: ZoneId,
		timestamp: datetime,
		weight: float,
		is_expedited: bool,
		is_fragile: bool,
		is_hazardous: bool,
		is_perishable: bool,
	):
		self.order_id: OrderId = order_id
		self.user_id: UserId = user_id
		self.delivery_zone: ZoneId = delivery_zone
		self.timestamp: datetime = timestamp
		self.weight: float = weight
		self.is_expedited: bool = is_expedited
		self.is_fragile: bool = is_fragile
		self.is_hazardous: bool = is_hazardous
		self.is_perishable: bool = is_perishable
		self.was_delivered: bool = False

	def __repr__(self):
		return (
			f'Order {self.order_id} at {self.timestamp} to {self.delivery_zone} '
			+ f'({self.weight}g)'
		)

	def print_details(self):
		'''Prints a formatted list of order details.'''
		print(
			f'\t█ - ORDER: #{self.order_id}.\n'
			f'\t█ - ZONE: {self.delivery_zone}\n'
			f'\t█ - USER: {self.user_id}\n'
			f'\t█ - DATE: {self.timestamp:%Y-%m-%d %H:%M}\n'
			f'\t█ - WEIGHT: {self.weight}\n'
			f'\t█ - TAGS: '
			f'\033[36m{'expedited ' if self.is_expedited else ''}\033[0m'
			f'\033[33m{'fragile ' if self.is_fragile else ''}\033[0m'
			f'\033[31m{'hazardous ' if self.is_hazardous else ''}\033[0m'
			f'\033[32m{'perishable ' if self.is_perishable else ''}\033[0m'
		)
