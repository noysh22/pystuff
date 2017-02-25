class BinTree(object):
    """Represent a tree object"""
    def __init__(self, data, tree_left = None, tree_right = None):
        self.__tree_left = tree_left
        self.__tree_right = tree_right
        self.__data = data

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value

    @property
    def left(self):
        return self.__tree_left

    @left.setter
    def left(self, value):
        self.__tree_left = value

    @property
    def right(self):
        return self.__tree_right

    @right.setter
    def right(self, value):
        self.__tree_right = value

    @property
    def is_leaf(self):
        return self.left == None and self.right == None

    @staticmethod
    def add_tree(tree, value):
        """ 
            Add a sub tree by it's value to the correct place in the tree
            In case a value that already exists given 
            it will be added to the right side of the tree
        """
        if tree == None:
            return BinTree(value)

        if tree.data > value:
            tree.left = BinTree.add_tree(tree.left, value)
        else:
            tree.right = BinTree.add_tree(tree.right, value)

        return tree

    @staticmethod
    def inorder(tree):
        """
            Travel the tree in a inorder way
        """
        if tree == None:
            return

        BinTree.inorder(tree.left)
        print("%s" % tree.data)
        BinTree.inorder(tree.right)

    @staticmethod
    def preorder(tree):
        """
            Travel the tree in a preorder way
        """
        if tree == None:
            return

        print("%s" % tree.data)
        BinTree.preorder(tree.left)
        BinTree.preorder(tree.right)
        

    @staticmethod
    def postorder(tree):
        """
            Travel the tree in a postorder way
        """
        if tree == None:
            return

        BinTree.postorder(tree.left)
        BinTree.postorder(tree.right)
        print("%s" % tree.data)

    @staticmethod
    def breadthfirst(tree):
        """
            Traverse the tree in a breadth first method
        """
        que = []
        que.insert(0, tree)
        
        while(que):
            item = que.pop()
            print("%s" % item.data)
            if item.left != None:
                que.insert(0, item.left)
            if item.right != None:
                que.insert(0, item.right)
