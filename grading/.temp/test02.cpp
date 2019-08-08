// gettter / setter, name

#include <iostream>
#include "Student.h"

int main(){
    Student nancy;
    string name;
    cin >> name;
    nancy.setName(name);
    cout << nancy.getName() << endl;
    return 0;
}