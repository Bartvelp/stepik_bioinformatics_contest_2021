import sys
from multiprocessing import Pool
import os

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def parse_input(fn):
    lines = open(fn).readlines()
    num_isoforms = int(lines[0].split(' ')[0])
    delta = int(lines[0].split(' ')[1])
    eprint("num iso, delta", num_isoforms, delta)

    lines = lines[1:]
    isoforms = []
    for isoform_i in range(num_isoforms):
        isoform_line = lines[isoform_i].strip()
        exons = parse_isoform(isoform_line)
        isoforms.append(exons)
    
    lines = lines[num_isoforms + 1:]
    problem_isoforms = []
    for problem_line in lines:
        problem_line = problem_line.strip()
        exons = parse_isoform(problem_line)
        problem_isoforms.append(exons)
    return isoforms, problem_isoforms, delta

def parse_isoform(isoform_line):
    exon_parts = isoform_line.split(',')
    exons = []
    for exon_str in exon_parts: # e.g. 10-20
        start, end = tuple(map(int, exon_str.split('-'))) # [10, 20]
        exon = (start, end)
        exons.append(exon)
    return exons

def calculate_s(isoform, read):
    # isoform = [(10, 20), (40, 50)]
    # read = [(10, 20), (21, 30), (40, 60)]
    total_exon_overlap = 0
    for read_exon in read:
        for isoform_exon in isoform:
            total_exon_overlap += find_overlap(read_exon, isoform_exon)
    pos_exon_overlap = calc_possible_overlap(read)

    # total overlap is 20
    isoform_introns = exons_2_introns(isoform)
    read_introns = exons_2_introns(read)

    total_intron_overlap = 0
    for read_intron in read_introns:
        for isoform_intron in isoform_introns:
            total_intron_overlap += find_overlap(read_intron, isoform_intron)
    pos_intron_overlap = calc_possible_overlap(read_introns)

    left = (2 / 3) * (total_exon_overlap / pos_exon_overlap)
    right = (1 / 3) * (total_intron_overlap / pos_intron_overlap)
    return left + right

def find_overlap(line_1, line_2):
    a, c = line_1
    b, d = line_2
    if (a > d or c < b):
        return 0
    else: # overlap
        overlap_left = max(a, b)
        overlap_right = min(c, d)
        return overlap_right - overlap_left

def calc_possible_overlap(isoform):
    total_overlap = 0
    for a, b in isoform:
        total_overlap += b - a
    return total_overlap

def exons_2_introns(exons):
    introns = []
    for i in range(len(exons) - 1): # the last exon has no intron after it
        _, exon_end = exons[i]
        exon_start, _ = exons[i + 1]
        introns.append((exon_end, exon_start))
    return introns

isoforms = []

def get_best_s(read):
    all_s = [calculate_s(isoform, read) for isoform in isoforms]
    best_s = max(all_s)
    return max(all_s), all_s.index(best_s)

if __name__ == "__main__":
    isoforms, reads, delta = parse_input(sys.argv[1])

    if sys.argv[2] != 'benchmark':
        results = []
        with Pool(min(os.cpu_count() - 1, 32)) as p:
            results = p.map(get_best_s, reads)        

        for best_s, i in results:
            print(i)
    else:
        for i, read in enumerate(reads):
            eprint("at i of n", i, len(reads))
            best_s, i = get_best_s(read)
            print(i)
