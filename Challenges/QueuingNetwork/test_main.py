import unittest
import main
import itertools


class TestIndividual(unittest.TestCase):

    test_vectors = [[1, 2, 3], [1, 4, 5, 6, 7, 8, 9],
                    [1, 2, 3, 4, 5, 6], [0, 2, 4, 5, 6, 7],
                    [0, 0, 0, 0, 0, 0]]

    def pair_of_6_vector_generator(self):
        """
        A generator to yield all possible pairings of strategies.
        """
        vectors_of_length_6 = self.test_vectors[-3:]
        for pair in itertools.product(vectors_of_length_6,
                                      vectors_of_length_6):
            for pair in [pair, pair[::-1]]:  # Test both orderings
                parents = [main.Individual(vector) for vector in pair]
                yield parents

    def test_init(self):
        for vector in self.test_vectors:
            individual = main.Individual(vector=vector)
            self.assertEqual(individual.vector, vector)
            self.assertEqual(individual.loss_cost, 10)
            self.assertEqual(individual.completion_reward, 10)

    def test_init_with_no_vector(self):
        individual = main.Individual()
        self.assertEqual(len(individual.vector), 6)
        self.assertEqual(individual.loss_cost, 10)
        self.assertEqual(individual.completion_reward, 10)

    def test_mutate_with_zero_probability(self):
        for vector in self.test_vectors:
            individual = main.Individual(vector=vector)
            individual.mutate(p=0)
            self.assertEqual(individual.vector, vector)

    def test_mutate_does_not_give_neg_genes(self):
        for vector in self.test_vectors:
            individual = main.Individual(vector=vector)
            for _ in range(2):
                individual.mutate(p=1)
                self.assertGreaterEqual(min(individual.vector), 0)

    def test_mutate_gives_valid_genes(self):
        for vector in self.test_vectors:
            individual = main.Individual(vector=vector)
            individual.mutate()
            for gene in individual.vector:
                self.assertIsInstance(gene, int)

    def test_mutate_distance(self):
        for vector in self.test_vectors:
            individual = main.Individual(vector=vector)
            individual.mutate()
            for gene, original_gene in zip(individual.vector, vector):
                self.assertLessEqual(abs(gene - original_gene), 1)

    def test_crossover_property_of_child(self):
        pairs = self.pair_of_6_vector_generator()
        for parents in pairs:
            child = parents[0].crossover(parents[1])

            self.assertIsInstance(child, main.Individual)
            self.assertTrue(len(child.vector), len(parents[0].vector))

    def test_crossover_inheritance_of_genes(self):
        pairs = self.pair_of_6_vector_generator()
        for parents in pairs:
            child = parents[0].crossover(parents[1])
            for i, gene in enumerate(child.vector):
                parent_genes = [p.vector[i] for p in parents]
                self.assertIn(gene, parent_genes)

    def test_crossover_with_equal_parents(self):
        pairs = self.pair_of_6_vector_generator()
        for parents in pairs:
            child = parents[0].crossover(parents[1])
            if parents[0].vector == parents[1].vector:
                self.assertEqual(child.vector, parents[0].vector)

    def test_child_non_default_parameters(self):
        non_default_loss = 7
        parents = [main.Individual(loss_cost=non_default_loss) for _ in range(2)]
        child = parents[0].crossover(other=parents[1])

        self.assertEqual(child.loss_cost, non_default_loss)

    def test_cost_property(self):
        vectors_of_length_6 = self.test_vectors[-3:]
        for vector in vectors_of_length_6:
            individual = main.Individual(vector=vector)
            individual.calculate_cost()
            self.assertIsInstance(individual.cost, float)

    def test_cost_setup_increase(self):
        vectors_of_length_6 = self.test_vectors[-3:]
        for vector in vectors_of_length_6:
            individual = main.Individual(vector=vector, setup_cost=0)
            individual.calculate_cost()
            zero_setup_cost = individual.cost

            individual.setup_cost = 500
            individual.calculate_cost()
            big_setup_cost = individual.cost

            self.assertEqual(big_setup_cost - zero_setup_cost,
                             sum(individual.vector[3:]) * 500)


class TestGeneticAlgorithm(unittest.TestCase):
    def test_init(self):
        ga = main.GeneticAlgorithm(population_size=50,
                                   death_number=10,
                                   mutation_rate=.05)
        self.assertEqual(ga.population_size, 50)
        self.assertEqual(ga.death_number, 10)
        self.assertEqual(ga.mutation_rate, .05)
        self.assertEqual(len(ga.individuals), 50)

        for individual in ga.individuals:
            self.assertIsInstance(individual, main.Individual)

        self.assertEqual(ga.generations, [])

    def test_calculate_fitness(self):
        ga = main.GeneticAlgorithm(population_size=5,
                                   death_number=2,
                                   mutation_rate=.05)
        initial_population = ga.individuals[:]
        ga.calculate_fitness()
        self.assertEqual(ga.individuals,
                         sorted(initial_population, key=lambda ind: ind.cost))

    def test_run(self):
        ga = main.GeneticAlgorithm(population_size=10,
                                   death_number=6,
                                   mutation_rate=.05)
        number_of_generations = 4
        ga.run(number_of_generations=number_of_generations)
        self.assertEqual(len(ga.generations), number_of_generations)

        for generation in ga.generations:
            for ind in generation:
                self.assertIsInstance(ind, main.Individual)
                self.assertIsInstance(ind.cost, float)

        self.assertIsInstance(ga.best, main.Individual)
