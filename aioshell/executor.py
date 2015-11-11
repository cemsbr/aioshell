"""This module provides only the Executor class."""
import asyncio
from .runnable import Runnable


class Executor:

    """Less boilerplate to run asynchronous tasks.

    **Basic usage**: call :func:`add` once for every :class:`Runnable` object
    (:class:`Shell`, :class:`SSH`) and, in the end, call :func:`finish`
    to wait for them to finish and clean resources. Example::

      from aioshell import Executor, Shell
      exe = Executor()
      exe.add(Shell('date >/tmp/aioshell; sleep 1'))
      exe.add(Shell('sleep 1; date >>/tmp/aioshell'))
      exe.finish()

    In the */tmp/test* file, you'll notice that it took only 1 second
    instead of 2.
    """

    _loop = None

    def __init__(self):
        """Get the main event loop."""
        self.futures = []
        """(*Advanced usage*) accumulated results of :func:`add`.

        Useful for further information about executions.
        If :func:`add` is called with a :class:`Runnable` or
        :ref:`coroutine <coroutine>` object, a correpondent Task will be
        appended to this list. If a :class:`Future <asyncio.Future>` is added,
        the Future itself will be appended.

        :type: list of :class:`Task <asyncio.Task>` or
            :class:`Future <asyncio.Future>`
        """
        self.loop = Executor._get_event_loop()
        """(*Advanced usage*) event loop.

        This event loop is shared between all objects until it is closed.
        If the loop is closed, automatically create a new one (it will also be
        shared between new objects).

        :type: :class:`BaseEventLoop <asyncio.BaseEventLoop>`
        """

    @classmethod
    def _get_event_loop(cls):
        """If the asyncio loop is closed, create a new one and set it."""
        if cls._loop is None:
            cls._loop = asyncio.get_event_loop()
        if cls._loop.is_closed():
            cls._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(cls._loop)
        return cls._loop

    def add(self, runnable_coro_future):
        """Run a Runnable (basic usage), coroutine or Future.

        *Note for advanced users:* each call will append a correspondent
        :class:`Task <asyncio.Task>` or :class:`Future <asyncio.Future>` to
        :attr:`futures` in case you want more information about the execution
        than provided by this class.

        :param runnable_coro_future: action to be performed asynchronously.
        :type runnable_coro_future: :class:`Runnable` (e.g. :class:`Shell`,
            :class:`SSH`), :ref:`coroutine <coroutine>` or
            :class:`Future <asyncio.Future>` objects
        """
        coro_future = _get_coro_future(runnable_coro_future)
        task = asyncio.ensure_future(coro_future)
        self.futures.append(task)
        return task

    def run_wait(self, runnable_coro_future):
        """Block until *runnable_coro_future* is finished.

        It will wait for only this `runnable_coro_future`.
        Useful if you want the traditional behaviour of sequential programming
        for some reason.
        Otherwise, use the concurrent and faster version :func:`add`.

        :param runnable_coro_future: action to be performed synchronously.
        :type runnable_coro_future: :class:`Runnable` (e.g. :class:`Shell`,
            :class:`SSH`), :ref:`coroutine <coroutine>` or
            :class:`Future <asyncio.Future>` objects
        """
        coro_future = _get_coro_future(runnable_coro_future)
        return self.loop.run_until_complete(coro_future)

    def wait(self):
        """Block until all added tasks by :func:`add` are done.

        You can add more tasks later.
        When you are finished, call :func:`finish`.
        """
        if self.futures:
            self.loop.run_until_complete(asyncio.wait(self.futures))

    def finish(self):
        """Wait for all tasks, close the event loop and clean resources.

        You should call this method in the end of your program.
        It performs 3 actions:

        #. Wait for all added tasks (by :func:`add`) to be finished
           (like :func:`wait` does);
        #. Clear :attr:`futures` list;
        #. Close the main event loop:

          * Allow clean exit, without warnings;
          * If you need to run anything else, use a new object of this class.
        """
        self.wait()
        self.loop.close()
        self.futures.clear()


def _get_coro_future(runnable_coro_future):
    """If it is a Runnable object, call run() to get the coroutine."""
    if isinstance(runnable_coro_future, Runnable):
        coro_future = runnable_coro_future.run()
    else:
        coro_future = runnable_coro_future
    return coro_future
