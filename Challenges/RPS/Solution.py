#! /usr/bin/env python
import random
import itertools

"""
This file contains code for the solution of the Rock Paper Scissors challenge.
"""

rps = ["R", "P", "S"]

class Strategy():
    """
    A generic strategy class
    """
    def __init__(self, name):
        """
        Initialisation
        """
        self.name = name
        self.history = []

    def strategy(self, opponent):
        """
        Generic strategy class
        """
        pass

    def reset(self):
        """
        A method to reset the history
        """
        self.history = []


##########################
#  All the strategies    #
##########################


class AlwaysRock(Strategy):
    """Always plays Rock"""
    def strategy(self, opponent):
        return "R"


class AlwaysPaper(Strategy):
    """Always plays Paper"""
    def strategy(self, opponent):
        return "P"


class AlwaysScissors(Strategy):
    """Always plays Scissors"""
    def strategy(self, opponent):
        return "S"


class AlternateRPS(Strategy):
    """Alternates according to the sequence: R -> P -> S
    Starts at a random spot"""
    sequence = {"R": "P", "P": "S", "S": "R"}

    def strategy(self, opponent):
        if len(self.history) == 0:
            return random.choice(rps)
        return self.sequence[self.history[-1]]


class AlternateRSP(AlternateRPS):
    """Alternates according to the sequence: R -> S -> P
    Starts at a random spot"""
    sequence = {"R": "S", "S": "P", "P": "R"}


class Random(Strategy):
    """Plays randomly"""
    def strategy(self, opponent):
        return random.choice(rps)


#############################
#   The Match class         #
#############################

class Match():
    """A match class. This is used by the tournament to create matches.
    """
    def __init__(self, p1, p2):
        """Initialises with two players and
        also takes the rules of the game."""
        self.players = (p1, p2)
        self.rules = {('R', 'R'): (0, 0),
                      ('S', 'S'): (0, 0),
                      ('P', 'P'): (0, 0),
                      ('R', 'P'): (-1, 1),
                      ('P', 'R'): (1, -1),
                      ('R', 'S'): (1, -1),
                      ('S', 'R'): (-1, 1),
                      ('S', 'P'): (1, -1),
                      ('P', 'S'): (-1, 1),
                      }

    def play(self, rounds):
        """Plays the match and calculates the results."""
        p1, p2 = self.players

        p1.reset()
        p2.reset()

        for round in xrange(rounds):
            p1_dec, p2_dec = p1.strategy(p2), p2.strategy(p1)
            p1.history.append(p1_dec)
            p2.history.append(p2_dec)

        self.calculate_results()

    def calculate_results(self):
        """After the match is played, calculate the results.

        This creates:

        - results, which is a list of tuples showing the win/lose/draws:

        [(1, -1), (1, -1), (0, 0), (-1, 1)]

        - scores, which is a sum of the elements in results:

        [1, -1]

        - winner, the winner of the match, can also be False if there is no
          winner (a draw)
        """
        p1, p2 = self.players

        self.results = [self.rules[rnd] for rnd in zip(p1.history, p2.history)]
        self.scores = [sum(v) for v in zip(*self.results)]
        if self.scores[0] == self.scores[1]:
            self.winner = False
        elif self.scores[0] > self.scores[1]:
            self.winner = self.players[0]
        else:
            self.winner = self.players[1]




#############################
#   The tournament class    #
#############################


class Tournament():
    """
    A class for the tournament
    """
    def __init__(self, players, rounds, repetitions):
        """Initialises the players, number of rounds and repetitions and also
        creates all the matches"""
        self.players = players
        self.rounds = rounds
        self.repetitions = repetitions
        self.matches = [Match(p1, p2) for p1, p2 in
                        itertools.combinations(players, 2)]

    def play(self):
        """Play one round of matches"""
        for m in self.matches:
            m.play(self.rounds)

    def summarise(self):
        """Summarise a round of matches

        Creates:

        - wins which is a list of 2-lists with each sublist being of the form:

        [<player>, <number of wins>]
        """
        self.wins = [[p, 0] for p in self.players]
        for m in self.matches:
            if m.winner:
                record = [r for r in self.wins if r[0] == m.winner][0]
                record[1] += 1
        #for record in self.wins:
            #for m in self.matches:
                #if p in m.players and m.winner == p:
                    #record[1] += 1

    def repeat_play(self):
        """Plays the repeated version of the tournament. Puts outcomes (as
        calculated by summarise) in to a new attribute: data, which looks
        contains elements of the form:

        [<player>, [<number of wins in 1st>, <number of wins in 2nd> ...,
        <number of wins in last>]]
        """
        self.data = [[p, []] for p in self.players]
        for _ in range(self.repetitions):
            self.play()
            self.summarise()
            for i, p in enumerate(self.players):
                self.data[i][1].append(self.wins[i][1])
