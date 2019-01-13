/*
 * BinarySearchTree.cpp
 *
 * Mark A. Sheldon, Tufts University, Spring 2016
 */

#include <iostream>
#include <climits>
#include <cassert>

#include "BinarySearchTree.h"

using namespace std;


static inline int max(int a, int b)
{
        return (a > b) ? a : b;
}

/*
 * Return pointer to newly heap-allocated node initialized
 * with given values.
 */
static Node *newNode(int data, int count, Node *left, Node *right)
{
        Node *np = new Node();
 
        np->data  = data;
        np->count = count;
        np->left  = left;
        np->right = right;

        return np;
}        

/*
 * Return pointer to newly heap-allocated node initialized
 * with given data.  
 * Initial count is 1, and subtrees are empty.
 */
static Node *newNode(int data)
{
        return newNode(data, 1, NULL, NULL);
}

/*
 * Set node contents to predictable, "deleted" node values
 * and then recycle the node.
 */
static void deleteNode(Node *np)
{
        np->count = -1;  /* Something that couldn't be in a real node */
        np->data  = -1;  /* Arbitrary value                           */
        np->left  = np->right = NULL;
        delete np;
}

/*
 * Nullary constructor makes empty tree.
 */
BinarySearchTree::BinarySearchTree()
{
        root = NULL;
}

/*
 * Destructor recycles storage and makes tree empty.
 */
BinarySearchTree::~BinarySearchTree()
{
        post_order_delete(root);
        root = NULL;   /*
                        * not really necessary, since the tree is going 
                        * away, but might want to guard against someone
                        * using a pointer after deleting
                        */
}

/*
 * Delete all nodes in the tree rooted at node.
 */
void BinarySearchTree::post_order_delete(Node *node)
{
        if (node != NULL) {
                //cerr << "deleting node with " << node->data << endl;
                post_order_delete(node->left);
                post_order_delete(node->right);
                deleteNode(node);
        }
}

/*
 * Copy constructor
 */
BinarySearchTree::BinarySearchTree(const BinarySearchTree &source)
{
        root = pre_order_copy(source.root);
}

/*
 * Assignment operator overload
 * Makes LHS be a (deep) copy of RHS
 * 
 * Algorithm:  
 *
 * Delete storage associated with left hand side of assignment.
 * Deep copy tree from right hand side into tree on left hand side.
 * Does nothing on self assignment (e. g., bst = bst;)
 */
BinarySearchTree &BinarySearchTree::operator= (const BinarySearchTree &source)
{
        /* only do something if not self assignment */
        if (this != &source) {
                post_order_delete(this->root);
                this->root = pre_order_copy(source.root);
        }
        return *this;
}

/*
 * Return pointer to root of a deep copy of tree rooted at node.
 */
Node *BinarySearchTree::pre_order_copy(Node *node) const
{
        if (node == NULL)
                return NULL;
        else
                return newNode(node->data,
                               node->count,
                               pre_order_copy(node->left),
                               pre_order_copy(node->right));
}

/******************************************************************/
/* MAS:  These are backwards from the traditional view:           */
/*       find_min() should return INT_MAX for the minimum value   */
/*       find_max() should return INT_MIN for the maximum value   */
/******************************************************************/

/*
 * Return least element in tree, INT_MIN if tree is empty (harumph!)
 */
int BinarySearchTree::find_min() const
{
        if (root == NULL)
                return INT_MIN;
        return find_min(root)->data;
}

/*
 * Return largest element in tree, INT_MAX if tree is empty (harumph!)
 */
int BinarySearchTree::find_max() const
{
        if (root == NULL)
                return INT_MAX;
        else
                return find_max(root)->data;
}

/*
 * Return pointer to node with smallest value in tree.
 * Assumes:  node is not NULL
 */
Node *BinarySearchTree::find_min(Node *node) const
{
        if (node->left == NULL)
                return node;
        else
                return find_min(node->left);
}

/*
 * Return pointer to node with the largest value in tree.
 * Assumes:  node is not NULL
 */
Node *BinarySearchTree::find_max(Node *node) const
{
        if (node->right == NULL)
                return node;
        else
                return find_max(node->right);
}

/*
 * Return true of tree contains given value, false otherwise
 */
bool BinarySearchTree::contains(int value) const
{
        return contains(root, value);
}

/*
 * Return true if tree rooted at node contains given value,
 * false otherwise
 */
bool BinarySearchTree::contains(Node *node, int value) const
{
        if (node == NULL)
                return false;
        else if (node->data == value)
                return true;
        else if (value < node->data)
                return contains(node->left, value);
        else
                return contains(node->right, value);
}

/*
 * Update tree so it contains one occurrence of given value.
 *
 * I changed the interface of for the private insertion function, 
 * because I feel the code is cleaner this way.
 * I wrote it both ways, so you can decide what you think.
 */
void BinarySearchTree::insert(int value)
{
        // insert(root, NULL, value);
        root = insert(root, value);
}

/*
 * Return pointer to root of the tree that results from inserting
 * given value into the tree rooted at np.
 *
 * If tree rooted at np isn't empty, the return value is np.  
 * But if tree rooted at np is empty, the return value is a 
 * newly-allocated root.
 */
Node *BinarySearchTree::insert(Node *np, int value)
{
        /* 
         * Need to insert the value, but we've hit a dead end.
         * Make a new leaf.
         */
        if (np == NULL)
                return newNode(value);

        /*
         * Otherwise, return this node after completing insertion
         */
        if (np->data == value)
                np->count++;
        else if (value < np->data)
                np->left = insert(np->left, value);
        else
                np->right = insert(np->right, value);

        return np;
}

