import os
import subprocess
import random
import sys
import time

# === Functions in this section are imported from the fuzzing book. Some have been modified slightly=== #
class Fuzzer(object):
    def __init__(self):
        pass

    def fuzz(self):
        """Return fuzz input"""
        return ""

class RandomFuzzer(Fuzzer):
    def __init__(self, min_length=10, max_length=100,
                 char_start=32, char_range=32):
        """Produce strings of `min_length` to `max_length` characters
           in the range [`char_start`, `char_start` + `char_range`]"""
        self.min_length = min_length
        self.max_length = max_length
        self.char_start = char_start
        self.char_range = char_range

    def fuzz(self):
        string_length = random.randrange(self.min_length, self.max_length + 1)
        out = ""
        for i in range(0, string_length):
            out += chr(random.randrange(self.char_start,
                                        self.char_start + self.char_range))
        return out


def delete_random_character(s):
    """Returns s with a random character deleted"""
    if s == "":
        return s

    pos = random.randint(0, len(s) - 1)
    # print("Deleting", repr(s[pos]), "at", pos)
    return s[:pos] + s[pos + 1:]

def insert_random_character(s):
    """Returns s with a random character inserted"""
    pos = random.randint(0, len(s))
    random_character = chr(random.randrange(32, 127))
    # print("Inserting", repr(random_character), "at", pos)
    return s[:pos] + random_character + s[pos:]

def flip_random_character(s):
    """Returns s with a random bit flipped in a random position"""
    if s == "":
        return s

    pos = random.randint(0, len(s) - 1)
    c = s[pos]
    bit = 1 << random.randint(0, 6)
    new_c = chr(ord(c) ^ bit)
    # while (chr(0) in new_c):
    #     new_c = chr(ord(c) ^ bit)
    # print("Flipping", bit, "in", repr(c) + ", giving", repr(new_c))
    return s[:pos] + new_c + s[pos + 1:]


def mutate(s):
    """Return s with a random mutation applied"""
    mutators = [
        delete_random_character,
        insert_random_character,
        flip_random_character
    ]
    mutator = random.choice(mutators)
    # print(mutator)
    return mutator(s) 

def read_gcov_coverage(c_file):
    gcov_file = c_file + ".gcov"
    coverage = set()
    with open(gcov_file) as file:
        for line in file.readlines():
            elems = line.split(':')
            covered = elems[0].strip()
            line_number = int(elems[1].strip())
            if covered.startswith('-') or covered.startswith('#'):
                continue
            coverage.add(line_number)
    return coverage

class MutationFuzzer(Fuzzer):
    def __init__(self, seed, min_mutations=2, max_mutations=10):
        self.seed = seed
        self.min_mutations = min_mutations
        self.max_mutations = max_mutations
        self.reset()

    def reset(self):
        self.population = self.seed
        self.seed_index = 0
        
    def mutate(self, inp):
        return mutate(inp)

    def create_candidate(self):
        candidate = random.choice(self.population)
        trials = random.randint(self.min_mutations, self.max_mutations)
        for i in range(trials):
            candidate = self.mutate(candidate)
        return candidate
    
    def fuzz(self):
        if self.seed_index < len(self.seed):
            # Still seeding
            self.inp = self.seed[self.seed_index]
            self.seed_index += 1
        else:
            # Mutating
            self.inp = self.create_candidate()
        return self.inp

# === ... === #

TRIALS = 5500

def main():
    startTime = time.time()
    c_file_path = sys.argv[1] # take the path of the executable given from the command line.
    seed = [sys.argv[2]]
    c_file_gcov = c_file_path + '.c' # append '.c' to that so that the read_gcov_coverage() function can recognize it and read the gcov file.
    random.seed() 
    
    silence_arg = ' >/dev/null 2>&1' # append to commands run so that it doesn't display in the terminal.
    clean_command = 'rm ' + c_file_path + '.c.gcov' + ' ' + c_file_path + '.gcda' + silence_arg
    command = 'gcov ' + c_file_path + silence_arg + silence_arg
    os.system(clean_command) # clean previous coverage files for fresh run.
    os.system(command) # running the gcov command at the start to generate the first gcov file.
    
    mutation = MutationFuzzer(seed=seed, min_mutations=2, max_mutations=5)
    prev = read_gcov_coverage(c_file_gcov) # reading the initial gcov file for later comparison.
    
    for i in range(TRIALS):
        fuzz = mutation.fuzz()
        
        while (chr(0) in fuzz): # discard fuzz that has the null character in it to avoid null byte error.
            fuzz = mutation.fuzz()
            
        if (i == 0):
            result = subprocess.run([c_file_path, seed[0]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        else:
            result = subprocess.run([c_file_path, fuzz], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        os.system(command) # generate new gcov file for comparison to previous.
        curr = read_gcov_coverage(c_file_gcov)
        if (result.returncode == 0 and not i == 0 and fuzz not in mutation.population and not len(prev) == len(curr)):
            mutation.population.append(fuzz)
            prev = curr
        
        
    os.system(command)
    print('Population: ', mutation.population)
    print('Trials run: ', TRIALS)
    print(sorted(read_gcov_coverage(c_file_gcov)), ' lines: ', len(read_gcov_coverage(c_file_gcov)))
    print("--- %s seconds ---" % (time.time() - startTime))
    
    

if __name__ == '__main__':
    main()
