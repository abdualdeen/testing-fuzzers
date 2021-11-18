from rapidfuzz import fuzz

def read_gcov_coverage(cFile):
    gcov_file = cFile + ".gcov"
    coverage = set()
    with open(gcov_file) as file:
        for line in file.readlines():
            elems = line.split(':')
            covered = elems[0].strip()
            line_number = int(elems[1].strip())
            if covered.startswith('-') or covered.startswith('#'):
                continue
            coverage.add(('calc.c', line_number)) # originally passed c_file for the name, but for better readability, it was hardcoded to 'calc.c'
    return coverage



def main():
    print(fuzz.ratio('hello', 'hello'))




if __name__ == '__main__':
    main()