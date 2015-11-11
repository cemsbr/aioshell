"""Run shell commands asynchronously with :class:`Executor`."""
from subprocess import CalledProcessError
import asyncio
from .runnable import Runnable


class Shell(Runnable):

    """Run shell commands asynchronously with few keystrokes.

    Examples::

        from aioshell import Executor, Shell
        exe = Executor()

        # If you don't care about shell's output
        exe.add(Shell('date >/tmp/aioshell'))

        # Output can be read later from Shell object
        shell = Shell('date', stdout=Shell.TRUE)
        exe.add(shell)

        # We won't add any other task, so let's finish:
        exe.finish()

        # All the tasks are done after finish(), so stdout is now available:
        print(shell.stdout)

    The constructor has all the information to run a shell command.
    It will be run after being passed as an argument to
    :func:`Executor.add`.
    The default behavior is to capture only stderr output (for error
    debugging).

    :param str cmd: shell command to be executed.
    :param str title: a meaninful name for your task for debugging purposes.
    :param stdout: whether or not to capture stdout. Default: don't capture.
    :type stdout: :const:`Shell.DEVNULL` or :const:`Shell.TRUE`
    :param stderr: whether or not to capture stderr. Default: capture.
    :type stderr: :const:`Shell.TRUE`, :const:`Shell.DEVNULL` or
        :const:`Shell.ERR2OUT`

    :var str cmd: shell command (constructor's argument).
    :var str title: title as in the constructor.
    :var int returncode: shell exit code.
    :var str stdout: shell standard output. None if not requested or not
        executed.
    :var str stderr: shell standard error. None if not requested or not
        executed.
    """

    TRUE = asyncio.subprocess.PIPE
    """Capture stdout or stderr output."""
    DEVNULL = asyncio.subprocess.DEVNULL
    """Ignore stdout or stderr output."""
    ERR2OUT = asyncio.subprocess.STDOUT
    """Mix stderr and stdout outputs in stdout."""

    def __init__(self, cmd, title=None, stdout=None, stderr=None):
        """Create the object without running *cmd* yet."""
        if title is None:
            title = cmd
        if stdout is None:
            stdout = Shell.DEVNULL
        if stderr is None:
            stderr = Shell.TRUE

        self.cmd, self.title = cmd, title
        self._stdout, self._stderr = stdout, stderr
        self.returncode = self.stdout = self.stderr = None

    @asyncio.coroutine
    def run(self):
        """*(coroutine)* Execute shell command asynchronously.

        You should not call this method directly. Instead, pass this object as
        an argument to :func:`Executor.add`.

        :return: coroutine for the shell stdout (also found as an attribute).
        :rtype: :ref:`coroutine <coroutine>`, str
        :raises: :class:`CalledProcessError <subprocess.CalledProcessError>`
        """
        # Create the subprocess, redirect the standard output into a pipe
        shell = yield from asyncio.create_subprocess_shell(self.cmd,
                                                           stdout=self._stdout,
                                                           stderr=self._stderr)
        rcode, stdout, stderr = yield from self._get_process_info(shell)
        self.returncode, self.stdout, self.stderr = rcode, stdout, stderr

        if rcode != 0:
            raise CalledProcessError(rcode, self.cmd, stdout, stderr)
        else:
            return self.stdout

    @asyncio.coroutine
    def _get_process_info(self, shell):
        stds_bytes = yield from shell.communicate()
        stdout = _get_output(self._stdout, stds_bytes[0])
        stderr = _get_output(self._stderr, stds_bytes[1])

        return shell.returncode, stdout, stderr


def _get_output(requested, actual):
    if requested == Shell.DEVNULL:
        output = None
    else:
        output = actual.decode().rstrip()
    return output
