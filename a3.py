import matplotlib.pyplot as plt
import csv
import sys
import math
from random import *

a0, a1, b0, b1, c0, c1, d0, d1 = "a0", "a1", "b0", "b1", "c0", "c1", "d0", "d1"
current_assignment = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
sample_a, sample_c, sample_d = 0, 1, 2
samples = []

f_a_b = {(a0, b0): 30,
        (a0, b1): 5,
        (a1, b0): 1,
        (a1, b1): 10}

f_b_c = {(b0, c0): 100,
        (b0, c1): 1,
        (b1, c0): 1,
        (b1, c1): 100}

f_c_d = {(c0, d0): 1,
        (c0, d1): 100,
        (c1, d0): 100,
        (c1, d1): 1}

f_d_a = {(d0, a0): 100,
        (d0, a1): 1,
        (d1, a0): 1,
        (d1, a1): 100}

def run():
    init_random_initial_assignment()
    samples.append(current_assignment)
    generate_samples()
    write_samples_to_csv()

# Generate 100 samples from the initial assignment using Gibbs Sampling
def generate_samples():
    for i in range(100):
        var_to_sample = i % 3
        if (var_to_sample == sample_a):
            print("going to sample a")
        elif (var_to_sample == sample_c):
            print("going to sample c")
        elif (var_to_sample == sample_d):
            print("going to sample d")

# Take our collection of samples and write to csv
def write_samples_to_csv():
    with open('samples.csv', 'w', newline='') as csvfile:
        samplewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for sample in samples:
            samplewriter.writerow(sample.values())

# Randomly generates the initial assignment of the variables
def init_random_initial_assignment():
    current_assignment['a'] = randint(0, 1)
    current_assignment['b'] = 1                 # b is observed to be b1
    current_assignment['c'] = randint(0, 1)
    current_assignment['d'] = randint(0, 1)


if __name__ == '__main__':
    run()
