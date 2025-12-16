class Node:
    def __init__(self, item, next=None):
        self.item = item
        self.next = next


class Stack:
    MAX_SIZE = 10

    def __init__(self):
        self._top = None
        self._size = 0

    def empty(self) -> bool:
        return self._top is None

    def size(self):
        return self._size

    def push(self, item) -> bool:
        if self.size() >= self.MAX_SIZE:
            print(f'Stack is Full!')
            return False

        new_node = Node(item, self._top)
        self._top = new_node
        self._size += 1
        return True

    def pop(self) -> object | None:
        if self.empty():
            print('Empty Stack!')
            return None

        item = self._top.item
        self._top = self._top.next
        self._size -= 1
        return item

    def peek(self) -> object | None:
        if self.empty():
            print('Empty Stack!')
            return None
        return self._top.item

    def __str__(self):
        items = []
        cur = self._top
        while cur:
            items.append(cur.item)
            cur = cur.next
        return f'Stack({items[::-1]})'

# if __name__ == '__main__':
# 문제