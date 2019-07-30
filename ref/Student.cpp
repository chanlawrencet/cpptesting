#include "Student.h"

// default constructor
Student::Student(){
	this->name = "default";
	this->age = 0;
	this->allocatedMem = new int;
	*(this->allocatedMem) = 5;
}

// parameterized constructor
Student::Student(string name, int age){
	this->name = name;
	this->age = age;
	this->allocatedMem = new int;
	*(this->allocatedMem) = 5;
}

void Student::makeSegfault(){
	int ray[5];
	ray[12312313] = 5; // should make make segfault
}

// allocate memory and forget to free it, causes memory leak
void Student::allocateUnfreedMem(){
	int *number = new int;

}


// getters + setters
void Student::setName(string name){
	this->name = name;
}

void Student::setAge(int age){
	this->age = age;
}

string Student::getName(){
	return this->name;
}

int Student::getAge(){
	return this->age;
}

Student::~Student(){
	delete this->allocatedMem;
    this->allocatedMem = NULL;	
};
