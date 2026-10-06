'''
This file stores some valuable utility functions for the drone warehouse
server, including a function that gets the distance between zones.
'''

from classes.user import UserId
from classes.zone import ZONE_DISTANCE_MATRIX, ZoneId

type Location = tuple[ZoneId, UserId | None]

# This represents the location of a warehouse. Our main warehouse is at zone 0.
# The UserId in this tuple is None, since a warehouse has no UserId.
WAREHOUSE_LOCATION: Location = (0, None)

def distance_between(origin_location: Location, destination_location: Location) -> float:
	'''
	Returns the distance in kilometers between the centers of the given
	origin and destination zones.
	If an invalid zone is provided, returns infinity.
	'''
	# Extract the location data.
	orig_zone, orig_user = origin_location
	dest_zone, dest_user = destination_location

	# Obtain the zone distance from the matrix.
	distance = ZONE_DISTANCE_MATRIX[orig_zone][dest_zone]
	if distance == None:
		return float('inf')

	# Add a small penalty if the orders deliver to the same zone, but different users.
	# This simulates the distance that a drone must travel between nearby addresses.
	# Note, the warehouse is marked with a user_id of `None`.
	# When a user_id is compared to `None`, it does still count for the penalty!
	if (orig_zone == dest_zone) and (orig_user != dest_user):
		distance += 1/2

	return distance
