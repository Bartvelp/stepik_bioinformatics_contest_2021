"""
In this problem you will be given a number of haplotype-resolved genotypes
impute missing positions in a collection of partial genotypes

Chromosomes: two binary strings of length k

For a subset of n people from this population you will be given fully resolved haplotypes
For a subset of m people from the same population you will be given partially-resolved genotypes

Input file
there are n blocks of three strings each

then m blocks of 2 string consisting of 0, 1, 2, and ???. Summed of parents
"""

import numpy as np
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def parse_input(fn: str):
    if fn.endswith('.txt'):
        lines = open(fn).readlines()
    
    num_full = int(lines[0].split(' ')[0])
    num_part = int(lines[0].split(' ')[1])
    eprint('Got num_full, num_part', num_full, num_part)
    lines = lines[2:]

    full_haplotypes = []
    for i in range(0, num_full * 3, 3):
        chromosomes = [lines[i].strip(), lines[i + 1].strip()]
        full_haplotypes.append(chromosomes)
    full_haplotypes = np.array(full_haplotypes)

    half_haplotypes = []
    for i in range(num_full * 3, len(lines), 2):
        half_haplotypes.append(lines[i].strip())

    return full_haplotypes, half_haplotypes

def get_closest_full_i(half_haplotype: str, search_pos: int):
    for i in range(5):
        before = search_pos - i
        after = search_pos + i
        if before < 0:
            before = search_pos
        if after > len(half_haplotype) - 1:
            after = search_pos
        before_res = half_haplotype[before]
        after_res = half_haplotype[after]
        if before_res != '?':
            return before
        elif after_res != '?':
            return after

def get_predicted_char(search_char, search_pos, wanted_pos, full_haplotypes):
    if search_char == '2':
        search_char = '1'

    found_chars = []
    for chromosomes in full_haplotypes:
        for chromosome in chromosomes:
            if chromosome[search_pos] == search_char:
                found_chars.append(chromosome[wanted_pos])
    average = sum(map(int, found_chars)) / len(found_chars)
    if (average < 0.33):
        return '0'
    elif (average < 0.67):
        return '1'
    else:
        return '2'

def solve_problem(half_haplotype, full_haplotypes):
    resolved_haplotype = list(half_haplotype)
    for i, char in enumerate(half_haplotype):
        if char == '?':
            closest_avail_i = get_closest_full_i(half_haplotype, i)
            avail_char = half_haplotype[closest_avail_i]
            new_char = get_predicted_char(avail_char, closest_avail_i, i, full_haplotypes)
            resolved_haplotype[i] = new_char
    return ''.join(resolved_haplotype)

if __name__ == "__main__":
    full_haplotypes, half_haplotypes = parse_input(sys.argv[1])

    for half_haplotype in half_haplotypes:
        resolved_haplotype = solve_problem(half_haplotype, full_haplotypes)
        print(resolved_haplotype + '\n')