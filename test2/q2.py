from typing import Any

class stack:
    def __init__(self):
        self.data = []
        self.capacity = 10

    def push(self, value: Any) -> bool:
        if len(self.data) >= self.capacity:
            print("Stack is full.")
            return False
        self.data.append(value)
        return True

    def pop(self) -> object | None:
        if len(self.data) == 0:
            print("Stack is empty.")
            return None
        return self.data.pop()

    def empty(self) -> bool:
        return len(self.data) == 0

    def peek(self) -> object | None:
        if len(self.data) == 0:
            return None
        return self.data[-1]


def main():
    s = stack()
    pass


if __name__ == "__main__":
    main()
