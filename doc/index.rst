.. aioshell documentation master file, created by
   sphinx-quickstart on Thu Nov 12 12:21:18 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to aioshell's documentation!
======================================

Run shell and SSH commands concurrently inside Python code with few keystrokes
and the new powerful Python's :mod:`asyncio` module (since version 3.4).
Quick example::

  from aioshell import Executor, Shell
  exe = Executor()
  exe.add(Shell('date >/tmp/aioshell; sleep 1'))
  exe.add(Shell('sleep 1; date >>/tmp/aioshell'))
  exe.finish()
  # Check /tmp/aioshell file to see that only 1 sec has passed.

Contents:

.. toctree::
   :maxdepth: 2

   aioshell/index.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
