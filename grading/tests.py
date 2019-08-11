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

    if num_tests == 1:
        print('Starting ' + str(num_tests) + ' test.' )
    else:
        print('Starting ' + str(num_tests) + ' tests.' )

    set_tests_to_run()

    run_tests()

    test_summary()


def test_summary():
    global results
    global tests_to_run
    print('Test Summary:')
    for test in tests_to_run:
        print(test)
        failed = False
        if results['tests'][test]['errors'] != 0:
            print('\t' + str(results['tests'][test]['errors']) + ' errors ✘ (did not compile)')
            failed = True
        if results['tests'][test]['warnings'] != 0:
            print('\t' + str(results['tests'][test]['warnings']) + ' warnings ✘')
            failed = True
        if not results['tests'][test]['output']:
            print('\tOutput ✘')
            failed = True
        if results['tests'][test]['memLeaks'] != 0:
            print('\t' + str(results['tests'][test]['memLeaks']) + ' bytes definitely lost ✘')
        if results['tests'][test]['memErrors'] != 0:
            print('\t' + str(results['tests'][test]['memErrors']) + ' memory errors ✘')

        if not failed:
            print('\tPassed '+ test +' ✓')


def make_dirs():
    call('rm -rf out')
    call('rm -rf vout')
    call('rm -rf logs')
    call('rm -rf diff')
    call('mkdir out')
    call('mkdir vout')
    call('mkdir logs')
    call('mkdir diff')

def run_tests():
    global tests_to_run
    global results
    call('rm -rf .temp')
    call('mkdir .temp')
    os.chdir('.temp')

    for test in tests_to_run:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~'+ test +'~~~~~~~~~~~~~~~~~~~~~~~~~')
        results['tests'][test] = dict()
        results['tests'][test]['warnings'] = 0
        results['tests'][test]['errors'] = 0
        results['tests'][test]['memLeaks'] = 0  # 0 == success
        results['tests'][test]['memErrors'] = 0 # 0 == success
        results['tests'][test]['output'] = True     # true == success
        results['tests'][test]['segfault'] = False     # false == success
        call('cp ../*.cpp .')
        call('cp ../*.h .')
        call('cp ../cpp/' + append_suffix(test, '.cpp') + ' .')
        call('cp ../in/' + append_suffix(test, '.in') + ' .')
        call('cp ../Makefile_test' + ' .')
        print('Compiling ' + test + '...', end='\r')
        compile_program_specified(test)
        print_compile_result(test)

        if not os.path.isfile('./' + test):
            print('Error: Executable not made! Aborting ' + test + '.')
        else:
            print('Running ' + test + '...', end='\r')
            run_program_specified(test)
            print('Running ' + test + '... ✓')
            print('Comparing ' + test + '...', end='\r')
            compare_output(test)
            
            if results['tests'][test]['output']:
                print('Comparing ' + test + '... ✓')
            else:
                print('Comparing ' + test + '... ✘')
                print_compare_failure(test)

            print('Valgrind ' + test + '...', end='\r')
            check_memory(test)
            print_valigrnd_result(test)

        print()

    os.chdir('..')
    # print(num_tests, configs, tests_to_run)

############## Run programs
# Actually runs valgrind inline (so no need to do it twice!)
def run_program_specified(test):
    valgrind_file = '../vout/' + append_suffix(test, '.vout')
    output_file = '../out/' + append_suffix(test, '.out')
    call('valgrind --log-file="' + valgrind_file + '" ' + test + ' < ' + append_suffix(test, '.in') + ' &> ' + output_file)



############## Compile programs

# compiles a program based on a specific test (name of the program), with a specified filename (our custom makefile)
# makes test.log in curr directory
def compile_program_specified(test):
    call('make --file=Makefile_test ' + test + ' &> ' + append_suffix(test, '.log'))
    global results
    results['tests'][test]['warnings'] = 0
    results['tests'][test]['errors'] = 0

    with open(append_suffix(test, '.log'), 'r') as make_logs:
        for line in make_logs:
            regex_find_warnings = re.findall(r"(\d*) warnings generated.", line)
            regex_find_errors = re.findall(r"(\d*) errors generated.", line)
            if len(regex_find_warnings) > 0:
                print(regex_find_warnings[0] + ' warnings! Check make logs (logs/' + append_suffix(test, '.log)'))
                results['tests'][test]['warnings'] = regex_find_warnings[0]
            if len(regex_find_errors) > 0:
                print(regex_find_errors[0] + ' errors! Check make logs (logs/' + append_suffix(test, '.log)'))
                results['tests'][test]['errors'] = regex_find_errors[0]

    call('cp ' + append_suffix(test, '.log') + ' ../logs/' + append_suffix(test, '.log'))


