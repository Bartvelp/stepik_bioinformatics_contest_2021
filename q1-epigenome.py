from sys import argv
import zipfile

def parse_input(lines: list):
    """ Returns list of [{numSeq: 2, len: 2, seqs: ['0', '1', ...]}]
    """
    all_results = []
    curEntry = None
    for line in lines:
        line_parts = line.split(' ')
        if len(line_parts) == 2: # it's a header
            all_results.append(curEntry) # add the previous entry
            curEntry = {
                'numSeq': int(line_parts[0]),
                'len': int(line_parts[1]),
                'seqs': []
            }
        else: # it's not a header, so it's a sequence
            curEntry['seqs'].append(list(line))
    all_results.append(curEntry) # add the last entry

    return all_results[1:] # remove the first None entry

def find_states(sequence_entry: dict):
    """ Finds all states and their ordering of a sequence entry

    Returns:
    found_states: like  [['0', '1'], ...]
    state_history: like [0, 3, 2, 1]
    """
    found_states = [] # All previously found states
    state_history = [] # States used to build up the sequences
    columns = [list(column) for column in zip(*sequence_entry['seqs'])]
    for column in columns:
        if not column in found_states: # it is a new state
            found_states.append(column)
        state_history.append(found_states.index(column)) # add it to the state history

    return found_states, state_history

if __name__ == "__main__":
    input_path = argv[1]
    if input_path.endswith('.zip'):
        archive = zipfile.ZipFile(argv[1], 'r')
        lines = archive.read(argv[2]).decode().splitlines()[1:]
    elif input_path.endswith('.txt'):
        fh = open(input_path)
        lines = fh.read().splitlines()[1:]

    sequence_entries = parse_input(lines)
    for sequence_entry in sequence_entries:
        found_states, state_history = find_states(sequence_entry)
        print(len(found_states)) # Print number of unique states
        wanted_indices = list(map(lambda i: str(i + 1), state_history))
        print(' '.join(wanted_indices))

    print()