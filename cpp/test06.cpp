// Test: find_max(): Inserts 5,3,6,4,7,2 into a tree, prints tree and maximum
/*
 * main6.cpp
 *
 *  Created on: Oct. 14, 2014
 *      Author: chrisgregg
 */
#include <iostream>
#include "BinarySearchTree.h"

using namespace std;

int main() {
	BinarySearchTree bst;
	bst.insert(5);
	bst.insert(3);
	bst.insert(6);
	bst.insert(4);
	bst.insert(7);
	bst.insert(2);
	bst.print_tree();
	cout << "maximum: " << bst.find_max() << "\n";

	return 0;
}
