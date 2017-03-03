"""
Solution code for a hackathon exercise for the 2016-2017 MSc.

Students were asked to write a genetic algorithm to best configure a 3 queue in
series network.
"""
import random
import ciw
import copy

class Individual():
    """
    An individual of a population for a genetic algorithm.

    Methods:

        - Cost: this uses Ciw to obtain the cost.
        - Mutate: this randomly mutate individual genes of the underlying vector
        - Crossover: crossover the current individual with another
    """

    def __init__(self, vector=None, loss_cost=10, completion_reward=10,
                 lambda_vector=[2, 4, 5], mu_vector=[5, 2, 3],
                 max_sim_time=168, num_trials=2, setup_cost=20, hourly_wage=2):

        if vector is None:
            vector = [random.randint(0, 10) for _ in range(6)]

        self.vector = vector
        self.loss_cost = loss_cost
        self.completion_reward = completion_reward
        self.lambda_vector = lambda_vector
        self.mu_vector = mu_vector
        self.max_sim_time = max_sim_time
        self.num_trials = num_trials
        self.setup_cost = setup_cost
        self.hourly_wage = hourly_wage

    def mutate(self, p=0.05):
        """
        Mutate the underlying vector

        Parameters:

            - p: The probability of a given gene being mutated.
        """
        for i, gene in enumerate(self.vector):
            if random.random() <= p:
                if random.random() < 0.5:
                    self.vector[i] -= min(1, self.vector[i])
                else:
                    self.vector[i] += 1

    def crossover(self, other):
        """
        Carry out a crossover between two individuals. Outputs an instance of
        the Individual class.
        """
        crossover_index = random.randint(0, len(self.vector))
        child_vector = self.vector[:crossover_index] + other.vector[crossover_index:]
        child = copy.deepcopy(self)
        child.vector = child_vector
        return child

    def calculate_cost(self):
        num_nodes = 3
        params = {'Arrival_distributions': [['Exponential', rate] for rate in
                                            self.lambda_vector],
                  'Number_of_servers': self.vector[:num_nodes],
                  'Queue_capacities': self.vector[num_nodes:],
                  'Service_distributions': [['Exponential', rate] for rate in
                                            self.mu_vector],
                  'Transition_matrices': [[0, 1, 0], [0, 0, 1], [0, 0, 0]]
                  }

        cost = 0
        for seed in range(self.num_trials):
            ciw.seed(seed)
            N = ciw.create_network(params)
            Q = ciw.Simulation(N)
            Q.simulate_until_max_time(self.max_sim_time)

            num_losses = sum(len(Q.rejection_dict[node][0]) for node in range(1,
                                                                 num_nodes + 1))
            num_completed = len(Q.nodes[-1].all_individuals)

            h_per_week = self.max_sim_time

            cost += num_losses * self.loss_cost
            cost -= num_completed * self.completion_reward
            cost += h_per_week * sum(self.vector[:num_nodes]) * self.hourly_wage
            cost += self.setup_cost * sum(self.vector[num_nodes:])

        self.cost = cost / self.num_trials


class GeneticAlgorithm():
    """
    A class to run a genetic algorithm


    Methods
        - fitness: compute the cost function for each individual in a current
          population;
        - evolve: run the entire genetic algorithm.
    """

    def __init__(self, population_size=50, death_number=10, mutation_rate=0.05,
                 **kwargs):
        self.population_size = population_size
        self.death_number = death_number
        self.mutation_rate = mutation_rate
        self.individuals = [Individual(**kwargs)
                            for _ in range(population_size)]
        self.generations = []
        self.best = None

    def calculate_fitness(self):
        """
        Sort the individuals according to their cost.
        """
        for individual in self.individuals:
            individual.calculate_cost()
        self.individuals.sort(key=lambda ind: ind.cost)

    def run(self, number_of_generations=10):
        """
        Run the evolutionary algorithm:

            - Remove weak individuals;
            - Crossover;
            - Mutate
        """
        for _ in range(number_of_generations):
            self.calculate_fitness()
            if self.best is None or self.individuals[0].cost < self.best.cost:
                self.best = self.individuals[0]
            self.generations.append(self.individuals)

            self.individuals = self.individuals[:self.death_number]

            for seed in range(self.population_size - self.death_number):
                random.seed(seed)
                parents = random.sample(self.individuals, 2)
                self.individuals.append(parents[0].crossover(parents[1]))

            for individual in self.individuals:
                individual.mutate(self.mutation_rate)
