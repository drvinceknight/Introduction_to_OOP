# Shortest possible simulation of problem
from random import expovariate, seed
def main(arrival_date=0, delivery_date=0, customers=0, delivery_period=10, delivery_quantity=5, retail_price=5, wholesale_price=1, hot_dogs=0, lmbda=1, T=2000, warmup=500):
    while min(arrival_date, delivery_date) < T:
        if arrival_date < delivery_date: customers, hot_dogs, arrival_date = customers + min(1, hot_dogs) * (arrival_date > warmup), max(hot_dogs - 1, 0), arrival_date + expovariate(lmbda)
        else: delivery_date, hot_dogs = delivery_date + delivery_period, hot_dogs + delivery_quantity
    return customers * retail_price - int((arrival_date - warmup) / delivery_period) * delivery_quantity * wholesale_price
min_period, max_period, min_quantity, max_quantity, trials = 1, 20, 1, 20, 20
seed(1)
print max([(period, quantity, sum([main(delivery_period=period, delivery_quantity=quantity) for k in range(trials)])) for period in range(min_period, max_period + 1) for quantity in range(min_quantity, max_quantity + 1)], key=lambda x: x[2])
