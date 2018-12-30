# Testing Suite Script
# Lawrence Chan 
# Dec 2018
# Goal: use this to write bash tests

import subprocess


def main():
	hwName = input('hwName:')
	numTests = countFiles()
	print("numTests:", numTests);
	executable = input('executable:')
	dirsToMake = ['out','ref','vout']
	inpath = [];
	refpath = [];
	outpath = [];

	## set up directories
	for dir in dirsToMake:
		reMkdir(dir)

	## setup lists
	for x in range(1, numTests + 1):
		testName = 'test' + str(x)
		inpath.append('in/' + testName + '.in')
		refpath.append('ref/' + testName + '.ref')
		outpath.append('out/' + testName + '.out')
		outpath.append('vout/' + testName + '.vout')

	# generate reference output
	for x in range(0, numTests):
		subprocess.call("./" + executable + "  < " + 
			            inpath[x] +  " > " + refpath[x], shell=True)

# counts # of files inside in/, up to 99
def countFiles():
	out = subprocess.Popen("ls in| wc -l", stdout=subprocess.PIPE, stderr=subprocess.STDOUT , shell=True)
	stdout = out.communicate()[0]
	splitted = list(str(stdout))
	if (len(splitted) == 6):
		return int(splitted[2])
	elif (len(splitted) == 7):
		return int(splitted[2]) * 10 + splitted[3]
	else:
		print("too many tests")
		exit(1)

def echo(input):
	print('echo \"' + input + '\"')

# deletes and remakes directories
def reMkdir(input):
	subprocess.call("rm -rf " + input, shell=True)
	subprocess.call("mkdir " + input, shell=True)


if __name__ == "__main__":
    main()