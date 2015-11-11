"""Run SSH asynchronously with :class:`Executor`."""
import asyncio
from shlex import quote
from .shell import Shell


class SSH(Shell):

    """Run SSH asynchronously.

    The difference between using this class and :class:`Shell` is that the
    remote stdout and stderr are also managed.
    For example, if a remote command prints long and useless output, it would
    be transfered throught the network and then discarded locally by
    :class:`Shell`. To solve this problem, SSH class manages also the remote
    stdout and stderr, so no bandwidth is wasted.

    SSH behaves like :class:`Shell` (subclass). The only difference is:

    :param string params: all ssh options. Requires hostname or IP address.
    """

    def __init__(self, params, cmd, title=None, stdout=None, stderr=None):
        """TODO constructor docstring."""
        if stdout is None:
            stdout = Shell.DEVNULL
        if stderr is None:
            stderr = Shell.TRUE

        remote_cmd = _redirect_outputs(cmd, stdout, stderr)
        local_cmd = 'ssh {} {}'.format(params, quote(remote_cmd))
        super().__init__(local_cmd, title=title, stdout=stdout, stderr=stderr)

    @asyncio.coroutine
    def run(self):
        return super().run()


def _redirect_outputs(cmd, stdout, stderr):
    """Can reduce the bandwidth and log size.

    :type stdout: Shell.TRUE, Shell.DEVNULL
    :type stderr: Shell.TRUE, Shell.DEVNULL, Shell.ERR2OUT
    """
    suffix = ''
    if stdout == Shell.DEVNULL:
        suffix += ' 1>/dev/null'
    if stderr == Shell.DEVNULL:
        suffix += ' 2>/dev/null'
    elif stderr == Shell.ERR2OUT:
        suffix += '2>&1'

    return cmd + suffix
