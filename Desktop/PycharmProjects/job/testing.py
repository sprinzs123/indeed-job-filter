# this a mock up how filter is going to be implemented and data from input field is going to be gathered

all_inputs = {'title-0': 'network', 'title-1': 'it', 'subject-0': 'python'}
combined_filters = {'title': [], 'subject': []}

all_titles = []
for i in all_inputs:
    if i.startswith('title'):
        name = all_inputs.get(i)
        all_titles.append(name)


class Node(object):
    def __init__(self, title=None, subject=None):
        self.title = title
        self.subject = subject
        self.next = None


class LinkedList(object):
    def __init__(self):
        self.head = None

    def insert_start(self, title, subject):
        new_node = Node(title, subject)
        if self.head is None:
            self.head = new_node
        else:
            old_head = self.head
            new_node.next = old_head
            self.head = new_node

    def final_results(self):
        if self.head is None:
            return False
        else:
            all_results = {}
            current_node = self.head
            while current_node:
                one_job = {'title': current_node.title, 'subject': current_node.subject}
                all_results.update({1: one_job})
                current_node = current_node.next
            return all_results

    # iterate through nodes to filter by category
    def filter_titles(self, titles_list):
        current = self.head
        previous = None
        while current:
            # print(current.title)
            if current.title in title_filters:
                previous.next = current.next
                current = current.next
            else:
                previous = current
                current = current.next



# testing for filter implementation
test = LinkedList()
dummy_items = [['python', 'python'], ['networking person', 'C#'], ]

# adding items
for item in dummy_items:
    test.insert_start(item[0], item[1])

title_filters = ['python', 'filter']
test.filter_titles(title_filters)




