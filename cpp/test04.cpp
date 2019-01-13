// Test: Inserts 5,4,6,6,5,4 into a tree and prints
/*
 * main4.cpp
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
	bst.insert(4);
	bst.insert(6);
	bst.insert(6);
	bst.insert(5);
	bst.insert(4);
	bst.print_tree();

	return 0;
}
