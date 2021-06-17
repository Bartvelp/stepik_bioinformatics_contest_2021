from sys import argv
import zipfile

def find_all_substrings(haystack: str, needle: str):
    indices = []
    lastIndex = 0
    while (lastIndex != -1):
        newIndex = haystack.find(needle, lastIndex + 1)
        indices.append(newIndex)
        lastIndex = newIndex
    return indices[:-1] # Remove the last -1

if __name__ == "__main__":
    archive = zipfile.ZipFile(argv[1], 'r')
    lines = archive.read('input.txt').decode().splitlines()
    lines_with_pairs = lines[1:]
    needle_hay_pairs = zip(lines_with_pairs[::2], lines_with_pairs[1::2])
    for haystack, needle in needle_hay_pairs:
        all_needle_indices = find_all_substrings(haystack, needle)
        wanted_indices = list(map(lambda i: str(i + 1), all_needle_indices))
        print(' '.join(wanted_indices))
    print()
