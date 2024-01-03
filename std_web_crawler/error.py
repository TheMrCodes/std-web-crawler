from typing import NoReturn


class ExitCode:
    SUCCESS = 0
    WORKER_TIMEOUT = 2



def error(msg: str) -> NoReturn:
    raise RuntimeError(msg)

def value_error(msg: str) -> NoReturn:
    raise ValueError(msg)