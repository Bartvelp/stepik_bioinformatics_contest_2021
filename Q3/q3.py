import sys
import random
import statistics
import os
# import numpy as np
from multiprocessing import Pool

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def parse_input(fn):
    lines = open(fn).readlines()
    
    num_communities = int(lines[0])
    eprint("Num communites", num_communities)
    num_people = 0
    all_communities = []
    all_days = []
    cur_day = []

    for line in lines[1:]:
        line = line.strip()
        line_parts = line.split(' ')
        if len(line_parts) == 3:
            person_a = int(line_parts[0])
            person_b = int(line_parts[1])
            trans_prob = float(line_parts[2])
            cur_day.append((person_a, person_b, trans_prob))
        else:
            if len(cur_day) > 0:
                all_days.append(cur_day)
            cur_day = []
            if len(line_parts) == 2: # new comm
                if len(all_days) > 0:
                    all_communities.append((num_people, all_days))
                num_people = int(line_parts[0])
                all_days = []
    if len(cur_day) > 0:
        all_days.append(cur_day)
    all_communities.append((num_people, all_days))

    return all_communities

def find_number_infected_once(person, all_days, num_people):
    previous_infected_people = set([person])
    new_infected_people = set()
    for transmissions in all_days:
        for transmission in transmissions:
            person_a, person_b, trans_prob = transmission
            if person_a in previous_infected_people:
                if trans_prob == 1 or random.random() < trans_prob:
                    new_infected_people.add(person_b)
        previous_infected_people = set.union(previous_infected_people, new_infected_people)
    return len(previous_infected_people)
# 518170
# 100000

def find_number_infected(person, all_days, num_people):
    results = [find_number_infected_once(person, all_days, num_people) for _ in range(1)]
    if person % 1000 == 0:
        eprint(person, results)
    return statistics.median(results)

def all_days2_transmissions(all_days):
    all_transmissions = []
    for day in all_days: # [(1, 2, 1.0), (1, 3, 1.0)]
        all_transmissions += day
    return all_transmissions

def find_pos_transmissions(all_transmissions, person):
    pos_transmissions = []
    pos_infected = set([person])
    for transmission in all_transmissions:
        person_a, person_b, trans_prob = transmission
        if person_a in pos_infected and trans_prob > 0.1:
            pos_infected.add(person_b)
            pos_transmissions.append(transmission)
    return pos_transmissions


def find_most_infectious_person(community):
    num_people, all_days = community
    
    max_infected = float('-inf')
    max_person = -1

    for person in range(1, min(num_people + 1, 2000)):
        num_infected = find_number_infected(person, all_days, num_people)
        if num_infected > max_infected:
            max_person = person
            max_infected = num_infected
    eprint('Best person:', max_person, max_infected, num_people)
    return max_person

if __name__ == "__main__":
    all_communities = parse_input(sys.argv[1])


    if sys.argv[2] != 'benchmark':
        results = []
        with Pool(min(os.cpu_count() - 1, 32)) as p:
            results = p.map(find_most_infectious_person, all_communities[:-1])

        for res in results:
            print(res)
    else:
        for community in all_communities:
            print(find_most_infectious_person(community))

# 21 seconds for python3
# 4.5 for pypy3
# 1.5 for pypy3 multi