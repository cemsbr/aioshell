aioshell
========

Run single-threaded concurrent shell and SSH commands with few keystrokes.

.. code:: python

    from aioshell import Executor, Shell
    exe = Executor()
    exe.add(Shell('date >/tmp/aioshell; sleep 1'))
    exe.add(Shell('sleep 1; date >>/tmp/aioshell'))
    exe.finish()
    # Check /tmp/aioshell file to see that only 1 sec has passed.

For more details, please, `Read the Docs
<http://aioshell.rtfd.org/en/latest/>`_.
