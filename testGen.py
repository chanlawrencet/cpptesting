#!/usr/bin/python
# -*- coding: UTF-8 -*-

import subprocess
import sys
import os
import json

configs = {}


def main():
    parse_args()

    print('Checking prerequisites', end='\r')
    check_prerequisites()
    print('Checking prerequisites ✓',)

    print('Generating folders', end='\r')
    generate_folders()
    print('Generating folders ✓')

    print('Parsing configs', end='\r')
    parse_configs()
    print('Parsing configs ✓')

    print('Checking tests', end='\r')
    check_tests()
    print('Checking tests ✓')


    print('Making reference (' + str(configs['numTests']) + ' tests)')
    make_reference()
    print('Made reference ✓')
    print()
    print('All files made, found in ./grading.')


# https://stackoverflow.com/questions/2632205/how-to-count-the-number-of-files-in-a-directory-using-python
def check_tests():
    global configs
    files = next(os.walk('./in/'))[2]
    if len(files) != configs['numTests']:
        raise RuntimeError(str(len(files)) + ' files in ./in found; ' + str(configs['numTests']) + ' expected.')

    files = next(os.walk('./cpp/'))[2]
    if len(files) != configs['numTests']:
        raise RuntimeError(str(len(files)) + ' files in ./cpp found; ' + str(configs['numTests']) + ' expected.')


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


def make_reference():
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
        print(' -' + to_string_default(test_num) + ' - b', end='\r', flush=True)
        call('./' + to_string_default(test_num) + ' < ' + to_string(test_num, '.in') + ' > ' + to_string(test_num, '.ref'))
        call('cp ' + to_string(test_num, '.ref') + ' ../grading/ref/')
        call('rm *')
        print(' -' + to_string_default(test_num) + ' - done ✓   ', end='\n')
    os.chdir('..')

    # back to root dir
    call('rm -rf temp')
    call('cp ./in/* ./grading/in/')
    call('cp tests.py ./grading/')


def parse_configs():
    global configs
    with open('./config/config.json') as jsonFile:
        configs = json.load(jsonFile)


def parse_args():
    if len(sys.argv) > 1:
        if sys.argv[1] == '-clean':
            print('Deleting folders', end='\r')
            delete_folders()
            print('Deleting folders ✓', end='\n')
            exit()


def delete_folders():
    call('rm -rf grading')
    call('rm -rf temp')


def generate_folders():
    call('rm -rf grading')
    call('rm -rf temp')
    call('mkdir temp')
    call('mkdir grading')
    call('mkdir grading/in')
    call('mkdir grading/ref')


def check_file(file_path):
    if not os.path.isfile(file_path):
        raise RuntimeError(file_path + ' not found')


def check_dir(dir_path):
    if not os.path.isdir(dir_path):
        raise RuntimeError(dir_path + ' dir not found')


def check_prerequisites():
    dir_prereqs = ['./ref', './cpp', './in']
    file_prereqs = ['./config/config.json', './config/Makefile']
    for dir in dir_prereqs:
        check_dir(dir)
    for file in file_prereqs:
        check_file(file)

if __name__ == "__main__":
    main()
