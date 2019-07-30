# CPPTests

The purpose of this program is to make a simple input and output testing for students in comp15, Data Structures, taken at Tufts University. The hope is to generate code used by TAs to make grading more efficient while maintainng consistency throughout the tests throughout the course. 

## File Structure
```
|-testGen.py (generates grading dir)
|-tests.py (testing program)
|-config/
  |-config.json
  |-Makefile *
|-in/ (input files)
|-ref/
  |-files needed for compilation
  |-reference executable *
  |-Makefile *
|-grading/ **
  |-in/ (input files) **
  |-ref/ (reference output) **
  |-tests.py **
|-distribute/ **
  |-input/ (1 test) **
  |-ref/ (1 test) **
  |-tests.py **
```
_`*` are optional files_

_`**` are generated files_

## Two types and setup
There are two types of tests available to be generated, with baseline prerequsities:
* config JSON (to be stored in `./config/config.json`)
* test input, to be fed in `stdin` (to be stored in `./in/`)

### Type 1 - functional tests

Functional tests are meant to provide a type of unit testing for students, to make a series of `main.cpp` files that target and test specific functions that students are meant to implement. Typically, we will supply a list of functions they are to implement, but some functions (eg. `arrayList.expand()`) are marked as `Private`. In our testing, we will compile with our own `.h` file that gives us access to these private functions.

Additional prerequisites:
* complete, compileable solution code (to be stored in `./ref/`)
* Makefile with targets for tests written inside (to be stored in `./config/Makefile`)

### Type 2 - end-to-end tests

As the course progresses, we become increasingly more interested in how students tackle bigger problems, such as a grepping program. Thus, we rely more heavily on full functionality programs. 

Additionalrerequisites:
* reference executable (to be stored in `./ref/`)

## Examples
### Type 1 - functional test example
In place currently is a type 1 example, a functional test. The reference program is stored in `./ref`, and is a simple class-based program with a `Student` class. I included a few functions that would cause memory leaks (that will be detected by the testing program). 


## Troubleshooting
* Programs aren't being generated to create reference output!
  * Check your `./config/Makefile` to make sure all targets are accounted for
