#!/usr/bin/python
# -*- coding: UTF-8 -*-

import subprocess
import sys
import os
import json

configs = {}


def main():
    print('options: -clean')
    parse_args()
    print('Parsing configs', end='\r')
    parse_configs()
    print('Parsing configs ✓')

    print('Checking prerequisites', end='\r')
    check_prerequisites()
    print('Checking prerequisites ✓',)

    print('Generating folders', end='\r')
    generate_folders()
    print('Generating folders ✓')

    print('Checking tests', end='\r')
    check_tests()
    print('Checking tests ✓')

    print('Making reference (' + str(configs['numTests']) + ' tests)')
    if 'compile' in configs:
        if configs['compile']:
            make_reference_type_1()
        else:
            make_reference_type_2()
    print('Made reference ✓')

    print('Making config JSON', end='\r')
    make_JSON()
    print('Making config JSON ✓')

    print('Copying tests', end='\r')
    copy_tests()
    print('Copying tests ✓')

    if 'toDistribute' in configs:
        print('Making distribution test (' + configs['toDistribute'] + ')', end='\r')
        make_distribute(configs['toDistribute'])
        print('Making distribution test (' + configs['toDistribute'] + ') ✓')

    print()
    print('All files made, found in ./grading.')

def copy_tests():
    call('cp tests.py ./grading/')

def make_JSON():
    toJsonify = {
        "makeExec": str(configs['makeExec'])
    }

    with open('./grading/config.json', 'w') as file:
        json.dump(toJsonify, file, indent=4)

def parse_args():
    if len(sys.argv) > 1:
        if sys.argv[1] == '-clean':
            print('Deleting folders', end='\r')
            delete_folders()
            print('Deleting folders ✓', end='\n')
            exit()


def check_prerequisites():
    dir_prereqs_type_1 = ['./ref', './cpp', './in']
    dir_prereqs_type_2 = ['./ref', './in']
    file_prereqs_type_1 = ['./config/config.json', './config/Makefile']
    file_prereqs_type_2 = ['./config/config.json']

    dirs_to_check = None
    files_to_check = None
    if configs['compile']:
        dirs_to_check = dir_prereqs_type_1
        files_to_check = file_prereqs_type_1
    else:
        dirs_to_check = dir_prereqs_type_2
        files_to_check = file_prereqs_type_2

    for dir_name in dirs_to_check:
        check_dir(dir_name)

    for file_name in files_to_check:
        check_file(file_name)


def generate_folders():
    call('rm -rf grading')
    call('rm -rf temp')
    call('rm -rf distribute')
    call('mkdir temp')
    call('mkdir grading')
    call('mkdir grading/in')
    call('mkdir grading/ref')


def parse_configs():
    global configs
    check_file('./config/config.json')
    with open('./config/config.json') as jsonFile:
        configs = json.load(jsonFile)


# https://stackoverflow.com/questions/2632205/how-to-count-the-number-of-files-in-a-directory-using-python
def check_tests():
    global configs
    files = next(os.walk('./in/'))[2]
    if len(files) != configs['numTests']:
        raise RuntimeError(str(len(files)) + ' files in ./in found; ' + str(configs['numTests']) + ' expected.')

    if configs['compile']:
        files = next(os.walk('./cpp/'))[2]
        if len(files) != configs['numTests']:
            raise RuntimeError(str(len(files)) + ' files in ./cpp found; ' + str(configs['numTests']) + ' expected.')


def make_reference_type_1():
    global configs
    os.chdir('temp')

    # in temp dir

    for test_num in range(1, configs['numTests'] + 1):
        call('cp ../in/* .')
        call('cp ../ref/* .')
        call('cp ../cpp/' + to_string(test_num, '.cpp') + ' .')
        call('cp ../config/Makefile .')
        print(' -' + to_string_default(test_num) + ' - compiling', end='\r', flush=True)
        call('make clean &> null')
        call('make ' + to_string_default(test_num) + ' &> null')
        check_file(to_string_default(test_num))
        print(' -' + to_string_default(test_num) + ' - running', end='\r', flush=True)
        call('./' + to_string_default(test_num) + ' < ' + to_string(test_num, '.in') + ' > ' + to_string(test_num, '.ref'))
        call('cp ' + to_string(test_num, '.ref') + ' ../grading/ref/')
        call('rm *')
        print(' -' + to_string_default(test_num) + ' - done ✓   ', end='\n')
    os.chdir('..')

    # back to root dir
    call('rm -rf temp')
    call('cp ./in/* ./grading/in/')


def make_reference_type_2():
    global configs
    os.chdir('temp')

    # in temp dir
    for test_num in range(1, configs['numTests'] + 1):
        call('cp ../in/* .')
        call('cp ../ref/* .')
        print(' -' + to_string_default(test_num) + ' - running', end='\r', flush=True)
        call('./' + configs['execName'] + ' < ' + to_string(test_num, '.in') + ' > ' + to_string(test_num, '.ref'))
        call('cp ' + to_string(test_num, '.ref') + ' ../grading/ref/')
        call('rm *')
        print(' -' + to_string_default(test_num) + ' - done ✓   ', end='\n')
    os.chdir('..')

    # back to root dir
    call('rm -rf temp')
    call('cp ./in/* ./grading/in/')
    call('cp tests.py ./grading/')


def make_distribute(toDistribute):
    call('mkdir distribute')
    call('mkdir distribute/ref')
    call('mkdir distribute/in')
    check_file('./grading/ref/' + toDistribute + '.ref')
    call('cp ./grading/ref/' + toDistribute + '.ref distribute/ref')
    check_file('./grading/in/' + toDistribute + '.in')
    call('cp ./grading/in/' + toDistribute + '.in distribute/in')
    call('cp tests.py ./distribute/')


# Utilities #

def call(command):
    subprocess.call(command, shell=True)


def to_string_default(test_num):
    if test_num < 10:
        return 'test0' + str(test_num)
    else:
        return 'test' + str(test_num)


def to_string(test_num, suffix):
    if test_num < 10:
        return 'test0' + str(test_num) + suffix
    else:
        return 'test' + str(test_num) + suffix


def delete_folders():
    print('delete folders')
    # call('rm -rf grading')
    # call('rm -rf temp')
    # call('rm -rf distribute')


def check_file(file_path):
    if not os.path.isfile(file_path):
        raise RuntimeError(file_path + ' not found')


def check_dir(dir_path):
    if not os.path.isdir(dir_path):
        raise RuntimeError(dir_path + ' dir not found')



if __name__ == "__main__":
    main()
