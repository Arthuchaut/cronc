from cronc.libs.task import Task, TCollection
import pathlib
from pprint import pp
import click
from cronc.libs.cronc import Cronc
from cronc.libs.task import Task


class Main:
    _CRONTAB_FILE: pathlib.Path = pathlib.Path('crontab')

    @click.group()
    def run() -> None:
        ...

    @run.command(help='Consult the tasks list.')
    @click.option(
        '--all',
        '-a',
        type=bool,
        is_flag=True,
        default=False,
        help='Show disabled tasks too.'
    )
    def ls(all: bool) -> None:
        cronc: Cronc = Cronc(Main._CRONTAB_FILE)
        tasks: TCollection = cronc.tasks

        if all:
            return print(tasks.as_table())

        tasks = TCollection(
            filter(lambda t: t.state == Task.STATUS.ENABLED, tasks)
        )
        print(tasks.as_table())

    @run.command(help='Add a new task')
    @click.option(
        '--schedule',
        '-s',
        type=str,
        required=True,
        help='The schedule of the task.'
    )
    @click.option(
        '--user',
        '-u',
        type=str,
        required=True,
        help='The user that\'ll be used to execute the command.'
    )
    @click.option(
        '--command',
        '-c',
        type=str,
        required=True,
        help='The command to execute.'
    )
    def add(schedule: str, user: str, command: str) -> None:
        cronc: Cronc = Cronc(Main._CRONTAB_FILE)
        task: Task = Task(schedule=schedule, user=user, command=command)
        cronc.add_task(task)
        cronc.save()

    @run.command(help='Add a new task')
    @click.option('--tid', '-i', type=int, required=True)
    @click.option(
        '--schedule', '-s', type=str, help='The schedule of the task.'
    )
    @click.option(
        '--user',
        '-u',
        type=str,
        help='The user that\'ll be used to execute the command.'
    )
    @click.option('--command', '-c', type=str, help='The command to execute.')
    def update(tid: int, schedule: str, user: str, command: str) -> None:
        cronc: Cronc = Cronc(Main._CRONTAB_FILE)
        task: Task = cronc.get_task(tid)

        if not task:
            return print(f'The task {tid} does not exists.')
        if schedule:
            task.schedule = schedule
        if user:
            task.user = user
        if command:
            task.command = command

        cronc.save()

    @run.command(help='Delete a specific task.')
    @click.option('--tid', '-i', type=int, required=True)
    def rm(tid: int) -> None:
        cronc: Cronc = Cronc(Main._CRONTAB_FILE)
        cronc.delete_task(tid)
        cronc.save()

    @run.command(help='Delete a specific task.')
    @click.option('--tid', '-i', type=int, required=True)
    def enable(tid: int) -> None:
        cronc: Cronc = Cronc(Main._CRONTAB_FILE)
        task: Task = cronc.get_task(tid)

        if not task:
            return print(f'The task {tid} does not exists.')

        task.state = Task.STATUS.ENABLED
        cronc.save()

    @run.command(help='Delete a specific task.')
    @click.option('--tid', '-i', type=int, required=True)
    def disable(tid: int) -> None:
        cronc: Cronc = Cronc(Main._CRONTAB_FILE)
        task: Task = cronc.get_task(tid)

        if not task:
            return print(f'The task {tid} does not exists.')

        task.state = Task.STATUS.DISABLED
        cronc.save()

    @run.command()
    def debug() -> None:
        cronc: Cronc = Cronc(Main._CRONTAB_FILE)
        t = cronc.get_task(0)
        t.state = Task.STATUS.ENABLED
        cronc.save()


if __name__ == '__main__':
    Main.run()
