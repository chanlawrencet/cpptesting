# Testing Suite Script
# Lawrence Chan 
# Jan 2019
# Goal: use this to write bash tests

import subprocess
import os


def main():

    inputMode = int(input("inputmode? 1 = init, 2 = generate, 3 = reset: "))
    if inputMode == 1:
        init()
    elif inputMode == 2:
        generate()
    elif inputMode == 3:
        reset()
    else:
        print("Not 1, 2, or 3")
        exit(0)

def reset():
    toDelete = ['out','ref','vout', 'tmp']
    for thing in toDelete:
        subprocess.call("rm -rf " + thing, shell=True)
    
# generate script (path from config)
def generate():
    inputs = {}
    hwName = None
    useMains = None
    executable = None
    hasInput = None

    # make sure config exists
    checkConfig()

    # getting info from config file
    getConfig(inputs)

    scriptname = inputs['scriptname']
    hwName = inputs['hwName']
    useMainsIn = inputs['useMains']
    hasInputIn = inputs['hasinput']
    hasInput = True if hasInputIn  == 'y' else False
    useMains = True if useMainsIn  == 'y' else False
    if (useMains == False):
        executable = inputs['executable'] # if using ref, executable is the same

    checkDirs(useMains) # make sure cpp and in exist (to count # tests)
    numTests = countTests(useMains) # count num tests
    checkTests(numTests) # make sure there are tests

    ## set up lists
    testnames, inpath, cpppath, refpath, outpath, voutpath = [], [], [], [], [], []
    setupLists(testnames, inpath, cpppath, refpath, outpath, voutpath, numTests)

    if useMains:
        printMains()
    else:
        printRefs()
    exit(0)

# print script to scriptname, with extra compile commands
def printMains():
    print('mkdir out')

# initialize all dirs and refs necessary
def init():
    inputs = {}
    hwName = None
    useMains = None
    executable = None
    hasInput = None

    # make sure config exists
    checkConfig()

    # getting info from config file
    getConfig(inputs)

    hwName = inputs['hwName']
    useMainsIn = inputs['useMains']
    hasInputIn = inputs['hasinput']
    hasInput = True if hasInputIn  == 'y' else False
    useMains = True if useMainsIn  == 'y' else False
    if (useMains == False):
        executable = inputs['executable'] # if using ref, executable is the same

    checkDirs(useMains) # make sure cpp and in exist
    numTests = countTests(useMains) # count num tests
    checkTests(numTests) # make sure there are tests
    checkMakefile(useMains) # if using mains, check if Makefile exists
    checkReferences(useMains, executable) # if using mains, check config/ref, else, check reference

    ## set up directories
    dirsToMake = ['ref', 'tmp']
    for dir in dirsToMake:
        reMkdir(dir)

    ## set up lists
    testnames, inpath, cpppath, refpath, outpath, voutpath = [], [], [], [], [], []
    setupLists(testnames, inpath, cpppath, refpath, outpath, voutpath, numTests)

    if useMains == True:
        mainsRef(numTests, cpppath, testnames, inpath, refpath, hasInput) # generate reference for mains
    else:
        refRef(numTests, executable, inpath, refpath)

def checkReferences(useMains, executable):
    if not os.path.isdir('./reference'):
        print('./reference not found! Aborting.')
        exit(1)

    if useMains:
        out = subprocess.Popen("ls ./reference/ | wc -l", stdout=subprocess.PIPE, stderr=subprocess.STDOUT , shell=True)
        splitted = list(str(out.communicate()[0]))
        if (countList(splitted) == 0):
            print('Nothing in ./reference! Aborting.')
            exit(1)
    else:
        print("executable", executable)
        if not os.path.isfile('./reference/' + executable):
            print('./config/' + executable + ' not found! Aborting.')
            exit(1)

# getting info from config file
def getConfig(inputs):
    file = open('./config/config',"r")
    config = file.read().splitlines()
    for line in config:
        theLine = line.split('=')
        if len(theLine) == 2:
            inputs[theLine[0]] = theLine[1]

# generate reference for refs
# by default there has to be an input (or else what are you testing?)
def refRef(numTests, executable, inpath, refpath):
    for x in range(0, numTests):
        subprocess.call("./reference/" + executable + "  < " + 
                        inpath[x] +  " > " + refpath[x], shell=True)
# generate reference for mains
def mainsRef(numTests, cpppath, testnames, inpath, refpath, hasInput):
    for x in range(0, numTests):
        print('Compiling ' + testnames[x])
        subprocess.call("cp " + cpppath[x] + " tmp", shell=True)
        subprocess.call("cp ./config/Makefile tmp", shell=True)
        subprocess.call("cp ./reference/* ./tmp/", shell=True)
        subprocess.call("make " + testnames[x] + " -C ./tmp/ &> /dev/null", shell=True)
        print('Running ' + testnames[x])
        if hasInput:
            subprocess.call("./tmp/" + testnames[x] + " > " + refpath[x], shell=True)
        else:
            subprocess.call("./tmp/" + testnames[x] + "  < " + 
                            inpath[x] +  " > " + refpath[x], shell=True)

        subprocess.call("rm ./tmp/*", shell=True)
        #print("cp " + cpppath[x] + " tmp")
        #print("cp config/Makefile .")
        #print("make "+ testnames[x] + " -C tmp")
        #print("rm temp")
    
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
    if not os.path.isfile('./config/config'):
        print('./config/config not found! Aborting.')
        exit(1)
    return
# convert nonzero int into string with leading zero
def addZero(inputNum):
    if inputNum < 10:
        return "0" + str(inputNum)
    else:
        return str(inputNum)
# check if /config/Makefile exists, if necessary
def checkMakefile(useMains):
    if useMains == False:
        return
    if not os.path.isfile('./config/Makefile'):
        print('./config/Makefile not found! Aborting.')
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
    splitted = list(str(out.communicate()[0]))
    return countList(splitted)

# turn list into number, max 999
def countList(theList):
    if (len(theList) == 6):
        return int(theList[2])
    elif (len(theList) == 7):
        return int(theList[2]) * 10 + int(theList[3])
    elif (len(theList) == 8):
        return int(theList[2]) * 100 + int(theList[3]) * 10 + int(theList[2])

def echo(input):
    print('echo \"' + input + '\"')

# deletes and remakes directories
def reMkdir(input):
    subprocess.call("rm -rf " + input, shell=True)
    subprocess.call("mkdir " + input, shell=True)


if __name__ == "__main__":
    main()
