// gettter / setter, age

#include <iostream>
#include "Student.h"

int main(){
    Student nancy;
    int age;
    cin >> age;
    nancy.setAge(age);
    cout << nancy.getAge() << endl;
    nancy.allocateUnfreedMem();
    return 0;
}