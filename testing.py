# Testing Suite Script
# Lawrence Chan 
# Jan 2019
# Goal: use this to write bash tests

import subprocess
import os


def main():

    inputMode = int(input("inputmode? 1 = init, 2 = reset: "))
    if inputMode == 1:
        init()
    elif inputMode == 2:
        reset()
    else:
        print("Not 1 or 2")
        exit(0)

def reset():
    toDelete = ['out','ref','vout', 'tmp']
    for thing in toDelete:
        subprocess.call("rm -rf " + thing, shell=True)
    

def init():
    inputs = {}
    hwName = None
    useMains = None
    executable = None

    checkConfig()

    # getting info from config file
    file = open('./bin/config',"r")
    config = file.read().splitlines()
    for line in config:
        theLine = line.split('=')
        if len(theLine) == 2:
            inputs[theLine[0]] = theLine[1]
    hwName = inputs['hwName']
    useMainsIn = inputs['useMains']
    useMains = True if useMainsIn  == 'y' else False
    if (useMains== False):
        executable = inputs['executable'] # if using ref, executable is the same

    print("hwname", hwName)
    print("usemains", useMains)
    print("executable", executable)

    checkDirs(useMains) # make sure dirs exist
    numTests = countTests(useMains) # count num tests
    checkTests(numTests) # make sure there are tests
    checkMakefile(useMains) # if using mains, check if Makefile exists

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

    ## set up lists
    setupLists(testnames, inpath, cpppath, refpath, outpath, voutpath, numTests)

    ## generate reference output
    if useMains == True:
        for x in range(0, numTests):

            subprocess.call("cp " + cpppath[x] + " tmp", shell=True)
            subprocess.call("cp ./bin/Makefile tmp", shell=True)
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
# set up lists given
def setupLists(testnames, inpath, cpppath, refpath, outpath, voutpath, numTests):
    ## setup lists
    for x in range(1, numTests + 1):
        testName = 'test' + addZero(x)
        testnames.append(str(testName))
        inpath.append('in/' + testName + '.in')
        cpppath.append('cpp/' + testName + '.cpp')
        refpath.append('ref/' + testName + '.ref')
        outpath.append('out/' + testName + '.out')
        voutpath.append('vout/' + testName + '.vout')

# check if config exists
def checkConfig():
    if not os.path.isfile('./bin/config'):
        print('./bin/config not found! Aborting.')
        exit(1)
    return
# convert nonzero int into string with leading zero
def addZero(inputNum):
    if inputNum < 10:
        return "0" + str(inputNum)
    else:
        return str(inputNum)
# check if /bin/Makefile exists, if necessary
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
def checkTests(numTests):
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
