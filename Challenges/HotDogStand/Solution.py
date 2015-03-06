#! /usr/bin/env python
from __future__ import division
import random

"""
This file contains code for the solution to the Hot Dog Stand stocking challenge

It prints the output for some default input parameters
"""

def mean(l):
    return sum(l) / len(l)

class Experiment:
    """
    A class to experiment to carry out trials and some form of optimisation
    """
    def __init__(self, arrival_rate=5, service_rate=6, wholesale_price=3, retail_price=4, replenishment_period=10, replenishment_quantity=8):
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.wholesale_price = wholesale_price
        self.retail_price = retail_price
        self.replenishment_period = replenishment_period
        self.replenishment_quantity = replenishment_quantity

    def trial(self, trials=5, simulation_time=1000, warmup=500):
        """
        A class to carry out a trial (repetition of simulation)

            >>> random.seed(10)
            >>> exp = Experiment()
            >>> exp.trial()
            [424, 424, 424, 424, 424]

            >>> exp = Experiment(arrival_rate=.5, service_rate=2, replenishment_period=90, replenishment_quantity=8)
            >>> exp.trial()
            [32, 28, 40, 28, 24]
        """
        return [HotDogStand(self.arrival_rate, self.service_rate, self.wholesale_price, self.retail_price, self.replenishment_period, self.replenishment_quantity).simulate(simulation_time=simulation_time, warmup=warmup) for k in range(trials)]

    def brute_force_optimisation(self, trials=5, simulation_time=1000, warmup=500, period_min=1, period_max=100, quantity_min=1, quantity_max=50):
        """
        Runs a brute force attack on attempting to find optimal period and quantity

        This is the solution to Scenario 1:

            >>> random.seed(1)
            >>> exp = Experiment(arrival_rate=1, service_rate=2, wholesale_price=3, retail_price=4)
            >>> argmax = exp.brute_force_optimisation(trials=10, period_min=10, period_max=30, quantity_min=20, quantity_max=30)
            >>> argmax
            (25, 24)
            >>> exp.profits[argmax]
            544.8

        This is the solution to Scenario 2:
            >>> random.seed(1)
            >>> exp = Experiment(arrival_rate=1, service_rate=2, wholesale_price=1, retail_price=8)
            >>> argmax = exp.brute_force_optimisation(trials=10, period_min=10, period_max=30, quantity_min=20, quantity_max=30)
            >>> argmax
            (19, 20)
            >>> exp.profits[argmax]
            3582.4

        This is the solution to Scenario 3:
            >>> random.seed(1)
            >>> exp = Experiment(arrival_rate=1, service_rate=.9, wholesale_price=3, retail_price=4)
            >>> argmax = exp.brute_force_optimisation(trials=10, period_min=10, period_max=30, quantity_min=20, quantity_max=30)
            >>> argmax
            (25, 23)
            >>> exp.profits[argmax]
            512.6

        This is the solution to Scenario 4:
            >>> random.seed(1)
            >>> exp = Experiment(arrival_rate=1, service_rate=.9, wholesale_price=3, retail_price=40)
            >>> argmax = exp.brute_force_optimisation(trials=10, period_min=10, period_max=30, quantity_min=20, quantity_max=30)
            >>> argmax
            (19, 25)
            >>> exp.profits[argmax]
            18778.0
        """
        self.profits = {}
        for period in range(period_min, period_max + 1):
            for quantity in range(quantity_min, quantity_max + 1):
                self.replenishment_period = period
                self.replenishment_quantity = quantity
                self.profits[(period, quantity)] = mean(self.trial(trials=trials, simulation_time=simulation_time, warmup=warmup))
        return max(self.profits.keys(), key=lambda x:self.profits[x])


