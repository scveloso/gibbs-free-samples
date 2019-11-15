import matplotlib.pyplot as plt
import csv
import sys
import math
from random import *

a0, a1, b0, b1, c0, c1, d0, d1 = "a0", "a1", "b0", "b1", "c0", "c1", "d0", "d1"
previous_sample = {}
is_a, is_c, is_d = 0, 1, 2
samples = []
VARIABLE_ELIMINATION_RESULT = 0.029

f_a_b = {(a0, b1): 5,
        (a1, b1): 10}

f_b_c = {(b1, c0): 1,
        (b1, c1): 100}

f_c_d = {(c0, d0): 1,
        (c0, d1): 100,
        (c1, d0): 100,
        (c1, d1): 1}

f_d_a = {(d0, a0): 100,
        (d0, a1): 1,
        (d1, a0): 1,
        (d1, a1): 100}

# Run Gibbs Sampling on a random initial assignment:
# (1) An initial assignment is made at random
# (2) We generate the given number of samples
# (3) We write the samples to a csv file (Not sure if needed for next TODO)
# (4) TODO: Plot a graph of P(A|b1) from the samples we generated. y-axis
#           is estimate of P(A|b1) and x-axis is number of samples. Also
#           plot a horizontal line representing the P(A|b1) computed from
#           Variable Elimination by hand (Q1A)
def run():
    if len(sys.argv) > 1:
        runGibbsSampling(int(sys.argv[1]))
        plotGraph()
    else:
        print('Usage: \n"python3 a3.py <number of samples to generate>" to run Gibbs Sampling and plot the Graph')

