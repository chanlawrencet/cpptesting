# Lawrence Chan
# Sample student program, Makefile

CXX = clang++
CXXFLAGS = -g3 -Wall -Wextra -std=c++11
LDFLAGS = -g3

studentProgram: main.o Student.o
	${CXX} ${LDFLAGS} -o exampleProgram main.o Student.o

main.o: main.cpp Student.h
Student.o: Student.cpp


clean:
	rm -rf studentProgram *.o *.dSYM
