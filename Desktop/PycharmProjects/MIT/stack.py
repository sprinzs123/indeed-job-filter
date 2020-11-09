class Stack:
    def __init__(self):
        self.start = []

    def push(self, data):
        self.start.append(data)

    def pop(self):
        return self.start.pop()

    def peek(self):
        return self.start[-1]

    def result(self):
        return self.start

    def reverse(self):
        fin = ''
        while len(self.start) > 0:
            fin += self.start.pop()

        print(fin)
        return fin






stak = Stack()
example = '12345'
for i in example:
    stak.push(i)

stak.reverse()
# print(stak.pop())





