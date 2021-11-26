import pyradamsa, subprocess, sys, os, time

TRIALS = 5500

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
            coverage.add(line_number) # originally passed c_file for the name, but for better readability, it was hardcoded to 'calc.c'
    return coverage


def main():
    startTime = time.time()
    c_file_path = sys.argv[1]
    seed = bytes(sys.argv[2], 'UTF-8')
    c_file_gcov = c_file_path + '.c'
    
    silence_arg = ' >/dev/null 2>&1' # append to commands run so that it doesn't display in the terminal.
    clean_command = 'rm ' + c_file_path + '.c.gcov' + ' ' + c_file_path + '.gcda' + silence_arg
    command = 'gcov ' + c_file_path + silence_arg
    os.system(clean_command) # clean previous coverage files for fresh run.
    os.system(command) # running the gcov command at the start to generate the first gcov file.
    
    rad = pyradamsa.Radamsa()
    prev = read_gcov_coverage(c_file_gcov) # reading the initial gcov file for later comparison.
    pop = [seed]
    
    for i in range(TRIALS):
        fuzz = rad.fuzz(seed)

        while (b'\x00' in fuzz): # discard fuzz that has the null character in it to avoid null byte error.
           fuzz = rad.fuzz(seed)
           
        if (i == 0):
            result = subprocess.run([c_file_path, seed], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            result = subprocess.run([c_file_path, fuzz], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
        os.system(command) # generate new gcov file for comparison to previous.
        curr = read_gcov_coverage(c_file_gcov)
        if ((result.returncode) == 0 and not (i == 0) and (fuzz not in pop) and not (len(prev) == len(curr))):
            pop.append(fuzz)
            prev = curr
        
        
    os.system(command)
    print('Population: ', pop)
    print('Trials run: ', TRIALS)
    print(sorted(read_gcov_coverage(c_file_gcov)), ' lines: ', len(read_gcov_coverage(c_file_gcov)))
    print("--- %s seconds ---" % (time.time() - startTime))



if __name__ == '__main__':
    main()