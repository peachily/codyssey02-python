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


# -------------- 커서 기반 원형 연결 리스트: circularlist ---------------
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

    # - delete(value) -> bool: 값이 같은 첫 노드 삭제(성공시 True, 실패시 False). 삭제 노드가 커서면 이전 노드로 이동한다. 만약 노드가 1개 있고 삭제되면 빈 상태가 된다.

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



# if __name__ == "__main__":

#     try:
#         input_data = input().strip()
#     except EOFError:
#         input_data = '1'

#     if input_data == '1':
#         # LinkedList 테스트 (기존 + 추가)
#         ll = LinkedList()

#         # 기본 테스트
#         ll.insert(0, 'a')
#         ll.insert(1, 'b')
#         ll.insert(1, 'X')
#         print(ll.to_list())  # 예상: ['a', 'X', 'b']
#         print(len(ll))  # 예상: 3
#         print(ll.delete(1))  # 예상: X
#         print(ll.to_list())  # 예상: ['a', 'b']
#         print(len(ll))  # 예상: 2

#         # 추가 테스트 (2배 확장)
#         ll.insert(0, 'Z')  # 맨 앞 삽입
#         print(ll.to_list())  # 예상: ['Z', 'a', 'b']
#         ll.insert(3, 'Y')  # 맨 뒤 삽입
#         print(ll.to_list())  # 예상: ['Z', 'a', 'b', 'Y']
#         print(len(ll))  # 예상: 4
#         print(ll.delete(0))  # 예상: Z (맨 앞 삭제)
#         print(ll.delete(2))  # 예상: Y (맨 뒤 삭제)
#         print(ll.to_list())  # 예상: ['a', 'b']
#         print(ll.delete(0))
#         print(ll.delete(0))
#         print(ll.to_list(), len(ll))
#         print(ll.delete(0))

#     else:
#         # CircularList 테스트 (기존 + 추가)
#         cl = CircularList()

#         # 기본 테스트
#         print(cl.get_next())  # 예상: None
#         cl.insert('A')
#         cl.insert('B')
#         cl.insert('C')
#         print(len(cl))  # 예상: 3
#         print(cl.get_next())  # 예상: A
#         print(cl.get_next())  # 예상: B
#         print(cl.search('B'))  # 예상: True
#         print(cl.search(999))  # 예상: False
#         print(cl.delete('A'))  # 예상: True
#         print(cl.delete(2))  # 예상: False
#         print(len(cl))  # 예상: 2
#         print([cl.get_next() for _ in range(4)])  # 예상: ['C', 'B', 'C', 'B']
#         print(cl.delete(42))  # 예상: False

#         # 추가 테스트 (2배 확장)
#         cl.insert('D')  # 추가 삽입
#         print(len(cl))  # 예상: 3
#         print(cl.search('D'))  # 예상: True
#         print(cl.get_next())  # 예상: B (순환 계속)
#         print(cl.delete('C'))  # 예상: True
#         print(len(cl))  # 예상: 2
#         print([cl.get_next() for _ in range(4)])  # 예상: ['D', 'B', 'D', 'B']