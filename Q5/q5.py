import sys
from multiprocessing import Pool

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
        exon = {
                "start": start,
                "end": end
                }
        exons.append(exon)
    return exons

def read_is_isoform(problem_isoform, isoform, delta):
    # First find the first matching exon, then it must be sequential
  
    first_real_exon_i = -1
    read_start, read_end = (problem_isoform[0]['start'], problem_isoform[0]['end'])
    for i, real_exon in enumerate(isoform):
        real_start = real_exon['start']
        real_end = real_exon['end']
        if read_start >= (real_start - delta): # Start is good
            if abs(read_end - real_end) <= delta: # 41 - 40 == 1
                # Exon found
                first_real_exon_i = i
                break
    if first_real_exon_i == -1: # First exon not found
        return False

    possible_real_exons = isoform[first_real_exon_i + 1:]

    if len(problem_isoform[1:]) > len(possible_real_exons):
        return False
    for problem_exon, real_exon in zip(problem_isoform[1:], possible_real_exons): # middle and last exons

        read_start = problem_exon['start']
        read_end = problem_exon['end']

        real_start = real_exon['start']
        real_end = real_exon['end']
        if problem_exon == problem_isoform[-1]: # isLast
            if abs(read_start - real_start) <= delta: # 30 - 31 = 1 <= 1
                if read_end <= (real_end + delta): # 41 <= 40 + 1
                    return True # last exon is good, report
        else: # both must match
            if abs(read_start - real_start) > delta: # 40 - 39
                return False
            if abs(read_end - real_end) > delta: # 60 - 61
                return False
    return False

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

isoforms = []
delta = 0

def find_options(problem_isoform):
    options = []
    for i, isoform in enumerate(isoforms):
        if read_is_isoform(problem_isoform, isoform, delta):
            options.append(i)
    return options

if __name__ == "__main__":
    isoforms, problem_isoforms, delta = parse_input(sys.argv[1])

    if sys.argv[2] != 'benchmark':
        results = []
        with Pool() as p:
            results = p.map(find_options, problem_isoforms)        

        # results = [ray.get(res_id) for res_id in result_ids]
        for all_options in results:
            if len(all_options) == 0:
                print('-1 0')
            else:
                print('{} {}'.format(all_options[0], len(all_options)))
    else:
        results = []
        
        for i, problem_isoform in enumerate(problem_isoforms):
            if i % 1 == 0:
                eprint('At i/totali: {}/{}'.format(i, len(problem_isoforms)))
            result = find_options(problem_isoform)
            results.append(result)
            
        for all_options in results:
            if len(all_options) == 0:
                print('-1 0')
            else:
                print('{} {}'.format(all_options[0], len(all_options)))