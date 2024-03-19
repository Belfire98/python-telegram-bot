import contextlib
import sys
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union

T = TypeVar("T")


class ContextManager:
    def __init__(self, enter_fn: Callable[[], T], exit_fn: Callable[[T], None]):
        self.enter_fn = enter_fn
        self.exit_fn = exit_fn

    def __enter__(self) -> T:
        self.value = self.enter_fn()
        return self.value

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]):
        self.exit_fn(self.value)


@contextlib.contextmanager
def contextmanager_demo(value: int) -> ContextManager[int]:
    entered_value = None

    def enter_fn() -> int:
        nonlocal entered_value
        print("Entering contextmanager_demo with value:", value)
        entered_value = value
        return entered_value

    def exit_fn(entered_value: int) -> None:
        print("Exiting contextmanager_demo with value:", entered_value)

    yield ContextManager(enter_fn, exit_fn)


def main() -> None:
    with contextmanager_demo(5) as manager:
        print("Inside contextmanager_demo with value:", manager.value)


if __name__ == "__main__":
    sys.exit(main())
