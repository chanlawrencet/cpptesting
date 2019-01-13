# Testing Suite Script
# Lawrence Chan 
# Jan 2019
# Goal: use this to write bash tests

import subprocess
import os

def main():
    config = open('config',"r")
    inputs = {}
    hwName = None
    useMains = None
    executable = None
    for line in config:
        theLine = line.split('=')
        if theLine[0] == '\n' or line[0] == '#':
            continue
        if theLine[1] == '\n':
            print('Field not completed! Aborting.')
            exit(1)
        inputs[theLine[0]] = theLine[1]
    hwName = inputs['hwName']
    useMains = inputs['useMains']
    useMains = True if useMains  == 'y' else False

    print(hwName)
    print(useMains)

    print(executable)

    checkDirs(useMains) # make sure dirs exist
    numTests = countTests(useMains) # count num tests
    checkFiles(numTests) # make sure there are tests
    checkMakefile(numTests) # if using mains, check if Makefile exists
    #print("numtests:", numTests)
    if (useMains== False):
        executable = input('executable:') # if using ref, executable is the same

    dirsToMake = ['out','ref','vout', 'tmp']
    testnames = []
    inpath = []
    cpppath = []
    refpath = []
    outpath = []
    voutpath = []

    ## set up directories
    for dir in dirsToMake:
        reMkdir(dir)

    ## setup lists
    for x in range(1, numTests + 1):
        testName = 'test' + addZero(x)
        testnames.append(str(testName))
        inpath.append('in/' + testName + '.in')
        cpppath.append('cpp/' + testName + '.cpp')
        refpath.append('ref/' + testName + '.ref')
        outpath.append('out/' + testName + '.out')
        voutpath.append('vout/' + testName + '.vout')

    print(inpath, cpppath, refpath, outpath, voutpath)


    ## generate reference output
    if useMains == True:
        for x in range(0, numTests):
            subprocess.call("cp " + cpppath[x] + " tmp", shell=True)
            subprocess.call("cp bin/Makefile tmep")
            subprocess.call
            #print("cp " + cpppath[x] + " tmp")
            #print("cp bin/Makefile .")
            #print("make "+ testnames[x] + " -C tmp")
            #print("rm temp")
        exit(0)
        subprocess.call("make -C bin/", shell=True)
        subprocess.call("ls", shell=True)
    else:
        for x in range(0, numTests):
            subprocess.call("./" + executable + "  < " + 
                            inpath[x] +  " > " + refpath[x], shell=True)
# convert nonzero int into string with leading zero
def addZero(inputNum):
    if inputNum < 10:
        return "0" + str(inputNum)
    else:
        return str(inputNum)
# check if /bin/Makefile exists
def checkMakefile(useMains):
    if useMains == False:
        return
    if not os.path.isfile('./bin/Makefile'):
        print('./bin/Makefile not found! Aborting.')
        exit(1)
# check if dirs exist
def checkDirs(useMains):
    if (useMains == True) and (not os.path.isdir('./cpp')):
        print('./cpp not found! Aborting.')
        exit(1)
    elif (useMains == False) and (not os.path.isdir('./in')):
        print('./in not found! Aborting.')
        exit(1)

# make sure # tests is non 0
def checkFiles(numTests):
    if (numTests == 0):
        print('no tests found! Aborting.')
        exit(1)

# counts # of files inside dir/, up to 99
def countTests(useMains):
    out = None
    if (useMains == True):
        # counts # files in cpp/ (for main unit testing)
        out = subprocess.Popen("ls cpp | wc -l", stdout=subprocess.PIPE, stderr=subprocess.STDOUT , shell=True)
    else:
        # counts # files in in/ (for ref comparision)
        out = subprocess.Popen("ls in | wc -l", stdout=subprocess.PIPE, stderr=subprocess.STDOUT , shell=True)
    stdout = out.communicate()[0]
    splitted = list(str(stdout))

    # turn list back into number, max 99
    if (len(splitted) == 6):
        return int(splitted[2])
    elif (len(splitted) == 7):
        return int(splitted[2]) * 10 + int(splitted[3])
    else:
        print("Too many tests! Aborting.") # max = 99
        exit(1)

def echo(input):
    print('echo \"' + input + '\"')

# deletes and remakes directories
def reMkdir(input):
    subprocess.call("rm -rf " + input, shell=True)
    subprocess.call("mkdir " + input, shell=True)


if __name__ == "__main__":
    main()