# compiles a program based on the generic 'make' command, without a specified filename
def compile_program():
    call('make &> make.log')
    global results
    with open('./make.log', 'r') as make_logs:
        for line in make_logs:
            regex_find_warnings = re.findall(r"(\d*) warnings generated.", line)
            regex_find_errors = re.findall(r"(\d*) errors generated.", line)
            if len(regex_find_warnings) > 0:
                print(regex_find_warnings[0] + ' warnings! Check make logs (logs/' + append_suffix(test, '.log)'))
                results['compile']['warnings'] = regex_find_warnings
            if len(regex_find_errors) > 0:
                print(regex_find_errors[0] + ' errors! Check make logs (logs/' + append_suffix(test, '.log)'))
                results['compile']['errors'] = regex_find_errors

    if not os.path.isfile('./' + str(configs['makeExec'])):
        print('Error: Executable not made! Check make logs (make.log)')
        exit(1)

############## Checkers / Verifiers

def check_memory(test):
    global results
    valgrind_file = '../vout/' + append_suffix(test, '.vout')
    with open(valgrind_file, 'r') as valgrind_logs:
        for line in valgrind_logs:
            regex_find_issues = re.findall(r"==[0-9]*== All heap blocks were freed -- no leaks are possible", line)
            regex_find_errors = re.findall(r"==[0-9]*== ERROR SUMMARY: (\d*) errors from (\d*) contexts", line) 
            regex_find_definitely_lost = re.findall(r"==[0-9]*==    definitely lost: (\d{1,3}(?:,\d{3})*) bytes in (\d{1,3}(?:,\d{3})*) blocks", line)
            regex_find_indirectly_lost = re.findall(r"==[0-9]*==    indirectly lost: (\d{1,3}(?:,\d{3})*) bytes in (\d{1,3}(?:,\d{3})*) blocks", line)
            regex_find_possibly_lost = re.findall(r"==[0-9]*==    possibly lost: (\d{1,3}(?:,\d{3})*) bytes in (\d{1,3}(?:,\d{3})*) blocks", line)

            for num in regex_find_definitely_lost:
                (a, b) = num
                if a != '0':
                    results['tests'][test]['memLeaks'] = int(a)

            for num in regex_find_errors:
                (a, b) = num
                if a != '0':
                    results['tests'][test]['memErrors'] = int(a)



def compare_output(test):
    global results

    output_file = '../out/' + append_suffix(test, '.out')
    reference_file = '../ref/' + append_suffix(test, '.ref')
    diff_file = '../diff/' + append_suffix(test, '.diff')
    call('touch ' + diff_file)
    call('diff -EZBwB ' + output_file + ' ' + reference_file + ' &> ' + diff_file)

    if os.stat(diff_file).st_size != 0:
        results['tests'][test]['output'] = False

############## Print Results
        
def print_compile_result(test):
    if results['tests'][test]['warnings'] == 0 and results['tests'][test]['errors'] == 0:
        print('Compiling ' + test + '... warnings ✓ errors ✓')
    elif results['tests'][test]['warnings'] != 0 and results['tests'][test]['errors'] == 0:
        print('Compiling ' + test + '... warnings ✘ errors ✓')
    elif results['tests'][test]['warnings'] == 0 and results['tests'][test]['errors'] != 0:
        print('Compiling ' + test + '... warnings ✓ errors ✘')
    else:
        print('Compiling ' + test + '... warnings ✘ errors ✘')

def print_compare_failure(test):
    output_file = '../out/' + append_suffix(test, '.out')
    reference_file = '../ref/' + append_suffix(test, '.ref')
    diff_file = '../diff/' + append_suffix(test, '.diff')
    print('            ~~~expected (' + 'ref/' + append_suffix(test, '.ref)') + '~~~')
    call('head -5 ' + reference_file)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('             ~~~actual (' + 'out/' + append_suffix(test, '.out)') + '~~~')
    call('head -5 ' + output_file)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('              ~~~diff (' + 'diff/' + append_suffix(test, '.diff)') + '~~~')
    call('head -5 ' + diff_file)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

def print_valigrnd_result(test):
    global results
    if results['tests'][test]['memLeaks'] != 0 or results['tests'][test]['memErrors'] != 0:
        print('Valgrind ' + test + '... ✘')
    else:
        print('Valgrind ' + test + '... ✓')

    if  results['tests'][test]['memLeaks'] != 0:
        print('\tLeaks ' + test + '... ✘ (' + str(results['tests'][test]['memLeaks']) + ' bytes)')
    else:
        print('\tLeaks ' + test + '... ✓')

    if  results['tests'][test]['memErrors'] != 0:
        print('\tErrors ' + test + '... ✘ (' + str(results['tests'][test]['memErrors']) + ' errors)')
    else:
        print('\tErrors ' + test + '... ✓')

############## Utilities

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
