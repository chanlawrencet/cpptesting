// Test: count_total(): inserts 5,3,6,6,4,4 into tree, prints tree and count_total()
/*
 * main16.cpp
 *
 *  Created on: Oct. 14, 2014
 *      Author: chrisgregg
 */
#include <iostream>
#include "BinarySearchTree.h"

using namespace std;

int main() {
	int rand_ints[6]={5,3,6,6,4,4};

	BinarySearchTree bst;
	for (int i=0;i<6;i++) {
		cout << "Inserting " << rand_ints[i] << "\n";
		bst.insert(rand_ints[i]);
	}
	bst.print_tree();
	cout << "Count total: " << bst.count_total() << "\n";

	return 0;
}