#plots the graph of P(A|b1)
# y-axis is estimate of P(A|b1) and x-axis is number of samples.
# Also plot a horizontal line representing the P(A|b1) computed from Variable Elimination by hand (Q1A)
def plotGraph():
    x = []
    y = []
    num_samples = 0
    num_a0 = 0
    num_a1 = 0

    with open('samples.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            num_samples += 1
            if row[0] == 'a0':
                num_a0 += 1
            elif row[0] == 'a1':
                num_a1 += 1

            normalized_a1 = num_a1 / num_samples
            x.append(num_samples)
            y.append(normalized_a1)

    normalized_a1 = num_a1 / num_samples
    normalized_a0 = num_a0 / num_samples
    final_posterior_distribution = str(normalized_a1) + ", " + str(normalized_a0)
    print(final_posterior_distribution)
    plot(x, y, 'Gibbs Sampling')
    sys.exit()

# Plots the given x, y into a graph
def plot(x, y, title):
    ve_result = [VARIABLE_ELIMINATION_RESULT] * len(y)
    plt.plot(x,y, label='P(r|s,w)')
    plt.plot(x,ve_result)
    plt.xlabel('Number of samples')
    plt.ylabel('P(A|b1)')
    plt.title(title)
    plt.legend()
    plt.legend(['P(r|s,w) through Gibbs Sampling', 'P(r|s,w) through Variable Elimination'], loc='upper right')
    plt.show()

# executes Gibbs Sampling and writes the samples to a csv file
def runGibbsSampling(num_samples_to_generate):
    init_random_initial_assignment()
    #print("Initial assignment:")
    #print(previous_sample)
    samples.append(previous_sample)
    generate_samples(num_samples_to_generate)
    write_samples_to_csv()

# Generate the given number of samples from a random initial assignment using Gibbs Sampling
def generate_samples(num_samples_to_generate):
    for i in range(num_samples_to_generate):
        var_to_sample = i % 3
        if (var_to_sample == is_a):
            sample_a()
        elif (var_to_sample == is_c):
            sample_c()
        elif (var_to_sample == is_d):
            sample_d()

# (1) Compute probability of 'a' given the previous sample
# (2) Sample 'a' based on that probability
# (3) Add it to a list of samples
def sample_a():
    if random() <= probability_a()[a0]:
        a_val = a0
    else:
        a_val = a1

    generated_sample = {'a': a_val,
                        'b': previous_sample['b'],
                        'c': previous_sample['c'],
                        'd': previous_sample['d']}
    #print("Sampled a and adding generated sample:")
    #print(generated_sample)
    samples.append(generated_sample)
    update_previous_sample(generated_sample)

# (1) Compute probability of 'c' given the previous sample
# (2) Sample 'c' based on that probability
# (3) Add it to a list of samples
def sample_c():
    if random() <= probability_c()[c0]:
        c_val = c0
    else:
        c_val = c1

    generated_sample = {'a': previous_sample['a'],
                        'b': previous_sample['b'],
                        'c': c_val,
                        'd': previous_sample['d']}
    #print("Sampled c and adding generated sample:")
    #print(generated_sample)
    samples.append(generated_sample)
    update_previous_sample(generated_sample)

# (1) Compute probability of 'd' given the previous sample
# (2) Sample 'd' based on that probability
# (3) Add it to a list of samples
def sample_d():
    if random() <= probability_d()[d0]:
        d_val = d0
    else:
        d_val = d1

    generated_sample = {'a': previous_sample['a'],
                        'b': previous_sample['b'],
                        'c': previous_sample['c'],
                        'd': d_val}
    #print("Sampled d and adding generated sample:")
    #print(generated_sample)
    samples.append(generated_sample)
    update_previous_sample(generated_sample)

# Multiply out factors to get probability of a
def probability_a():
    d_val = previous_sample['d']
    b_val = previous_sample['b']

    f_a = {a0: (get_factor_value(f_a_b, a0, b_val) * get_factor_value(f_d_a, a0, d_val)),
           a1: (get_factor_value(f_a_b, a1, b_val) * get_factor_value(f_d_a, a1, d_val)) }
    return normalize(f_a)

# Multiply out factors to get probability of c
def probability_c():
    d_val = previous_sample['d']
    b_val = previous_sample['b']

    f_c = {c0: (get_factor_value(f_c_d, c0, d_val) * get_factor_value(f_b_c, c0, b_val)),
           c1: (get_factor_value(f_c_d, c1, d_val) * get_factor_value(f_b_c, c1, b_val)) }
    return normalize(f_c)

# Multiply out factors to get probability of d
def probability_d():
    c_val = previous_sample['c']
    a_val = previous_sample['a']

    f_d = {d0: (get_factor_value(f_c_d, d0, c_val) * get_factor_value(f_d_a, d0, a_val)),
           d1: (get_factor_value(f_c_d, d1, c_val) * get_factor_value(f_d_a, d1, a_val)) }
    return normalize(f_d)

# Sum out variable from a factor
def get_factor_value(factor, var, observed):
    factor_value = 0
    for key, value in factor.items():
        if var in key and observed in key:
            factor_value += value
    return factor_value

# Normalize the given factor values
def normalize(factor):
    total_value = 0
    for value in factor.values():
        total_value += value

    for key, value in factor.items():
        factor[key] = value / total_value

    return factor

# Update previous sample with the generated sample
def update_previous_sample(generated_sample):
    previous_sample['a'] = generated_sample['a']
    previous_sample['b'] = generated_sample['b']
    previous_sample['c'] = generated_sample['c']
    previous_sample['d'] = generated_sample['d']

# Take our collection of samples and write to csv
def write_samples_to_csv():
    with open('samples.csv', 'w', newline='') as csvfile:
        samplewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for sample in samples:
            samplewriter.writerow(sample.values())

# Randomly generates the initial assignment of the variables
def init_random_initial_assignment():
    previous_sample['a'] = a0 if randint(0, 1) == 0 else a1
    previous_sample['b'] = b1                # b is observed to be b1
    previous_sample['c'] = c0 if randint(0, 1) == 0 else c1
    previous_sample['d'] = d0 if randint(0, 1) == 0 else d1


if __name__ == '__main__':
    run()
