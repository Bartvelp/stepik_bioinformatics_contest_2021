from multiprocessing.dummy import Pool as ThreadPool
from sys import argv
import sys
import zipfile
import numpy as np
import math
# import ray
# ray.init(num_cpus=8)

def chunks(l: list, n: int):
    # https://stackoverflow.com/a/1751478/5329317
    n = max(1, n)
    return list(l[i:i+n] for i in range(0, len(l), n))

def find_nearest(array, value, sorter):
    # Adapted from https://stackoverflow.com/a/26026189/5329317
    idx = np.searchsorted(array, value, side="left", sorter=sorter)
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return array[idx-1], idx - 1
    else:
        return array[idx], idx


def parse_problems(lines: list):
    problems = []
    problems_lines = chunks(lines, 4)
    for problem_lines in problems_lines:
        problem_lines = problem_lines[1:] # remove counts line
        metabolite_strings = problem_lines[0].strip().split(' ')
        metabolite_masses = np.asarray(metabolite_strings, dtype=np.single)

        adducts_strings = problem_lines[1].strip().split(' ')
        adducts_masses = np.asarray(adducts_strings, dtype=np.single)

        signal_strings = problem_lines[2].strip().split(' ')
        signal_masses = np.asarray(signal_strings, dtype=np.single)

        problems.append((metabolite_masses, adducts_masses, signal_masses))
    return problems

def find_optimal_ma_comb(signal: float, pos_metabolites: np.array, pos_adducts: np.array, pos_metabolites_sort_i: np.array):
    best_delta = None
    best_indices = None # (mi, ai)
    # For each adduct, find the best metabolite
    for ai, adduct in enumerate(pos_adducts): # Signal = metabolite + adduct + delta
        wanted_metabolite_weight = signal - adduct
        best_met, mi = find_nearest(pos_metabolites, wanted_metabolite_weight, pos_metabolites_sort_i)
        if (best_met + adduct < 0):
            continue # Skip negatives
        delta = abs(signal - best_met - adduct)
        if best_delta is None or delta < best_delta:
            best_delta = delta
            best_indices = (mi, ai)
    return best_indices


if __name__ == "__main__":
    input_path = argv[1]
    if input_path.endswith('.zip'):
        archive = zipfile.ZipFile(argv[1], 'r')
        lines = archive.read(argv[2]).decode().splitlines()[1:]
    elif input_path.endswith('.txt'):
        fh = open(input_path)
        lines = fh.read().splitlines()[1:]
    problems = parse_problems(lines)

    # Solve each problem
    result_ids = []
    for problem in problems:
        pos_metabolites, pos_adducts, signals = problem
        pos_metabolites_sort_i = np.argsort(pos_metabolites)
        for signal in signals:
            optimal_comb = find_optimal_ma_comb(signal, pos_metabolites, pos_adducts, pos_metabolites_sort_i)
            result_ids.append(optimal_comb)
    results = result_ids # ray.get(result_ids)

    for result in results:
        wanted_indices = list(map(lambda i: str(i + 1), result))
        print(' '.join(wanted_indices))
    # Q2 big took 0m29,975s