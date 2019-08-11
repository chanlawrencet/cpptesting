// gettter / setter, name and age

#include <iostream>
#include "Student.h"

int main(){
    Student nancy;
    string name;
    int age;
    cin >> name >> age;
    nancy.setName(name);
    nancy.setAge(age);
    cout << nancy.getName() << endl;
    cout << nancy.getAge() << endl;
    nancy.makeSegfault();
    return 0;
}