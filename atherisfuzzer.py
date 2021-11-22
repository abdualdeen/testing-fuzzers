import atheris, subprocess, sys, os, time

TRIALS = 5500
CFILE = '/home/vanishing/git/rapidfuzz-radamsa/test'

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

def testFunc(fuzz):
    result = subprocess.run([CFILE, fuzz], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if (result.returncode == 0):
        raise RuntimeError("Oooops!")

def main():
    atheris.Setup(sys.argv, testFunc)
    for _ in range(TRIALS):
        atheris.Fuzz()
    # print(atheris.Fuzz())

if __name__ == '__main__':
    main()