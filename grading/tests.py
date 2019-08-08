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

    if get_num_tests() > len(tests_to_run) > 0:
        num_tests = len(tests_to_run)
    else:
        num_tests = get_num_tests()

    print('Starting ' + str(num_tests) + ' tests.')

    print('Compiling...', end='\r')
    compile_program()
    print('Compiling... ✓')

    set_tests_to_run()


    # print(num_tests, configs, tests_to_run)

def set_tests_to_run():
    global tests_to_run
    if len(tests_to_run) == 0:
        for i in range (1, get_num_tests() + 1):
            tests_to_run.append(to_string_default(i))

    print(tests_to_run)
    exit(1)

# def run_tests():


def parse_configs():
    global configs
    check_file('./config.json')
    with open('./config.json') as jsonFile:
        configs = json.load(jsonFile)


def compile_program():
    call('make &> make.logs')
    global results
    with open('./make.logs', 'r') as make_logs:
        for line in make_logs:
            regex_find_warnings = re.findall(r"(\d*) warnings generated.", line)
            regex_find_errors = re.findall(r"(\d*) errors generated.", line)
            if len(regex_find_warnings) > 0:
                print(regex_find_warnings[0] + ' warnings! Check make logs (make.logs)')
                results['compile']['warnings'] = regex_find_warnings
            if len(regex_find_errors) > 0:
                print(regex_find_errors[0] + ' errors! Check make logs (make.logs)')
                results['compile']['errors'] = regex_find_errors

    if not os.path.isfile('./' + str(configs['makeExec'])):
        print('Executable not made! Check make logs (make.logs)')
        print(results)
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
