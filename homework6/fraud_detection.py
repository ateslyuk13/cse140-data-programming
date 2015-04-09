#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://courses.cs.washington.edu/courses/cse140/13wi/homework/hw6/assignment.html

from __future__ import unicode_literals, print_function
from matplotlib import pyplot
from collections import Counter
import math, csv, codecs
from random import randint, uniform
from itertools import chain, izip

def extract_data(filename, column_names):
    with open(filename) as f:
        elects = [row for row in csv.DictReader(f)]
    
    results = ([row[cn] for cn in column_names] for row in elects)
    results = [row for row in results if '' not in row]
    results = chain(*results)
    return list(results)

def extract_election_vote_counts(filename, column_names):
    """
    >>> extract_election_vote_counts("election-iran-2009.csv", ["Ahmadinejad", "Rezai", "Karrubi", "Mousavi"]) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    [1131111, 16920, 7246, 837858, 623946, 12199, 21609, 656508, ...
    """
    '''
    with open(filename) as f:
        elects = [row for row in csv.DictReader(f)]
    
    results = ([row[cn] for cn in column_names] for row in elects)
    results = [row for row in results if '' not in row]
    results = chain(*results)
    '''
    results = extract_data(filename, column_names)
    return [int(filter(lambda x:x!=',', vote)) for vote in results]

def ones_and_tens_digit_histogram(numbers):
    """
    >>> ones_and_tens_digit_histogram([0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765])
    [0.21428571428571427, 0.14285714285714285, 0.047619047619047616, 0.11904761904761904, 0.09523809523809523, 0.09523809523809523, 0.023809523809523808, 0.09523809523809523, 0.11904761904761904, 0.047619047619047616]
    """
    twodigits = (number % 100 for number in numbers)
    twodigits = [(d/10, d%10) for d in twodigits]
    return [float(sum(twodigit.count(i) for twodigit in twodigits)) / (len(numbers) * 2) for i in range(10)]


def plot_iranian_least_digits_histogram(histogram):
    """
    >>> plot_iranian_least_digits_histogram(
    ...     ones_and_tens_digit_histogram(
    ...         [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
    ...     )
    ... ) # doctest: +SKIP
    None
    """
    pyplot.plot([0.1 for _ in range(10)], label='Ideal')
    pyplot.plot(histogram, label='Iran')
    pyplot.legend()
    pyplot.ylabel('Frequency')
    pyplot.xlabel('Digit')
    pyplot.savefig('iran-digits.png')
    pyplot.show()
    return None

def plot_distribution_by_sample_size():
    """
    >>> plot_distribution_by_sample_size() # doctest: +SKIP
    None
    """
    pyplot.plot([0.1 for _ in range(10)], label='Ideal')
    for size in [10, 50, 100, 1000, 10000]:
        dist = [randint(0,99) for _ in range(size)]
        hist = ones_and_tens_digit_histogram(dist)
        pyplot.plot(hist, label=size)
    pyplot.legend()
    pyplot.ylabel('Frequency')
    pyplot.xlabel('Digit')
    pyplot.savefig('random-digits.png')
    pyplot.show()
    return None

def mean_squared_error(numbers1, numbers2):
    """
    >>> mean_squared_error([1, 4, 9], [6, 5, 4])
    51.0
    """
    return reduce(lambda x,y:x+y, (math.pow(a-b,2) for (a,b) in izip(numbers1, numbers2)))

def calculate_mse_with_uniform(histogram):
    """
    >>> counts = extract_election_vote_counts("election-iran-2009.csv", ["Ahmadinejad", "Rezai", "Karrubi", "Mousavi"])
    >>> histogram = ones_and_tens_digit_histogram(counts)
    >>> calculate_mse_with_uniform(histogram) # doctest: +ELLIPSIS
    0.00739583333333...
    """
    #print(histogram)
    uniform_dist = [0.1 for _ in histogram]
    return mean_squared_error(histogram, uniform_dist)

def compare_iranian_mse_to_samples(mse):
    """
    >>> compare_iranian_mse_to_samples(0.00739583333333) # doctest: +ELLIPSIS +SKIP
    Quantity of MSEs larger than or equal to the 2009 Iranian election MSE: ... 
    Quantity of MSEs smaller than the 2009 Iranian election MSE: ...
    2009 Iranian election null hypothesis rejection level p: ... 
    """
    def group():
        return [randint(0,99) for _ in range(120)]

    mse_samples = (calculate_mse_with_uniform(ones_and_tens_digit_histogram(group())) for _ in range(10000))
    larger_count = sum(1 for mse_sample in mse_samples if mse_sample >= mse)
    smaller_count = 10000-larger_count
    print("Quantity of MSEs larger than or equal to the 2009 Iranian election MSE:", larger_count)
    print("Quantity of MSEs smaller than the 2009 Iranian election MSE:", smaller_count)
    print("2009 Iranian election null hypothesis rejection level p:", float(larger_count) / 10000) 

def most_sig_digits_from_numbers(numbers):
    '''
    >>> most_sig_digits_from_numbers([1,20,300,4000])
    [1, 2, 3, 4]
    '''
    msdigits = (n / int(math.pow(10, len(str(n))-1 ) ) for n in numbers)
    return list(msdigits)

def most_sig_digits_histogram(numbers):
    '''
    >>> most_sig_digits_histogram([1,20,300,4000])
    [0.25, 0.25, 0.25, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0]
    '''
    msdcounts = Counter(most_sig_digits_from_numbers(numbers))
    return [float(msdcounts[d]) / len(numbers) for d in range(1,10)]

def most_sig_digits_benfold(numbers):
    #print('===>', numbers)
    return [math.log10(1+1./d) for d in range(1,10)]

