> This repository was built upon a mock-project template.
> You can see in `TODO.md` that there were a series of tasks given to be completed.
>
> All the tasks are complete in this project workspace!
> I had a lot of fun completing these tasks on my own and tweaking the codebase, to help practice and showcase my skills.

# Drone Delivery
This project is designed to run simulations of delivery drones packing and shipping merchandise, like an online retailer might want to do.
Given a set of products that were ordered by customers, it will optimally load drones based on order weight, product tags, premium membership, and importantly, when the product was ordered.
Drones will order as much as they can per trip, and prioritize delivering more critical deliveries first.

## How to Run
Download the code, and then run:
- `python3 ./src/main.py`

## How to Test
Download the code, and then run:
- `python3 ./src/main.py --test`

## How to Use
### Input Values
The input values can all be found in the csv files.
Navigate to `./src/data/` in order to view different sets of mock order data!

### Terminal Output
When you run the script, data is output in your terminal.
It looks something like this:

~~~md
Headed out for delivery:
        ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
        █ Delivering Order...
        █ - ORDER: #ADV-003.
        █ - ZONE: 2
        █ - USER: user-002
        █ - DATE: 2030-01-08 09:00
        █ - WEIGHT: 900.0
        █ - TAGS: fragile
        █ ...Success!
        ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
        ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
        █ Delivering Order...
        █ - ORDER: #ADV-018.
        █ - ZONE: 7
        █ - USER: user-009
        █ - DATE: 2030-01-08 15:35
        █ - WEIGHT: 950.0
        █ - TAGS: expedited fragile
        █ ...Success!
        ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
~~~

These tables show what orders were delivered by a drone, including various order details.
Orders are delivered chronologically, so Order ID `#ADV-018` was delivered after Order ID `#ADV-003` in this output.

The script also outputs any orders that were left undelivered, which should only be impossible orders.
