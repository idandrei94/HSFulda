#include <stdio.h>
#include <time.h> 
#include <stdlib.h> 

typedef struct Node
{
    int value;
    struct Node *left;
    struct Node *right;
} Node;

struct Node *create_node(
    int );

struct Node *insert_node(
    struct Node *, 
    int );

void print_tree_pre_order (
    struct Node * );

void print_tree_in_order (
    struct Node * );

void print_tree_post_order (
    struct Node * );

void delete_tree(
    struct Node * );

struct Node *create_node(
    int data )
{
    Node *newNode = malloc(sizeof(Node));
    newNode -> value = data;
    newNode -> left = NULL;
    newNode -> right = NULL;
    return newNode;
}

struct Node *insert_node(
    struct Node *root, 
    int data)
{
    Node *tempNode;
    if(root == NULL)
    {
        return create_node(data);
    }
    if(root -> value == data)
    {
        return root;
    }
    tempNode = root;
    if(tempNode -> value > data)
    {
        if(tempNode->left == NULL)
        {
            Node *newNode = create_node(data);
            tempNode->left = newNode;
            return newNode;
        }
        else
        {
            Node *ret = insert_node(tempNode->left, data);
            return ret == tempNode ? root : ret;
        }
    }
    else
    {
        if(tempNode->right == NULL)
        {
            Node *newNode = create_node(data);
            tempNode->right = newNode;
	    return newNode;
        }
        else
        {
            Node *ret = insert_node(tempNode->right, data);
            return ret == tempNode ? root : ret;
        }
    }
}

void print_tree_pre_order (
    struct Node * root )
{
    if(root == NULL)
        return;
    printf("%d ", root -> value);
    print_tree_pre_order(root -> left);
    print_tree_pre_order(root -> right);
}

void print_tree_in_order (
    struct Node *root )
{
    if(root == NULL)
        return;
    print_tree_in_order(root -> left);
    printf("%d ", root -> value);
    print_tree_in_order(root -> right);
}

void print_tree_post_order (
    struct Node *root )
{
    if(root == NULL)
        return;
    print_tree_post_order(root -> left);
    print_tree_post_order(root -> right);
    printf("%d ", root -> value);
}

void delete_tree(
    struct Node *root ) 
{
    if(root == NULL)
        return;
    delete_tree(root -> left);
    delete_tree(root -> right);
    free(root);
}

int main(
    void )
{
  time_t start_time = time(NULL);
  clock_t start_clock = clock();
  Node *root = insert_node(NULL, 50);
  insert_node(root, 56);
  insert_node(root, 46);
  insert_node(root, 6);
  insert_node(root, 27);
  insert_node(root, 67);
  insert_node(root, 65);
  insert_node(root, 92);
  insert_node(root, 90);

  print_tree_in_order(root);
    
  delete_tree(root);
  root = NULL;
  printf("\nCPU time:\t\t%.2f\t\tReal time: \t\t%.2f",
		(double)(clock()-start_clock)/CLOCKS_PER_SEC, 
		difftime(time(NULL), start_time));
  return EXIT_SUCCESS;
}
