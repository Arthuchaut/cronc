import pathlib
from cronc.libs.crontabio import CrontabIO
from cronc.libs.task import Task, TCollection


class Cronc:

    def __init__(self, crontab_file: pathlib.Path) -> None:
        self.__crontabio: CrontabIO = CrontabIO(crontab_file)
        self.tasks: TCollection = self.__crontabio.read_tasks()

    def add_task(self, task: Task) -> None:
        self.tasks += [task]

    def get_task(self, tid: int) -> Task:
        filtered_tasks: list[Task] = list(
            filter(lambda t: t.tid == tid, self.tasks)
        )
        return filtered_tasks[0] if len(filtered_tasks) else None

    def delete_task(self, tid: int) -> None:
        filtered_tasks: list[Task] = list(
            filter(lambda t: t.tid == tid, self.tasks)
        )

        if len(filtered_tasks):
            task = filtered_tasks[0]
            self.tasks.remove(task)

    def save(self) -> None:
        self.__crontabio.write_tasks(self.tasks)
