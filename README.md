# Task List
You may do these tasks in any order, but take note that they are listed in the order your team has prioritized completing them.

Reminder that you are NOT expected to complete all tasks.
You are expected to write clean, readable code.
Remember to add comments explaining what you were working on if you run out of time in the middle of a task.

## Task 1
**Drone Trip Simulations**

To determine if a trip is possible for a drone, we must check that the drone will not run out of battery during the trip.
This requires tracking the distance the drone travels and how much weight it is carrying at each point in the trip.
In [drone.py], implement the method with the prototype `simulate_trip_with_added_order(self, new_order, position)`.
This method should use `run_trip()` to simulate a trip with the given order added at the given position in the drone's order list, and return the resulting battery charge level.
Then, using that method as a helper, implement the method with the prototype `find_best_order_position(self, new_order)`.
This method should return the best position to add the `new_order` to the drone's current order list, to minimize battery usage.
If there is no position where the order can be added without the drone's battery failing, it should return -1.

## Task 2
**Single-Zone Trips**

In [dispatch_server.py], implement the method with the prototype `build_trip(self, zone)`.
This method returns a list of `orders` to be delivered on the next drone trip.
The returned list of `orders` should contain as many of the oldest pending `orders` in the zone as possible without exceeding the drone's range.
Once an order exceeds the drone's range, any remaining capacity should be filled with other orders destined for this same zone, from heaviest to lightest (regardless of when the order was placed).

Make use of the `payload_test_drone` to simulate trips to determine whether the `delivery_drone` will be able to accommodate an `order`.
Remember to remove all orders from the `payload_test_drone` after the trip is built!

## Task 3
**Customer Complaints**

Over the months that we've been in business, we've accumulated a few complaints from our customers.
Since our goal is to maximize efficiency and customer satisfaction, we've decided to address these complaints now.
Respond to customer feedback by implementing the method with the following prototype in [dispatch_server.py]: `build_better_trip(self)`.
Below is a list of customer complaints.
All of them are important to us, but some of them seem to compete with one another.
Implement this method in a way that resolves as many of these problems as you are able.

1. Our most common complaint is that customers' orders are sometimes split into separate trips, which makes pick-up a hassle.
	Ensure that all orders for the same customer are always sent together in a single trip (unless they can't all fit on a drone at once).

2. Some of our customers are subscribers, which means they pay an annual fee in exchange for expedited shipping.
	But some subscribers are complaining that their packages are arriving too slowly.
	Find a way to prioritize expedited orders so that they ship more quickly.

3. In rare circumstances, fragile packages bump into hazardous packages mid-flight and break - forcing us to pay out expensive refunds.
	To stop this, ensure orders marked "fragile" are never sent in the same trip as orders marked "hazardous."

4. Some of our orders are for perishable goods.
	These need to be shipped while they are still fresh.
	Ensure that perishable goods are always moved directly to the front of the queue.
	Feel free to add any other optimizations that you think will be useful (e.g. multi-zone trips).
	You are welcome to use any underlying data structures you like, but you are encouraged to make sure your decisions are well documented and your code is appropriately decomposed.

[drone.py]: src/classes/drone.py
[dispatch-server.py]: src/classes/dispatch_server.py
