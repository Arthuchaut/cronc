import pathlib
import re
from cronc.libs.task import Task, TCollection


class CrontabIO:
    __ENCODING: str = 'utf-8'

    def __init__(self, crontab_file: pathlib.Path) -> None:
        self.__crontab_file: pathlib.Path = crontab_file

    def read_params(self) -> str:
        params: str = ''
        content: str = self.__crontab_file.read_text(encoding=self.__ENCODING)
        for line in content.split('\n'):
            if match := re.search(r'^[A-Z]+=[a-z\/:-_\"\']+$', line):
                params += line + '\n'

        return params

    def read_tasks(self) -> TCollection:
        t_col: TCollection = TCollection()
        content: str = self.__crontab_file.read_text(encoding=self.__ENCODING)
        Task.reset_ids()

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
                t_col += [
                    Task(
                        Task.STATUS.DISABLED \
                        if match.group(1) \
                        else Task.STATUS.ENABLED,
                        match.group(3)[:-1],
                        user,
                        command
                    )
                ]

        return t_col

    def write_tasks(self, tasks: TCollection) -> None:
        content: str = self.read_params() + '\n'

        for task in tasks:
            content += task.as_string() + '\n'

        self.__crontab_file.write_text(content, encoding=self.__ENCODING)