def problem_nine_ten_eleven():
    """
    >>> problem_nine_ten_eleven() # doctest: +SKIP
    None
    """
    counts = extract_election_vote_counts("election-iran-2009.csv", ["Ahmadinejad", "Rezai", "Karrubi", "Mousavi"])
    histogram = most_sig_digits_histogram(counts)
    pyplot.plot(histogram, label='Iran')

    # problem 9
    benfolds = most_sig_digits_benfold(counts)
    pyplot.plot(benfolds, label='Benfold')

    # problem 10
    counts = [math.pow(math.e, uniform(0, 30)) for _ in range(1000)]
    histogram = most_sig_digits_histogram([int(c) for c in counts])
    pyplot.plot(histogram, label='1000 samples')

    # problem 11
    counts = [math.pi * e for e in counts]
    histogram = most_sig_digits_histogram([int(c) for c in counts])
    pyplot.plot(histogram, label='1000 samples, scaled by $\pi$')

    pyplot.legend()
    pyplot.ylabel('Frequency')
    pyplot.xlabel('First digit')
    pyplot.show()


def problem_13():
    '''
    >>> problem_13() # doctest: +SKIP
    '''
    # problem 12
    counts = extract_data('SUB-EST2009_ALL.csv', ["POPCENSUS_2000"])
    counts = [int(count) for count in counts if count not in ('0', 'X')]

    benfolds = most_sig_digits_benfold(counts)
    pyplot.plot(benfolds, label='Benfold')

    counts_filtered_zero = [count for count in counts if count != 0]
    histogram = most_sig_digits_histogram(counts)
    pyplot.plot(histogram, label='US (all)')

    # problem 13
    with codecs.open('literature-population.txt', encoding='utf8') as f:
        pops = (line.strip().split('\t')[1] for line in f)
        pops = [int(filter(lambda x:x!=',', pop)) for pop in pops]

    benfolds = most_sig_digits_benfold(pops)
    pyplot.plot(benfolds, label='Literature Place (b)')
    histogram = most_sig_digits_histogram(pops)
    pyplot.plot(histogram, label='Literature Places (h)')

    pyplot.legend()
    pyplot.ylabel('Frequency')
    pyplot.xlabel('First digit')
    pyplot.savefig('population-data.png')
    pyplot.show()

def problem_14():
    '''
    >>> problem_14() # doctest: +SKIP
    '''
    # problem 12
    counts = extract_data('SUB-EST2009_ALL.csv', ["POPCENSUS_2000"])
    counts = [int(count) for count in counts if count not in ('0', 'X')]

    benfolds = most_sig_digits_benfold(counts)
    pyplot.plot(benfolds, label='Benfold')

    counts_filtered_zero = [count for count in counts if count != 0]
    histogram = most_sig_digits_histogram(counts)
    pyplot.plot(histogram, label='US (all)')

    # problem 14
    with codecs.open('literature-population.txt', encoding='utf8') as f:
        pops = (line.strip().split('\t')[1] for line in f)
        pops = [int(filter(lambda x:x!=',', pop)) for pop in pops]

    benfolds = most_sig_digits_benfold(pops)
    pyplot.plot(benfolds, label='Literature Place (b)')
    histogram = most_sig_digits_histogram(pops)
    pyplot.plot(histogram, label='Literature Places (h)')

    n_samples = [10, 50, 100, 1000]
    for n in n_samples:
        counts = [math.pow(math.e, uniform(0, 30)) for _ in range(n)]
        histogram = most_sig_digits_histogram([int(c) for c in counts])
        pyplot.plot(histogram, label=unicode(n)+' samples')

    pyplot.legend()
    pyplot.ylabel('Frequency')
    pyplot.xlabel('First digit')
    pyplot.savefig('population-data.png')
    pyplot.show()

def problem_15():
    '''
    >>> problem_15()
    '''
    # problem 14
    with codecs.open('literature-population.txt', encoding='utf8') as f:
        pops = (line.strip().split('\t')[1] for line in f)
        pops = [int(filter(lambda x:x!=',', pop)) for pop in pops]

    benfolds = most_sig_digits_benfold(pops)
    pyplot.plot(benfolds, label='Literature Place (b)')
    histogram = most_sig_digits_histogram(pops)

    mse = mean_squared_error(benfolds, histogram)
    #print('---- %.10f' % mse)

    n_us_towns = len(pops)

    # problem 12
    counts = extract_data('SUB-EST2009_ALL.csv', ["POPCENSUS_2000"])
    counts = [int(count) for count in counts if count not in ('0', 'X')]

    samples = [[counts[randint(0, len(counts)-1)] for n in range(n_us_towns)] for _ in range(10000)]
    histograms = (most_sig_digits_histogram(sample) for sample in samples)
    benfolds = (most_sig_digits_benfold(sample) for sample in samples)
    mse_samples = (mean_squared_error(histogram, benfold) for (histogram, benfold) in izip(histograms, benfolds))
    smaller = sum(1 for mse_sample in mse_samples if mse_sample < mse)

    print('Comparison on US MSEs to literature MSE:\nlarger/equal: %d\nsmaller: %d\n'%(10000-smaller, smaller))

def main():
    us_2008_candidates = ["Obama", "McCain", "Nader", "Barr", "Baldwin", "McKinney"]
    counts = extract_election_vote_counts('election-us-2008.csv', us_2008_candidates)
    histogram = ones_and_tens_digit_histogram(counts)
    mse = calculate_mse_with_uniform(histogram)
    compare_iranian_mse_to_samples(mse)


if __name__ == '__main__':
    main()

