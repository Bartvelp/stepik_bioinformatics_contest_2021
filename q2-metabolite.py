from multiprocessing.dummy import Pool as ThreadPool
from sys import argv
import zipfile
import ray
ray.init(num_cpus=8)

def chunks(l: list, n: int):
    # https://stackoverflow.com/a/1751478/5329317
    n = max(1, n)
    return list(l[i:i+n] for i in range(0, len(l), n))

def parse_problems(lines: list):
    problems = []
    problems_lines = chunks(lines, 4)
    for problem_lines in problems_lines:
        problem_lines = problem_lines[1:] # remove counts line
        metabolite_masses = list(map(float, problem_lines[0].strip().split(' ')))
        adducts_masses = list(map(float, problem_lines[1].strip().split(' ')))
        signal_masses = list(map(float, problem_lines[2].strip().split(' ')))
        problems.append((metabolite_masses, adducts_masses, signal_masses))
    return problems

def find_optimal_ma_comb(signal: float, pos_metabolites: list, pos_adducts: list):
    best_delta = 2**10 # e.g. infinity
    best_comb = (0, 0) # indices
    for metabolite in pos_metabolites:
        for adduct in pos_adducts:
            combined_mass = metabolite + adduct
            if combined_mass < 0: # Can't be negative
                continue
            delta = abs(combined_mass - signal)
            if delta < best_delta:
                best_delta = delta
                best_comb = (pos_metabolites.index(metabolite), pos_adducts.index(adduct))
    return best_comb

@ray.remote
def solve_problem(problem: tuple):
    signal_results = []
    metabolite_m, adducts_m, signal_m = problem
    for signal in signal_m:
        optimal_comb = find_optimal_ma_comb(signal, metabolite_m, adducts_m)
        wanted_indices = list(map(lambda i: str(i + 1), optimal_comb))
        signal_results.append(wanted_indices)
    return signal_results


if __name__ == "__main__":
    input_path = argv[1]
    if input_path.endswith('.zip'):
        archive = zipfile.ZipFile(argv[1], 'r')
        lines = archive.read(argv[2]).decode().splitlines()[1:]
    elif input_path.endswith('.txt'):
        fh = open(input_path)
        lines = fh.read().splitlines()[1:]
    problems = parse_problems(lines)
    ray.put(problems)
    # Solve each problem
    results_ids = []
    for problem in problems:
        results_ids.append(solve_problem.remote(problem))
    results = ray.get(results_ids)
    for problem_results in results:
        for signal_result in problem_results:
            print(' '.join(signal_result))
    # Q2 big took 0m29,975s