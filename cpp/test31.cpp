// Test: assignment (=) overload
/*  main31.cpp
 *
 *  Created on: Oct. 19, 2014
 *      Author: chrisgregg
 */
#include <iostream>
#include "BinarySearchTree.h"

using namespace std;

int main() {
	int rand_ints[4]={5,3,6,11};

	BinarySearchTree bst,bst2;
	for (int i=0;i<4;i++) {
		cout << "Inserting " << rand_ints[i] << "\n";
		bst.insert(rand_ints[i]);
	}
	bst2 = bst;

	bst.print_tree();
	bst2.print_tree();
	cout << "Removing 5 from bst, but not bst2.\n";
	bst.remove(5); // necessary to ensure that the trees
			// aren't pointing at each other's data
	bst.print_tree();
	bst2.print_tree(); // should be original

	return 0;
}

