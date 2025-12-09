from typing import Any, Optional


class LinkedList:
    class _Node:
        def __init__(self, value: Any, next: Optional['LinkedList._Node'] = None):
            self.value = value
            self.next = next

    def __init__(self):
        self.head: Optional[LinkedList._Node] = None
        self._size = 0

    def insert(self, index: int, value: Any) -> None:
        if index < 0 or index > self._size:
            raise IndexError('Index out of range')

        if index == 0:
            self.head = LinkedList._Node(value, self.head)
        else:
            prev = self.head
            for _ in range(index - 1):
                prev = prev.next
            prev.next = LinkedList._Node(value, prev.next)

        self._size += 1

    def delete(self, index: int) -> Any:
        if index < 0 or index >= self._size:
            raise IndexError('Index out of range')

        if index == 0:
            deleted = self.head
            self.head = self.head.next
        else:
            prev = self.head
            for _ in range(index - 1):
                prev = prev.next
            deleted = prev.next
            prev.next = deleted.next

        self._size -= 1
        return deleted.value

    def to_list(self) -> list:
        result = []
        cur = self.head
        while cur:
            result.append(cur.value)
            cur = cur.next
        return result

    def __len__(self) -> int:
        return self._size


class CircularList:
    class _Node:
        def __init__(self, value: Any, next: Optional['CircularList._Node'] = None):
            self.value = value
            self.next = next

    def __init__(self):
        self.cursor: Optional[CircularList._Node] = None

    def insert(self, value: Any) -> None:
        new = CircularList._Node(value)

        if self.cursor is None:
            new.next = new
            self.cursor = new
        else:
            new.next = self.cursor.next
            self.cursor.next = new
            self.cursor = new

    def delete(self, value: Any) -> bool:
        if self.cursor is None:
            return False

        prev = self.cursor
        cur = self.cursor.next

        while True:
            if cur.value == value:
                # 삭제 시 한 개 노드뿐이면 빈 상태
                if cur is prev and cur is self.cursor:
                    self.cursor = None
                else:
                    prev.next = cur.next
                    if cur is self.cursor:
                        self.cursor = prev
                return True

            prev, cur = cur, cur.next

            if prev is self.cursor:
                break

        return False

    def get_next(self) -> Any | None:
        if self.cursor is None:
            return None
        self.cursor = self.cursor.next
        return self.cursor.value

    def search(self, value: Any) -> bool:
        if self.cursor is None:
            return False

        cur = self.cursor
        while True:
            if cur.value == value:
                return True
            cur = cur.next
            if cur is self.cursor:
                break
        return False


def main():
    # 아래는 샘플 데모 (자동채점과 무관 / 자유)
    # ▶ Singly Linked List
    lst = LinkedList()
    lst.insert(0, 'A')
    lst.insert(1, 'B')
    lst.insert(1, 'C')
    print(len(lst))
    print(lst.to_list())
    print(lst.delete(1))
    print(lst.to_list())
    print(len(lst))

    # ▶ Circular Linked List
    cl = CircularList()
    print(cl.get_next())
    for v in ['A', 'B', 'C']:
        cl.insert(v)

    print(cl.delete('B'))
    print(cl.delete('X'))

    prints = []
    for _ in range(5):
        prints.append(cl.get_next())
    print(prints)

    print(cl.search('A'))
    cl.delete('A')
    cl.delete('C')
    prints = []
    for _ in range(4):
        prints.append(cl.get_next())
    print(prints)
    print(cl.search('B'))


if __name__ == '__main__':
    main()
