---
layout     : post
title      : Rock Paper Scissors
categories : challenge
comments   : false
---

##Company:

University

##Required product:

Program to help understand the best strategy to play [Rock Paper
Scissors](https://en.wikipedia.org/wiki/Rock-paper-scissors).  You need to build
a tournament that creates a [round
robin](https://en.wikipedia.org/wiki/Round-robin_tournament) of players using
different strategies playing
Rock Paper Scissors. Each match between 2 players
will be 21 rounds of Rock Paper Scissors.

After creating this tournament, create a new strategy that wins the overall
tournament.

##Parameters:

There will be 6 original strategies/players:

- Always play Rock;
- Always play Paper;
- Always play Scissors;
- Alternate: Rock then Paper then Scissors;
- Alternate: Rock then Scissors then Paper;
- Play randomly

##Particularities that need to be taken in to account:

Strategies are allowed to keep track of what has happened throughout their
current duel but **do not know** what strategy/player they are playing (although
they can try to figure it out).

##Summary:

The following picture summarises your challenge:

![Simple summar](./rps_tournament.svg)

##Evaluation:


Your code will be evaluated in terms of:

- Precision (does it work and if so is it correct? - This is an objective criteria)
- Performance (how fast is it? how does it handle bugs? - This is an objective criteria)
- Time taken to submit solution (This is an objective criteria)
- Clarity (is it well written/documented/tested  - This is a subjective criteria)
- How have you been working as a team (This is a subjective criteria)

##Suggestion:

I suggest you proceed by clearly defining independent programming tasks and
attempting to work independently whilst ensuring that each piece of code
produced is capable of talking to each other piece.
