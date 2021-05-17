import pathlib
import re
from cronc.libs.schedule import Schedule


class CrontabReader:
    __ENCODING: str = 'utf-8'

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
                        Schedule.STATUS.DISABLED \
                        if match.group(1) \
                        else Schedule.STATUS.ENABLED,
                        match.group(3)[:-1],
                        user,
                        command
                    )
                ]

        return tasks

    def write_task(self, schedule: Schedule) -> None:
        ...