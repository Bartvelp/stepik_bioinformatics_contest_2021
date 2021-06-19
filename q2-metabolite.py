from multiprocessing.dummy import Pool as ThreadPool
from sys import argv
import sys
import zipfile
import numpy as np
# import ray
# ray.init(num_cpus=8)

def chunks(l: list, n: int):
    # https://stackoverflow.com/a/1751478/5329317
    n = max(1, n)
    return list(l[i:i+n] for i in range(0, len(l), n))

def parse_problems(lines: list):
    problems = []
    problems_lines = chunks(lines, 4)
    for problem_lines in problems_lines:
        problem_lines = problem_lines[1:] # remove counts line
        metabolite_strings = problem_lines[0].strip().split(' ')
        metabolite_masses = np.unique(np.asarray(metabolite_strings, dtype=np.single))
        adducts_strings = problem_lines[1].strip().split(' ')
        adducts_masses = np.unique(np.asarray(adducts_strings, dtype=np.single))
        signal_strings = problem_lines[2].strip().split(' ')
        signal_masses = np.asarray(signal_strings, dtype=np.single)
        problems.append((metabolite_masses, adducts_masses, signal_masses))
    return problems

# @ray.remote
def find_optimal_ma_comb(signal: float, pos_metabolites: np.array, pos_adducts: np.array):
    best_delta = 10 ** 5 # eg infinity
    best_indices = None
    for ai, adduct in enumerate(pos_adducts):
        adduct_f = float(adduct)
        pos_weights = adduct_f + pos_metabolites 
        positive_pos_weights = pos_weights[pos_weights >= 0.0] # remove negative weights
        pos_deltas = positive_pos_weights - signal
        if np.amin(pos_deltas) < best_delta:
            mi = np.argmin(pos_deltas)
            best_indices = (mi, ai)
            if (np.amin(pos_deltas) == 0.0):
                return best_indices
    return best_indices


def create_weight_2darray(pos_metabolites: list, pos_adducts: list):
    weight_arr = np.zeros(shape=(len(pos_metabolites), len(pos_adducts)))

    for mi, metabolite in enumerate(pos_metabolites):
        for ai, adduct in enumerate(pos_adducts):
            combined_mass = metabolite + adduct
            if combined_mass < 0:
                combined_mass = 10**3
            weight_arr[mi, ai] = combined_mass
    return weight_arr


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
        signals = signals[:10]
        for signal in signals:
            optimal_comb = find_optimal_ma_comb(signal, pos_metabolites, pos_adducts)
            result_ids.append(optimal_comb)
    results = result_ids # ray.get(result_ids)

    for result in results:
        wanted_indices = list(map(lambda i: str(i + 1), result))
        print(' '.join(wanted_indices))
    # Q2 big took 0m29,975s