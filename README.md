# rapidfuzz-radamsa
This repo has files that are used to compare the fuzzingbook fuzzer with the pyradamsa fuzzer.

## Run/Setup
Make sure to compile the programs using the following command (gcc 11.1.0 was used):
`gcc --coverage -o triangle triangle.c & gcc --coverage -o calc calc.c & gcc --coverage -o quake_fast_inverse_sqrt quake_fast_inverse_sqrt.c`

Install the pyradamsa library in python.
`pip install pyradamsa`

Both programs were run on Linux. Both use a system command to suppress output in the console and to clean files for each trial that might be only applicable to Linux systems. (See fuzzingbookfuzzer.py line 132-134 for example)

