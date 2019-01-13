// Test: Inserts 5,4,6 into a tree and prints
/*
 * main3.cpp
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
	bst.print_tree();

	return 0;
}
