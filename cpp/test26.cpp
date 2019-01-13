// Test: remove one-child node when node is in tree multiple times
/*
 * main26.cpp
 *
 *  Created on: Oct. 19, 2014
 *      Author: chrisgregg
 */
#include <iostream>
#include "BinarySearchTree.h"

using namespace std;

int main() {
	int rand_ints[12]={5,3,6,11,-5,-2,15,4,4,9,14,8};

	BinarySearchTree bst;
	for (int i=0;i<12;i++) {
		cout << "Inserting " << rand_ints[i] << "\n";
		bst.insert(rand_ints[i]);
		bst.insert(rand_ints[i]);
	}
	bst.print_tree();
	cout << "Removing 6.\n";
	bst.remove(6);
	bst.print_tree();

	return 0;
}



