# Lawrence Chan
# Makefile for testing

CXX = clang++
CXXFLAGS = -g3 -Wall -Wextra -std=c++11
LDFLAGS = -g3

studentProgram: main.o Student.o
	${CXX} ${LDFLAGS} -o exampleProgram main.o Student.o

test01: test01.o 
	${CXX} ${LDFLAGS} -o test01 test01.o

test02: test02.o Student.o
	${CXX} ${LDFLAGS} -o test02 test02.o Student.o

test03: test03.o Student.o
	${CXX} ${LDFLAGS} -o test03 test03.o Student.o

test04: test04.o Student.o
	${CXX} ${LDFLAGS} -o test04 test04.o Student.o

test05: test05.o Student.o
	${CXX} ${LDFLAGS} -o test05 test05.o Student.o

main.o: main.cpp Student.h
Student.o: Student.cpp


clean:
	rm -rf studentProgram *.o *.dSYM
