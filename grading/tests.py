import os
import sys
import subprocess
import json
import re

tests_to_run = []
configs = dict()
configs['outputOnly'] = False

results = dict()
results['tests'] = dict()
results['compile'] = dict()


def main():
    parse_configs()
    parse_args()
    make_dirs()

    if get_num_tests() > len(tests_to_run) > 0:
        num_tests = len(tests_to_run)
    else:
        num_tests = get_num_tests()

    print('Starting ' + str(num_tests) + ' tests.')

    set_tests_to_run()

    run_tests()

def make_dirs():
    call('rm -rf out')
    call('rm -rf vout')
    call('rm -rf logs')
    call('mkdir out')
    call('mkdir vout')
    call('mkdir logs')

def run_tests():
    global tests_to_run
    global results
    call('rm -rf .temp')
    call('mkdir .temp')
    os.chdir('.temp')

    for test in tests_to_run:
        print('~~~~~~~~~~~~~~~~~~' + test + '~~~~~~~~~~~~~~~~~~')
        results[test] = dict()
        results[test]['warnings'] = dict()
        results[test]['errors'] = dict()
        results[test]['output'] = dict()
        call('cp ../*.cpp .')
        call('cp ../*.h .')
        call('cp ../cpp/' + append_suffix(test, '.cpp') + ' .')
        call('cp ../in/' + append_suffix(test, '.in') + ' .')
        call('cp ../Makefile_test' + ' .')
        print('Compiling ' + test + '...', end='\r')
        compile_program_specified(test)
        if results[test]['warnings'] == 0 and results[test]['errors'] == 0:
            print('Compiling ' + test + '... ✓')
        else:
            print('Compiling ' + test + '... ✘')
        print('Running ' + test + '...', end='\r')
        run_program_specified(test)
        print('Running ' + test + '... ✓')
        call('cp ' + append_suffix(test, '.log') + ' ../logs/' + append_suffix(test, '.log'))
        # call('rm *')
        print()
        print()

    os.chdir('..')
    # print(num_tests, configs, tests_to_run)


def run_program_specified(test):
    valgrind_file = '../vout/' + append_suffix(test, '.vout')
    output_file = '../out/' + append_suffix(test, '.out')
    print('valgrind --log-file="' + valgrind_file + '" ' + test + ' < ' + append_suffix(test, '.in') + ' &> ' + output_file)
    call('valgrind --log-file="' + valgrind_file + '" ' + test + ' < ' + append_suffix(test, '.in') + ' &> ' + output_file)


def set_tests_to_run():
    global tests_to_run
    if len(tests_to_run) == 0:
        for i in range (1, get_num_tests() + 1):
            tests_to_run.append(to_string_default(i))


def parse_configs():
    global configs
    check_file('./config.json')
    with open('./config.json') as jsonFile:
        configs = json.load(jsonFile)


# compiles a program based on a specific test (name of the program), with a specified filename (our custom makefile)
# makes test.log in curr directory
def compile_program_specified(filename):
    call('make --file=Makefile_test ' + filename + ' &> ' + append_suffix(filename, '.log'))
    global results
    results[filename]['warnings'] = 0
    results[filename]['errors'] = 0

    with open(append_suffix(filename, '.log'), 'r') as make_logs:
        for line in make_logs:
            regex_find_warnings = re.findall(r"(\d*) warnings generated.", line)
            regex_find_errors = re.findall(r"(\d*) errors generated.", line)
            if len(regex_find_warnings) > 0:
                print(regex_find_warnings[0] + ' warnings! Check make logs (test+.log)')
                results[filename]['warnings'] = regex_find_warnings
            if len(regex_find_errors) > 0:
                print(regex_find_errors[0] + ' errors! Check make logs (test+.log)')
                results[filename]['errors'] = regex_find_errors

    if not os.path.isfile('./' + filename):
        print('Error: Executable not made! Check make logs (make.log)')


# compiles a program based on the generic 'make' command, without a specified filename
def compile_program():
    call('make &> make.log')
    global results
    with open('./make.log', 'r') as make_logs:
        for line in make_logs:
            regex_find_warnings = re.findall(r"(\d*) warnings generated.", line)
            regex_find_errors = re.findall(r"(\d*) errors generated.", line)
            if len(regex_find_warnings) > 0:
                print(regex_find_warnings[0] + ' warnings! Check make logs (test+.log)')
                results['compile']['warnings'] = regex_find_warnings
            if len(regex_find_errors) > 0:
                print(regex_find_errors[0] + ' errors! Check make logs (test+.log)')
                results['compile']['errors'] = regex_find_errors

    if not os.path.isfile('./' + str(configs['makeExec'])):
        print('Error: Executable not made! Check make logs (make.log)')
        exit(1)


def parse_args():
    global configs
    global tests_to_run
    i = 1
    if len(sys.argv) > 1:
        if sys.argv[1] == '-clean':
            print('Deleting folders', end='\r')
            delete_folders()
            print('Deleting folders ✓', end='\n')
            exit()
        if sys.argv[1] == '-output':
            print('setting to true')
            configs['outputOnly'] = True
            i = 2
        tests_to_run = sys.argv[i:]

def delete_folders():
    print('deleting folders')
    # call('rm -rf out')
    # call('rm -rf vout')
    # call('rm -rf diff')

def append_suffix(test, suffix):
    return test + suffix;

def to_string(test_num, suffix):
    if test_num < 10:
        return 'test0' + str(test_num) + suffix
    else:
        return 'test' + str(test_num) + suffix

def to_string_default(test_num):
    if test_num < 10:
        return 'test0' + str(test_num)
    else:
        return 'test' + str(test_num)

def check_file(file_path):
    if not os.path.isfile(file_path):
        raise RuntimeError(file_path + ' not found')

def get_num_tests():
    return len(next(os.walk('./in/'))[2])


def call(command):
    subprocess.call(command, shell=True)


if __name__ == '__main__':
    main()