/*
 * Return pointer to root of the tree that results from inserting
 * given value into the tree rooted at np.
 *
 * This was the insert we were looking for.
 * The need to reach back and update the parent disrupts the flow,
 * and we KNOW this test was already done when the parent node was
 * tested.
 */
void BinarySearchTree::insert(Node *node, Node *parent, int value)
{
        if (node == NULL and parent == NULL)  /* First node in tree */
                root = newNode(value);
        else if (node == NULL)
                /*
                 * assume (value != parent->data) or previous
                 * call would have caught it
                 */
                if (value < parent->data)
                        parent->left = newNode(value);
                else
                        parent->right = newNode(value);
        else if (node->data == value)
                node->count++;
        else if (value < node->data)
                insert(node->left, node, value);
        else
                insert(node->right, node, value);
}

/*
 * Update tree to have one fewer occurrences of the given value.
 * Return true if the value was found in the tree, false otherwise.
 *
 * I changed the interface of the private removal function.  Again,
 * why test which child we've descended through when the parent knows
 * which subtree it traversed?
 * 
 * So, I have caller pass the cell that might need updating by
 * reference.  I'm using C style here:  rather than a C++ reference
 * parameter, I'm passing a pointer to the location that holds the
 * Node pointer.
 * 
 * This time, I didn't write it both ways.
 */
bool BinarySearchTree::remove(int value)
{
        return remove(root, &root, value);
        // return remove(root, NULL, value);
}


/*
 * Make the given slot pointing to this node point to another
 * node instead, then delete the current node.
 */
static void replace_and_delete(Node  *me,
                               Node **ptr_to_slot_pointing_to_me,
                               Node  *ptr_to_my_replacement)
{
        *ptr_to_slot_pointing_to_me = ptr_to_my_replacement;
        delete me;
}

/* 
 * Update tree rooted at node so it contains one fewer occurrence of
 * given value.  If the node itself must be removed, then update the
 * variable in the parent that was pointing to node.
 *
 * This function is getting rather long.  It's structure is simple,
 * however:  It's just a big series of (non-nested) conditions with
 * simple actions in each case.
 * I could have made a helper function for remove_this_node(), or I
 * could have broken out the leaf, one child, and two child cases.
 */
bool BinarySearchTree::remove(Node *node, Node **ptr_to_ptr_to_me, int value)
{
        if (node == NULL)
                return false;
        else if (value < node->data)
                return remove(node->left, &node->left, value);
        else if (value > node->data)
                return remove(node->right, &node->right, value);

        /* This is the the node we're looking for */
        else if (node->count > 1) { 
                node->count--;
                return true;
        } else if ((node->left == NULL) and (node->right == NULL)) {
                replace_and_delete(node, ptr_to_ptr_to_me, NULL);
                return true;
        } else if ((node->left != NULL) and (node->right == NULL)) {
                replace_and_delete(node, ptr_to_ptr_to_me, node->left);
                return true;
        } else if ((node->left == NULL) and (node->right != NULL)) {
                replace_and_delete(node, ptr_to_ptr_to_me, node->right);
                return true;
        } else {
                Node *minNode = find_min(node->right);
                node->data  = minNode->data;
                node->count = minNode->count;
                minNode->count = 0;     /* ensure this node will be deleted */
                return remove(node->right, &node->right, minNode->data);
        }
}

/*
 * Return the height of the tree.
 */
int BinarySearchTree::tree_height() const
{
        return tree_height(root);
}

/*
 * Return the height of the tree rooted at node.
 */
int BinarySearchTree::tree_height(Node *node) const
{
        if (node == NULL)
                return -1;
        else
                return 1 + max(tree_height(node->left), tree_height(node->right));
}

/*
 * Return the total number of nodes.
 */
int BinarySearchTree::node_count() const
{
        return node_count(root);
}

/*
 * Return the total number of nodes rooted at node.
 */
int BinarySearchTree::node_count(Node *node) const
{
        if (node == NULL)
                return 0;
        else
                return 1 + node_count(node->left) + node_count(node->right);
}

/*
 * Return the sum of all the node values (including duplicates)
 */
int BinarySearchTree::count_total() const
{
        return count_total(root);
}

/*
 * Return the sum of all the node values (including duplicates)
 * in the tree rooted at node.
 */
int BinarySearchTree::count_total(Node *node) const
{
        if (node == NULL)
                return 0;
        else
                return (node->data * node->count)
                        + count_total(node->left) + count_total(node->right);
}

/*
 * Use the printPretty helper to make the tree look nice.
 */
void BinarySearchTree::print_tree() const
{
        printPretty(root, 1, 0, std::cout);
}

/*
 * Return pointer to parent node of child in tree rooted at node.
 * If tree is empty, then child has no parent, and we return NULL.
 * Assumes that node pointed to by given node is above child in the
 * tree  node != child
 * It is an error if child == NULL  
 * (all leaves look like the parent of NULL)
 */
Node *BinarySearchTree::find_parent(Node *node, Node *child) const
{
        assert(child != NULL);

        if (node == NULL) return NULL;

        /*
         * if node points to the child, found the parent
         */
        if (node->left == child or node->right == child) {
                return node;
        }

        /* Use the binary search tree invariant to walk the tree */
        if (child->data > node->data) {
                return find_parent(node->right, child);
        } else {
                return find_parent(node->left, child);
        }
}
