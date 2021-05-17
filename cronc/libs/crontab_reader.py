import pathlib
import re
from pprint import pp
from dataclasses import dataclass


class _Status:
    DISABLED: str = 'DISABLED'
    ENABLED: str = 'ENABLED'


@dataclass
class Schedule:
    status: _Status
    calendar: str
    user: str
    command: str


class CrontabReader:
    __ENCODING: str = 'utf-8'

    Status: _Status = _Status

    def __init__(self, crontab_file: pathlib.Path) -> None:
        self.__crontab_file: pathlib.Path = crontab_file

    def read_tasks(self) -> list[Schedule]:
        tasks: list[Schedule] = []
        content: str = self.__crontab_file.read_text(encoding=self.__ENCODING)

        for line in content.split('\n'):
            if match := re.search(
                r'(#( )?)?((@(annually|yearly|monthly|weekly|daily|hourly'
                r'|reboot))|(@every (\d+(ns|us|µs|ms|s|m|h))+)|((((\d+,)+'
                r'\d+|(\d+(\/|-)\d+)|\d+|\*|\*\/) ?){5,7}))', line
            ):
                action: str = line[len(match.group(1) or '') +
                                   len(match.group(3)):]
                user: str = action.split()[0]
                command: str = action[len(user) + 1:]

                tasks += [
                    Schedule(
                        self.Status.DISABLED \
                        if match.group(1) \
                        else self.Status.ENABLED,
                        match.group(3)[:-1],
                        user,
                        command
                    )
                ]

        pp(tasks)