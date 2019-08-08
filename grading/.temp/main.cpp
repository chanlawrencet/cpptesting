// Lawrence Chan
// Sample student program, main

#include <iostream>
#include <assert.h>
#include "Student.h"
using namespace std;

int main() {
	Student alex;
	alex.setName("alex");
	alex.setAge(20);

	Student barry("barry", 21);
	cout << barry.getName() << " is " << barry.getAge() << " years old." << endl;
	cout << alex.getName() << " is " << alex.getAge() << " years old." << endl;
}
