class Node(object):
    def __init__(self, data=None):
        self.data = data
        self.next = None

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next

    def set_next(self, new_next):
        self.next = new_next


class LinkedList(object):
    def __init__(self):
        self.head = None
        self.size = 0

    # works
    def insert_start(self, data):
        self.size += 1
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            self.size += 1
            new_node = Node(data)
            new_node.set_next(self.head)
            self.head = new_node

    def size(self):
        return str(self.size)

    def size2(self):
        actual_node = self.head
        size = 0
        while actual_node:
            size += 1
            actual_node = actual_node.get_next()
        return size

    # works
    def combine_sorted(self, lst_1, lst_2):
        all_nodes = []
        current = lst_1.head
        current_2 = lst_2.head

        while current:
            if current.data > current_2.data:
                all_nodes.append(current_2.data)
                current_2 = current_2.next
            if current.data < current_2.data:
                all_nodes.append(current.data)
                current = current.next
        if current_2 is not None:
            while current_2:
                all_nodes.append(current_2.data)
                current_2 = current_2.next
        return all_nodes


                # works
    def list_nodes(self):
        all_nodes = []
        actual_node = self.head
        while actual_node:
            all_nodes.append(actual_node.data)
            actual_node = actual_node.get_next()
        return all_nodes

    # works
    def delete(self, data):
        current = self.head
        previous = None
        found = False
        while current and found is False:
            if current.data == data:
                found = True
                print(previous.data, current.data)
                previous.next = current.next
            else:
                previous = current
                current = current.get_next()

    # works
    def insert_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            actual_node = self.head
            while actual_node.next is not None:
                actual_node = actual_node.next
            actual_node.next = new_node

    # works
    def reverse_list(self):
        current = self.head
        previous = None
        while current:
            next_one = current.next
            current.next = previous
            previous = current
            current = next_one
        self.head = previous

    # works
    def get_index(self, index):
        current = self.head
        count = 0
        while current:
            if count == index:
                return current.data
            else:
                count += 1
                current = current.next

    def reverse(self):
        current_node = self.head
        previous = None
        while current_node:
            next = current_node.next
            current_node.next = previous
            previous = current_node
            current_node = next
        self.head = previous

link = LinkedList()
link.insert_start(8)
link.insert_start(4)
link.insert_start(1)
# 321 order

link2 = LinkedList()
link2.insert_start(11)
link2.insert_start(9)
link2.insert_start(3)
link2.insert_start(2)


combined =LinkedList()
combined.combine_sorted(link, link2)

# link.reverse_list()
# print(link2.list_nodes())
# print(link.get_index(0))



