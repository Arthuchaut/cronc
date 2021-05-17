from __future__ import annotations
from itertools import count
from typing import Any, Callable, Iterable, Iterator, overload
from tabulate import tabulate


class _Status:
    DISABLED: str = 'DISABLED'
    ENABLED: str = 'ENABLED'


class Task:
    STATUS: _Status = _Status
    _ids: Iterator = count(0)

    def __init__(
        self, state: _Status, schedule: str, user: str, command: str
    ) -> None:
        self.tid: int = next(self._ids)
        self.state: _Status = state
        self.schedule: str = schedule
        self.user: str = user
        self.command: str = command

    @classmethod
    def reset_ids(cls) -> None:
        cls._ids = count(0)

    def as_string(self) -> str:
        return f'{"# " if self.state == self.STATUS.DISABLED else ""}' \
               f'{self.schedule} ' \
               f'{self.user} ' \
               f'{self.command}'

    def as_list(self) -> list[str]:
        return [self.tid, self.state, self.schedule, self.user, self.command]

    def readable_schedule(self) -> str:
        # TODO: do the do.
        ...

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} ' \
               f'tid={self.tid}, ' \
               f'state={self.state}, ' \
               f'schedule={self.schedule}, ' \
               f'user={self.user}, ' \
               f'command={self.command}>'


class TCollection(list):

    def as_table(self) -> str:
        if len(self):
            tasks_tab: list[list[str]] = [task.as_list() for task in self]
            return tabulate(
                tasks_tab, headers=[k for k in self[0].__dict__.keys()]
            )

    def append(self, task: Task) -> None:
        self.__raise_for_object(task)
        super().append(task)

    def __add__(self, tasks: Iterable[Task]) -> TCollection:
        for t in tasks:
            self.__raise_for_object(t)

        return super().__add__(tasks)

    def __iadd__(self, tasks: Iterable[Task]) -> TCollection:
        for t in tasks:
            self.__raise_for_object(t)

        return super().__iadd__(tasks)

    def __raise_for_object(self, obj: Any) -> None:
        if not isinstance(obj, Task):
            raise TypeError('The object must be an instance of Task.')