class HotDogStand:
    """
    A class for the actual simulation model
    """
    def __init__(self, arrival_rate=5, service_rate=6, wholesale_price=3, retail_price=4, replenishment_period=10, replenishment_quantity=8):
        """
        Initialisation

            >>> m = HotDogStand()
            >>> m.arrival_rate
            5
            >>> m.service_rate
            6
            >>> m.wholesale_price
            3
            >>> m.retail_price
            4
            >>> m.replenishment_period
            10
            >>> m.replenishment_quantity
            8
            >>> len(m.customers)
            1
            >>> m.cost
            24
            >>> m.sales
            0

            >>> m = HotDogStand(arrival_rate=8, service_rate=3, wholesale_price=4, retail_price=9, replenishment_period=100, replenishment_quantity=5)
            >>> m.arrival_rate
            8
            >>> m.service_rate
            3
            >>> m.wholesale_price
            4
            >>> m.retail_price
            9
            >>> m.replenishment_period
            100
            >>> m.replenishment_quantity
            5
            >>> len(m.customers)
            1
            >>> m.cost
            20
            >>> m.sales
            0
        """
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.wholesale_price = wholesale_price
        self.retail_price = retail_price
        self.replenishment_period = replenishment_period
        self.replenishment_quantity = replenishment_quantity
        self.customers = [Customer(0)]
        self.customers_served = [self.customers[-1]]
        self.customers_served[-1].service_end_date = self.sample_service_time()
        self.stock = self.replenishment_quantity
        self.cost = self.replenishment_quantity * self.wholesale_price
        self.sales = 0
        self.clock = 0
        self.next_arrival_date = 0
        self.next_restock_date = self.replenishment_period

    def simulate(self, simulation_time=1000, warmup=0):
        """
        Simulate the hot dog stand and output the profit (sales - cost).

            >>> m = HotDogStand()
            >>> m.simulate()
            796
        """
        if warmup > 0:
            self.cost = 0 # Reset the original cost
        self.warmup = warmup
        self.clock = 0
        self.next_arrival_date = self.sample_interarrival_time()
        while self.clock < simulation_time:
            if self.next_event_is_arrival():
                self.arrival(Customer(self.next_arrival_date))
                self.next_arrival_date += self.sample_interarrival_time()
            else:
                self.restock()
            self.clock = min(self.next_arrival_date, self.next_restock_date)  # Update the clock
        return self.sales - self.cost

    def sample_interarrival_time(self):
        """
        Sample an interarrival time

            >>> random.seed(1)
            >>> m = HotDogStand()
            >>> round(m.sample_interarrival_time(), 2)
            0.38
            >>> round(mean([m.sample_interarrival_time() for k in range(10000)]), 2)
            0.2
        """
        return random.expovariate(self.arrival_rate)

    def sample_service_time(self):
        """
        Sample a service time

            >>> random.seed(1)
            >>> m = HotDogStand()
            >>> round(m.sample_service_time(), 2)
            0.31
            >>> round(mean([m.sample_service_time() for k in range(10000)]), 2)
            0.17
        """
        return random.expovariate(self.service_rate)

    def restock(self):
        """
        Restock the stand

            >>> m = HotDogStand()
            >>> m.stock
            8
            >>> m.next_restock_date
            10
            >>> m.warmup = 0
            >>> m.restock()
            >>> m.stock
            16
            >>> m.next_restock_date
            20
        """
        self.stock += self.replenishment_quantity
        self.next_restock_date += self.replenishment_period
        if self.clock > self.warmup:
            self.cost += self.replenishment_quantity * self.wholesale_price

    def next_event_is_arrival(self):
        """
        Boolean of whether or not the next event is an arrival

            >>> m = HotDogStand()
            >>> m.next_restock_date = 5
            >>> m.next_arrival_date = 7
            >>> m.next_event_is_arrival()
            False
            >>> m.next_restock_date = 15
            >>> m.next_event_is_arrival()
            True
        """
        return self.next_restock_date > self.next_arrival_date

    def arrival(self, customer):
        """
        A method for an arrival of a customer

            >>> m = HotDogStand()
            >>> c = Customer(5)
            >>> len(m.customers)
            1
            >>> len(m.customers_served)
            1
            >>> m.warmup = 0
            >>> m.arrival(c)
            >>> len(m.customers)
            2
            >>> len(m.customers_served)
            2
        """
        if self.number_of_customers_at_stand() < self.stock:
            customer.service = True
            customer.service_start_date = max(customer.arrival_date, self.customers_served[-1].service_end_date)
            customer.service_end_date = customer.service_start_date + self.sample_service_time()
            self.customers_served.append(customer)
            self.stock -= 1
            if self.clock > self.warmup:
                self.sales += self.retail_price
        else:
            customer.service = False
            customer.service_start_date = customer.arrival_date
            customer.service_end_date = customer.arrival_date
        self.customers.append(customer)

    def number_of_customers_at_stand(self):
        """
        Returns the count of people currently at the stand

            >>> m = HotDogStand()
            >>> c1, c2, c3 = Customer(5), Customer(6), Customer(7)
            >>> c1.service_end_date, c2.service_end_date, c3.service_end_date = 10, 11, 12
            >>> m.customers_served = [c1, c2, c3]
            >>> m.clock = 10.5
            >>> m.number_of_customers_at_stand()
            2
        """
        return len([c for c in self.customers_served if c.service_end_date > self.clock])

class Customer():
    """
    A class for the customer
    """
    def __init__(self, arrival_date):
        self.arrival_date = arrival_date
