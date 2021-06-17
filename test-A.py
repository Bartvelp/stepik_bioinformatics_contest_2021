from sys import argv
import zipfile

if __name__ == "__main__":
    archive = zipfile.ZipFile(argv[1], 'r')
    lines = archive.read('input.txt').decode().splitlines()
    lines_with_nums = lines[1:]
    for line in lines_with_nums:
        parts = line.split(' ')
        print(int(parts[0]) + int(parts[1]))
    print()