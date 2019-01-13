/*
 * BinarySearchTree.h
 *
 *  Created on: Oct 13, 2014
 */

#ifndef BINARYSEARCHTREE_H_
#define BINARYSEARCHTREE_H_

#include <iostream>

// Binary Search Tree Node:
// - data is the value
// - count is the number of times the data has been inserted
//   into the tree (minus removals)
//
// We're defining this outside the class, which is really not good!
// However, we're giving you a pretty printer for trees that we got 
// from somewhere else, and it will need the node structure.
// Your client code must NOT access nodes.
// We will take deductions for abstraction violations when we assess
// your submission.
//
struct Node {
        int   data;
        int   count;
        Node *left;
        Node *right;
};

// defined in pretty_print.cpp
void printPretty(Node *root, int level, int indentSpace, std::ostream &out);

class BinarySearchTree {
public:
        // constructor
        BinarySearchTree();

        // destructor
        ~BinarySearchTree();

        // copy constructor (written for you)
        BinarySearchTree(const BinarySearchTree &source);

        // assignment overload
        BinarySearchTree &operator= (const BinarySearchTree &source);

        // find_min() returns the minimum value in the tree
        // returns INT_MIN if the tree is empty
        int find_min() const;

        // find_max() returns the maximum value in the tree
        // returns INT_MAX if tree is empty
        int find_max() const;

        // contains() returns true if the value is in the tree,
        // false if it is not in the tree
        bool contains(int value) const;

        // insert() inserts the value into the Binary Search Tree.
        // If the value is already in the tree, the node's count
        // is incremented by 1
        void insert(int value);

        // remove() does a full removal from the tree (NOT lazy removal)
        // If a node's count is greater than one, the count is
        // decremented, and the node is not removed.
        // Nodes with a count of 0 must be fully removed using the
        // following algorithm (discussed in class): if the node has no
        // children, simply remove it.  If the node has one child,
        // "bypass" the node to the child from the parent.  If the node
        // has two children, first find the minimum node of the
        // right child, replace the node's data with the value and
        // count of right's minimum, and then recursively delete
        // right's minimum.
        bool remove(int value);

        // returns the maximum distance from the root to it's farthest
        // leaf.  Note:  An empty tree has a height of -1, a tree with
        // just a root has a height of 0, and a tree with a root and
        // one or two children has a height of 1, etc.
        int tree_height() const;

        // returns the total number of nodes (NOT including duplicates)
        // i.e., if a tree contains 3, 4, 4, the number of nodes would
        // only be two, because the fours are contained in one node.
        int node_count() const;

        // return the sum of all the node values (including duplicates)
        // For the previous example, the count_total() would be 
        // 3 + 4 + 4 = 11
        int count_total() const;

        // print the tree (written for you)
        void print_tree() const;

private:
        // the root of the tree (starts as NULL)
        Node *root;

        // the following nine functions are private helper functions
        // for the public functions. We do not want to expose the
        // internals of the tree publicly, so we pass the root (and
        // other information in some cases) to the functions below
        // from the public functions.
        Node *find_min(Node *node) const;
        Node *find_max(Node *node) const;
        bool  contains(Node *node, int value) const;
        void  insert(Node *node,Node *parent, int value);
        Node *insert(Node *np, int value);
        bool  remove(Node *node, Node **parent, int value);
        int   tree_height(Node *node) const;
        int   node_count(Node *node) const;
        int   count_total(Node *node) const;
        Node *pre_order_copy(Node *node) const;

        // used by the destructor to delete nodes recursively
        void  post_order_delete(Node *node);

        // find_parent (written for you) is necessary for removing
        // the right_min of a node when removing a node that has
        // two children
        Node *find_parent(Node *node, Node *child) const;
};


#endif /* BINARYSEARCHTREE_H_ */
