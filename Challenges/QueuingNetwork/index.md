---
layout   : page
title    : Configuring a queueing network
comments : false
---

## Company:

Hospital Clinic

## Required product:

Program an **evolutionary algorithm** to evaluate the best configuration for a
given queuing network.

## Description

Consider the medical clinic shown below:

![Diagram of network](./network.png)

Note that if a customer arrives from outside the network at a node that has no
queuing capacity then they are turned away, ie "lost". However, if a customer
finishing service at a node tries to enter another node which has no
capacity then they will be blocked, remaining at their server until room becomes
available.

The goal is to identify how to best configure the medical clinic for its first
week (168 hours) of operation. We assume that we will be starting from an empty
system, and that there will be 24 hours of continuous service with no breaks.
The variables for the problem can be summarised as an integer vector of size 6:

$$x=(c_1, c_2, c_3, n_1, n_2, n_3)$$

The cost of a given configuration is given by:

$$f(x)=168\times(c_1 + c_2 + c_3)\times h + (n_1 + n_2 + n_3)\times S + C\times N_L - R\times N_C$$

where:

- \\(h\\): the hourly wage of a server (doctor/nurse/receptionist...) in the clinic.
- \\(S\\): the setup cost of a single waiting space.
- \\(C, N_L\\): the cost/number of individuals who are turned away ("lost") due to
  insufficient space.
- \\(R, N_C\\): the reward/number of times an individual completed their time in
  the clinic.

## Parameters:

The network is defined by the following parameters:

- Arrival rate at each node (how often customers arrive, assumed to follow an
  exponential distribution)
- Service rate at each node (how quickly a server serves an individual,
  assumed to follow an exponential distribution)

**Obtain the best configuration with the following parameter sets:**

### Parameter set 1

- \\(\mu=(0.5, 0.5, 0.5)\\)
- \\(\Lambda=(1.5, 1.5, 2.5)\\)
- \\(h=2\\)
- \\(S=20\\)
- \\(C=10\\)
- \\(R=20\\)

### Parameter set 2

- \\(\mu=(0.5, 0.5, 0.5)\\)
- \\(\Lambda=(1.5, 1.5, 2.5)\\)
- \\(h=0\\)
- \\(S=20\\)
- \\(C=10\\)
- \\(R=20\\)

### Parameter set 3

- \\(\mu=(10, 2, 3)\\)
- \\(\Lambda=(0.05, 0.05, 4)\\)
- \\(h=2\\)
- \\(S=20\\)
- \\(C=10\\)
- \\(R=20\\)

## Evaluation:

Your code will be evaluated in terms of:

- Use of object oriented programming (This is both a subjective and an objective
  criteria).
- Precision (does it work and if so is it correct? - This is an objective
  criteria).
- Performance (how fast is it? how does it handle bugs? - This is an objective
  criteria).
- Time taken to submit solution (This is an objective criteria).
- Clarity (is it well written/documented/tested - This is a subjective
  criteria).
- How well you work as a group during the two days of the hackathon (This is a
  subjective criteria)

## Suggestion:

I suggest you proceed by clearly defining independent programming tasks and
attempting to work independently whilst ensuring that each piece of code
produced is capable of talking to each other piece.

To simulate the queueing process you can use
[Ciw](http://ciw.readthedocs.io/en/latest/).
