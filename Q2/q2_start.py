import sys
from multiprocessing import Pool

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def parse_input(fn):
    lines = open(fn).readlines()
    t = int(lines[0])
    test_cases = []
    cur_test_case = [[], []] # positive, negative
    isPositive = False
    for line in lines[2:]:
        line = line.strip()
        if len(line.split(' ')) == 2:
            test_cases.append(cur_test_case)
            cur_test_case = [[], []]
        else:
            if line == '-':
                isPositive = False
            elif line == '+':
                isPositive = True
            else: # it's a sequence
                if isPositive:
                    cur_test_case[0].append(line)
                else:
                    cur_test_case[1].append(line)
    # append the last testcase
    test_cases.append(cur_test_case)
    eprint('Num testcases are:', t, len(test_cases))
    eprint('Length of seq', len(cur_test_case[0][0]))
    return test_cases

def solve_test_case(test_case):
    # testcase = [[], []] positive genomes, negative genomes
    l = len(test_case[0][0])
    found_good_char = [0] * l

    postive_genomes = test_case[0]
    negative_t_genomes = transpose_genomes(test_case[1])

    # eprint('pos mut', found_good_char)
    # eprint('pos genome', postive_genomes)
    # eprint('neg transposed genome', negative_t_genomes)

    for postive_genome in postive_genomes:
        for i, negative_t_genome in enumerate(negative_t_genomes):
            good_chars = list(negative_t_genome)
            bad_char = postive_genome[i]
            found_good_char[i] += get_char_score(bad_char, good_chars)

    eprint('pos mut after', found_good_char) # [3, 5, 9], [3], []
    lowest_indices = find_lowest_indices(found_good_char, 10)
    eprint('lowest', lowest_indices)
    return (min(lowest_indices), max(lowest_indices))
    
def find_lowest_indices(numbers: list, num_el = 5):
    sorted_numbers = sorted(numbers)
    lowest_indices = []
    for low_num in sorted_numbers:
        low_indices = [i for i, num in enumerate(numbers) if num == low_num]
        lowest_indices += low_indices
        if len(lowest_indices) > num_el - 1:
            break
    return lowest_indices


def get_char_score(bad_char, good_chars):
    # bad_char = 'A' | 'C' | 'T' | 'G'
    # good chars = ['A', 'C', 'A', 'C', 'T']
    ratio_bad_char = good_chars.count(bad_char) / len(good_chars) # 1 / 4 = 0.25
    points = round(ratio_bad_char * 4)
    return points


def transpose_genomes(genomes: list):
    # genomes is list of string
    l = len(genomes[0])
    transposed_genomes = [''] * l
    for i in range(l):
        for genome in genomes:
            good_char = genome[i]
            transposed_genomes[i] += genome[i]
    return transposed_genomes

if __name__ == "__main__":
    test_cases = parse_input(sys.argv[1])
    
    # benchmark
    for i, test_case in enumerate(test_cases):
        awnser = solve_test_case(test_case)
        eprint('At i', i)
        print(' '.join(map(str, awnser)))
