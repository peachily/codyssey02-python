def main():
    pass

class _Node:
    __slots__ = ('value', 'next')

    def __init__(self, value, nxt=None):
        self.value = value
        self.next = nxt


class LinkedList:
    def __init__(self):
        self._head = None
        self._size = 0

    def insert(self, index, value):
        if not isinstance(index, int):
            raise TypeError
        if index < 0 or index > self._size:
            raise IndexError

        new_node = _Node(value)
        if index == 0:
            new_node.next = self._head
            self._head = new_node
        else:
            prev = self._head
            for _ in range(index - 1):
                if prev is None:
                    raise RuntimeError
                prev = prev.next
            new_node.next = prev.next
            prev.next = new_node

        self._size += 1

    def delete(self, index):
        if not isinstance(index, int):
            raise TypeError
        if index < 0 or index >= self._size:
            raise IndexError

        if index == 0:
            deleted = self._head
            self._head = self._head.next
        else:
            prev = self._head
            for _ in range(index - 1):
                if prev is None:
                    raise RuntimeError
                prev = prev.next
            if prev is None or prev.next is None:
                raise RuntimeError
            deleted = prev.next
            prev.next = deleted.next
        self._size -= 1
        return deleted.value

    def to_list(self):
        out = []
        cur = self._head
        while cur is not None:
            out.append(cur.value)
            cur = cur.next
        return out

    def __len__(self):
        return self._size

class _CNode:
    __slots__ = ('value', 'next')

    def __init__(self, value, nxt=None):
        self.value = value
        self.next = nxt

class CircularList:
    def __init__(self):
        self._cursor = None
        self._size = 0

    def insert(self, value):
        new_node = _CNode(value)
        if self._cursor is None:
            new_node.next = new_node
            self._cursor = new_node
        else:
            new_node.next = self._cursor.next
            self._cursor.next = new_node
            self._cursor = new_node
        self._size += 1

    def delete(self, value):
        if self._cursor is None:
            return False

        prev = self._cursor
        cur = self._cursor.next
        for _ in range(self._size):
            if cur.value == value:
                if self._size == 1:
                    self._cursor = None
                else:
                    prev.next = cur.next
                    if self._cursor is cur:
                        self._cursor = prev
                self._size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def get_next(self):
        if self._cursor is None:
            return None
        self._cursor = self._cursor.next
        return self._cursor.value

    def search(self, value):
        if self._cursor is None:
            return False
        cur = self._cursor
        for _ in range(self._size):
            if cur.value == value:
                return True
            cur = cur.next
        return False

    def __len__(self):
        return self._size


if __name__ == "__main__":
    main()