class Queue(object):
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop()

    def is_empty(self):
        return len(self.items) == 0

    def peek(self):
        if not self.is_empty():
            return self.items[-1].value

    def __len__(self):
        return self.size()

    def size(self):
        return len(self.items)


class Node(object):
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None


class BinaryTree(object):
    def __init__(self):
        self.root = None

    def print_tree(self, traversal_style):
        if traversal_style == 'preorder':
            return self.preorder_print(self.root, '')
        elif traversal_style == 'inorder':
            return self.inorder_print(self.root, '')
        elif traversal_style == 'postorder':
            return self.postorder_print(self.root, '')
        elif traversal_style == 'leveleorder':
            return self.levelorder_print(self.root)
        else:
            print('traversal type not supported')

    def get_root(self):
        return self.root

    def get_root_data(self):
        return self.root.value

    # root > left > right
    def preorder_print(self, start, traversal):
        if start:
            traversal += (str(start.value) + '-')
            traversal = self.preorder_print(start.left, traversal)
            traversal = self.preorder_print(start.right, traversal)
        return traversal

    # left > root > right
    def inorder_print(self, start, traversal):
        if start:
            traversal = self.inorder_print(start.left, traversal)
            traversal += (str(start.value) + '-')
            traversal = self.preorder_print(start.right, traversal)
        return traversal

    # left > right > root
    def postorder_print(self, start, traversal):
        if start:
            traversal = self.inorder_print(start.left, traversal)
            traversal = self.preorder_print(start.right, traversal)
            traversal += (str(start.value) + '-')
        return traversal

    def levelorder_print(self, start):
        if start is None:
            return
        queue = Queue()
        queue.enqueue(start)
        traversal = ''
        while len(queue) > 0:
            traversal += str(queue.peek()) + '-'
            node = queue.dequeue()
            if node.left:
                queue.enqueue(node.left)
            if node.right:
                queue.enqueue(node.right)
        return traversal

    # check if tree is balanced
    def height_dif(self, node):
        if node is None:
            return -1
        left_height = self.height_dif(node.left)
        right_height = self.height_dif(node.right)
        difference = left_height - right_height
        return difference

    def is_balanced(self):
        if abs(self.height(self.root)) > 1:
            return False
        else:
            return True

    def rotate_tree(self, node):
        if node is None:
            return -1
        else:
            if self.is_balanced() is False:
                if self.height_dif(self.root) > 1:
                    node = node.right
                    self.rotate_tree(node)
                if self.height_dif(self.root) < -1:
                    node = node.left
                    self.rotate_tree(node)

    # height of children nodes usually used test if tree is balanced
    def height(self, node):
        if node is None:
            return -1
        left_height = self.height(node.left)
        right_height = self.height(node.right)
        return 1 + max(left_height, right_height)

    # inserting new nodes to tree
    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert(data, self.root)

    def _insert(self, data, current_node):
        if data < current_node.value:
            if current_node.left is None:
                current_node.left = Node(data)
            else:
                self._insert(data, current_node.left)
        elif data > current_node.value:
            if current_node.right is None:
                current_node.right = Node(data)
            else:
                self._insert(data, current_node.right)
        else:
            print('value already present in tree')

    def find(self, data):
        if self.root:
            is_found = self._find(data, self.root)
            if is_found:
                return True
            return False
        else:
            return None

    def _find(self, data, current_node):
        if data > current_node.value and current_node.right:
            return self._find(data, current_node.right)
        elif data < current_node.value and current_node.left:
            return self._find(data, current_node.left)
        if data == current_node.value:
            return True



make_tree = [1, 2, 3, 4, 5]
new = BinaryTree()
for i in make_tree:
    new.insert(i)

root_node = new.get_root()
# print(new.height(root_node))
# print(new.find(11))
print(new.is_balanced())
new.rotate_tree(root_node)
print(new.is_balanced())


# create tree
# tree = BinaryTree(1)
# tree.root.left = Node(2)
# tree.root.right = Node(3)
# tree.root.left.left = Node(4)
# tree.root.left.right = Node(5)
# tree.root.right.right = Node(7)
# tree.root.right.left = Node(6)
# tree.root.right.right.right = Node(8)


#           1
#         2     3
#       4   5   6 7
#
#
# pre order traversal
# 1-2-4-5-3-6-7-
# print(tree.print_tree('preorder'))

# 4-2-5-1-3-6-7-
# print(tree.print_tree('inorder'))

# 4-2-5-3-6-7-1-
# print(tree.print_tree('postorder'))

# 1-2-3-4-5-6-7-
# print(tree.print_tree('leveleorder'))


# print(tree.height(tree.root))
