// Test: tree_height(): Inserts 5,3,8,4,6,2,7 into a tree, prints tree and height
/*
 * main9.cpp
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
	bst.insert(8);
	bst.insert(4);
	bst.insert(6);
	bst.insert(2);
	bst.insert(7);
	bst.print_tree();
	cout << "Tree height: " << bst.tree_height() << "\n";

	return 0;
}

