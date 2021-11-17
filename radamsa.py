import pyradamsa, subprocess, sys, os


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
    c_file_path = sys.argv[1]
    # sampleFile = sys.argv[2]
    c_file_gcov = c_file_path + '.c'
    
    silence_arg = ' >/dev/null 2>&1' # append to commands run so that it doesn't display in the terminal.
    clean_command = 'rm ' + c_file_path + '.c.gcov' + ' ' + c_file_path + '.gcda' + silence_arg
    command = 'gcov ' + c_file_path + silence_arg
    os.system(clean_command) # clean previous coverage files for fresh run.
    os.system(command) # running the gcov command at the start to generate the first gcov file.
    
    rad = pyradamsa.Radamsa()
    data = b'GET /auth?pass=HelloWorld HTTP1.1'
    fuzzed = rad.fuzz(data)
    print(fuzzed)


if __name__ == '__main__':
    main()