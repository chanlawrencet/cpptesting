// Lawrence Chan
// Sample student program, class, student

#include <iostream>
using namespace std;

#ifndef STUDENT_H
#define STUDENT_H

class Student

{
public:
	Student();
	~Student();
	Student(string, int);

	string getName();
	int getAge();

	void setName(string);
	void setAge(int);

	void allocateUnfreedMem();

	void makeSegfault();

private:
	string name;
	int age;
	
	int *allocatedMem;
};

#endif