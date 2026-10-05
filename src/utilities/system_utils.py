import csv
from datetime import datetime
from pathlib import Path

from classes.order import Order

def read_orders_from_csv(path: str | Path) -> list[Order]:
	'''Read typed Order objects from a CSV file with an Order header row.'''
	with Path(path).open(newline='', encoding='utf-8') as csv_file:
		rows = csv.DictReader(csv_file)
		return [
			Order(
				order_id=row['id'],
				user_id=row['user_id'],
				delivery_zone=int(row['delivery_zone']),
				timestamp=datetime.fromisoformat(row['timestamp']),
				weight=float(row['weight']),
				is_expedited=row['is_expedited'].lower() == 'true',
				is_fragile=row['is_fragile'].lower() == 'true',
				is_hazardous=row['is_hazardous'].lower() == 'true',
				is_perishable=row['is_perishable'].lower() == 'true',
			)
			for row in rows
		]
