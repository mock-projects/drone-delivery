'''
This file stores some valuable utility functions for the drone warehouse
server, including a function that gets the distance between zones.
'''

from classes.zone import ZONE_DISTANCE_MATRIX, ZoneId

def distance_between(origin_zone: ZoneId, destination_zone: ZoneId) -> float:
	'''
	Returns the distance in kilometers between the centers of the given origin
	and destination zones. If an invalid zone is provided, returns infinity.
	'''
	distance = ZONE_DISTANCE_MATRIX[origin_zone][destination_zone]
	if distance != None: return distance
	return float('inf')
