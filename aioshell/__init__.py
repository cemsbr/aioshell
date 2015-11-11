"""Run single-threaded concurrent shell and ssh commands with few keystrokes.

A simpler way to use Python's new :mod:`asyncio <python:asyncio>` module, making
it easier and faster to run shell and ssh commands.
"""
from .runnable import Runnable  # noqa
from .executor import Executor  # noqa
from .shell import Shell        # noqa
from .ssh import SSH            # noqa
