class _Status:
    DISABLED: str = 'DISABLED'
    ENABLED: str = 'ENABLED'


class Schedule:
    STATUS: _Status = _Status

    def __init__(
        self, state: _Status, calendar: str, user: str, command: str
    ) -> None:
        self.state: _Status = state
        self.calendar: str = calendar
        self.user: str = user
        self.command: str = command
