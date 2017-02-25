
from Tree import BinTree

def main():

    tree = BinTree('F')
    BinTree.add_tree(tree, 'B')
    BinTree.add_tree(tree, 'G')
    BinTree.add_tree(tree, 'A')
    BinTree.add_tree(tree, 'I')
    BinTree.add_tree(tree, 'D')
    BinTree.add_tree(tree, 'C')
    BinTree.add_tree(tree, 'E')
    BinTree.add_tree(tree, 'H')


    print('inorder:')
    BinTree.inorder(tree)
    print('=============================')
    print('preorder:')
    BinTree.preorder(tree)
    print('=============================')
    print('postorder:')
    BinTree.postorder(tree)

    print('=============================')
    print('breadthorder:')
    BinTree.breadthfirst(tree)

    # TODO: write code that search a value in the tree
    # TODO: write code that adds to a tree without recursion
    # TODO: look for problems with trees
    # TODO look for more problems with data struvtures for interviews
    # write hash-table implementation or hash function
    # repeat on self balancing binary search tree (2-3 tree, AA tree, AVL tree)
    # repeat over B-trees maybe try implement
    # reapeat on linear search algorithems

if __name__ == '__main__':
	main()