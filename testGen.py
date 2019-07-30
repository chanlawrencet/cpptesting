import subprocess
import sys
import os
import json

configs = {}


def main():
    parse_args()

    print('Checking prerequisites')
    check_prerequisites()

    print('Generating folders')
    generate_folders()

    print('Parsing configs')
    parse_configs()

    print('Making reference')
    make_reference()


def call(command):
    subprocess.call(command, shell=True)


def to_dot_cpp(test_num):
    return to_string(test_num) + '.cpp'


def to_dot_in(test_num):
    return to_string(test_num) + '.in'


def to_string(test_num):
    if test_num < 10:
        return 'test0' + str(test_num)
    else:
        return 'test' + str(test_num)


def make_reference():
    global configs
    os.chdir('temp')

    # in temp dir

    for test_num in range(1, configs['numTests'] + 1):
        call('touch hello')
        call('cp ../config/Makefile .')
        call('cp ../in/* .')
        call('cp ../ref/* .')
        call('cp ../cpp/' + to_dot_cpp(test_num) + ' .')
        call('make clean')
        call('make ' + to_string(test_num))
        # call('rm *')
    os.chdir('..')

def parse_configs():
    global configs
    with open('./config/config.json') as jsonFile:
        configs = json.load(jsonFile)


def parse_args():
    if len(sys.argv) > 1:
        if sys.argv[1] == '-delete':
            print('Deleting folders')
            delete_folders()
            exit()


def delete_folders():
    call('rm -rf grading')


def generate_folders():
    call('rm -rf grading')
    call('rm -rf temp')
    call('mkdir temp')
    call('mkdir grading')
    call('mkdir grading/in')
    call('mkdir grading/ref')


def check_file(file_path):
    if not os.path.isfile(file_path):
        raise file_path + ' not found'


def check_dir(dir_path):
    if not os.path.isdir(dir_path):
        raise dir_path + ' dir not found'


def check_prerequisites():
    dir_prereqs = ['./ref', './cpp']
    file_prereqs = ['./config/config.json', './config/Makefile']
    for dir in dir_prereqs:
        check_dir(dir)
    for file in file_prereqs:
        check_file(file)

if __name__ == "__main__":
    main()
