"""Interface for running async code through :class:`Executor`."""
from abc import ABCMeta, abstractmethod
import asyncio


class Runnable(metaclass=ABCMeta):

    """Interface used by :class:`Executor`.

    Implement this interface to easily run asynchronous code with
    :func:`Executor.add()`.

    Current implementations: :class:`Shell`, :class:`SSH`.
    """

    @asyncio.coroutine
    @abstractmethod
    def run(self):
        """Coroutine called by :func:`Executor.add()`, without arguments.

        If you need arguments, keep them as attributes instead.
        """
        pass
