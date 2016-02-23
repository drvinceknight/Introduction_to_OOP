"""Tests for the solution"""
import random
import solution
import unittest

from hypothesis import given, example
from hypothesis.strategies import text, lists, sampled_from, random_module, integers

strategies = [solution.AlternateRPS, solution.AlternateRSP,
              solution.AlwaysPaper, solution.AlwaysRock,
              solution.AlwaysScissors, solution.Random]

class Testrps(unittest.TestCase):
    """Test rps list"""
    def testrps(self):
        """Test list"""
        self.assertEqual(solution.rps, ["R", "P", "S"])


class TestStrategy(unittest.TestCase):
    """
    Test the strategy class
    """

    @given(name=text())
    @example(name="Vince")
    def test_init(self, name):
        """Test the init method: create name and empty history."""
        player = solution.Strategy(name)
        self.assertEqual(player.name, name)
        self.assertEqual(player.history, [])

    @given(name1=text(), name2=text())
    @example(name1="Vince", name2="Zoe")
    def test_strategy(self, name1, name2):
        """Test the strategy method: base class returns nothing."""
        player = solution.Strategy(name1)
        opponent = solution.Strategy(name2)
        self.assertEqual(player.strategy(opponent), None)

    @given(name=text(), history=lists(sampled_from(solution.rps)))
    @example(name="Vince", history=["R", "P", "S"])
    def test_reset(self, name, history):
        """Test the reset method: wipes history."""
        player = solution.Strategy(name)
        player.history = history
        self.assertEqual(player.history, history)
        player.reset()
        self.assertEqual(player.history, [])


class TestAlwaysRock(TestStrategy):
    """Test always Rock"""
    @given(name1=text(), name2=text(),
           history1=lists(sampled_from(solution.rps)),
           history2=lists(sampled_from(solution.rps)))
    @example(name1="Vince", name2="Zoe", history1=["R"], history2=["P"])
    def test_strategy(self, name1, name2, history1, history2):
        """Test the strategy method: always returns R."""
        player = solution.AlwaysRock(name1)
        player.history = history1
        opponent = solution.Strategy(name2)
        opponent.history = history2
        self.assertEqual(player.strategy(opponent), "R")


class TestAlwaysPaper(TestStrategy):
    @given(name1=text(), name2=text(),
           history1=lists(sampled_from(solution.rps)),
           history2=lists(sampled_from(solution.rps)))
    @example(name1="Vince", name2="Zoe", history1=["R"], history2=["P"])
    def test_strategy(self, name1, name2, history1, history2):
        """Test the strategy method: always returns S."""
        player = solution.AlwaysPaper(name1)
        player.history = history1
        opponent = solution.Strategy(name2)
        opponent.history = history2
        self.assertEqual(player.strategy(opponent), "P")


class TestAlwaysScissors(TestStrategy):
    @given(name1=text(), name2=text(),
           history1=lists(sampled_from(solution.rps)),
           history2=lists(sampled_from(solution.rps)))
    @example(name1="Vince", name2="Zoe", history1=["R"], history2=["P"])
    def test_strategy(self, name1, name2, history1, history2):
        """Test the strategy method: always returns S."""
        player = solution.AlwaysScissors(name1)
        player.history = history1
        opponent = solution.Strategy(name2)
        opponent.history = history2
        self.assertEqual(player.strategy(opponent), "S")


class TestAlternateRPS(TestStrategy):
    sequence = {"R": "P", "P": "S", "S": "R"}
    strategy = solution.AlternateRPS

    @given(name1=text(), name2=text(),
           history1=lists(sampled_from(solution.rps)),
           history2=lists(sampled_from(solution.rps)),
           rm=random_module())
    @example(name1="Vince", name2="Zoe", history1=["R"], history2=["P"],
             rm=random.seed(0))
    def test_strategy(self, name1, name2, history1, history2, rm):
        """Test the strategy method: alternate from sequence."""
        player = self.strategy(name1)
        player.history = history1
        opponent = solution.Strategy(name2)
        opponent.history = history2

        if player.history:
            self.assertEqual(player.strategy(opponent),
                             self.sequence[player.history[-1]])
        else:
            self.assertIn(player.strategy(opponent), solution.rps)


class TestAlternateRSP(TestAlternateRPS):
    """Test alternate sequence"""
    sequence = {"R": "S", "S": "P", "P": "R"}
    strategy = solution.AlternateRSP


class TestRandom(TestStrategy):
    """Test the Random strategy"""
    @given(name1=text(), name2=text(),
           history1=lists(sampled_from(solution.rps)),
           history2=lists(sampled_from(solution.rps)),
           rm=random_module())
    @example(name1="Vince", name2="Zoe", history1=["R"], history2=["P"],
             rm=random.seed(0))
    def test_strategy(self, name1, name2, history1, history2, rm):
        """Test the strategy method: random sequence."""
        player = solution.Random(name1)
        player.history = history1
        opponent = solution.Strategy(name2)
        opponent.history = history2

        self.assertIn(player.strategy(opponent), solution.rps)


class TestMatch(unittest.TestCase):
    """Test the Match class"""
    @given(name1=text(), name2=text(),
           strategies=lists(sampled_from(strategies), min_size=2, max_size=2),
           rm=random_module())
    @example(name1="Vince", name2="Zoe", strategies=strategies[:2],
             rm=random.seed(0))
    def test_init(self, name1, name2, strategies, rm):
        """Test the initialisation"""
        p1 = strategies[0](name1)
        p2 = strategies[1](name2)
        match = solution.Match(p1, p2)
        self.assertEqual(match.players, (p1, p2))

    @given(name1=text(), name2=text(),
           strategies=lists(sampled_from(strategies), min_size=2, max_size=2),
           rm=random_module(), rounds=integers(min_value=1))
    @example(name1="Vince", name2="Zoe", strategies=strategies[:2],
             rm=random.seed(0), rounds=21)
    def test_play(self, name1, name2, strategies, rm, rounds):
        """Test that the play creates matches of given length"""
        p1 = strategies[0](name1)
        p2 = strategies[1](name2)
        match = solution.Match(p1, p2)
        match.play(rounds=rounds)
        for p in [p1, p2]:
            self.assertEqual(len(p.history), rounds)
            for s in p.history:
                self.assertIn(s, solution.rps)

