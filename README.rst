|TravisCI| |CircleCI| |Pypi Installs| |License| |Supported Python Versions|

|packagestatus|

Synopsis
--------

The *pyficache* module allows one to get any line from any file,
caching lines of the file on first access to the file. Although the
file may be any file, this package is more tailored to the case
where the file is a Python script.

Here, the file is parsed to determine statement bounderies,
and a copies of the file syntax-highlighted are also saved.

Also saved is file information such as when the file was last modified
and a SHA1 of the file. These are useful in determining if the file
has changed and verifying the contents of the file.

By caching contents, access is sped up when small small random sets of lines
are read from a single file, in particular in a debugger to show
source lines.

A file path can be remapped to another path. This is useful for
example when debugging remotely and the remote file path may be
different from the path on a local filesystem. In the `trepan2 <https://pypi.python.org/pypi/trepan2>`_
`debugger <https://pypi.python.org/pypi/trepan3k>`_, *eval* and *exec* strings are
saved in a temporary file and then the pseudo-filename `<string>` is
remapped to that temporary file name.

Similarly lines within a file can be remapped to other lines. This may
be useful in preprocessors or template systems where ones wants to
make a correspondence between the template file and the expanded
Python file as seen in a tool using that underlying Python file such as
a debugger or profiler.

Summary
-------

.. code:: python

    import pyficache
    filename = __file__ # e.g. '/tmp/myprogram'
     # return all lines of filename as an array
    lines = pyficache.getlines(filename)

     # return line 6, and reload all lines if the file has changed.
    line = pyficache.getline(filename, 6, {'reload_on_change': True})

    # return line 6 syntax highlighted via pygments using style 'emacs'
    line = pyficache.getline(filename, 6, {'style': 'emacs'})

    pyficache.remap_file('/tmp/myprogram.py', 'another-name')
    line_from_alias = pyficache.getline('another-name', 6)

    assert __file__, pyficache.remove_remap_file('another-name')

    # another-name is no longer an alias for /tmp/myprogram
    assert None, pyficache.remove_remap_file('another-name')

    # Clear cache for __file__
     pyficache.clear_file_cache(__file__)

    # Clear all cached files.
    pyficache.clear_file_cache()

    # Check for modifications of all cached files.
    pyficache.update_cache()

Credits
-------

This is a port of the my Ruby linecache_ module which in turn is based
on the Python linecache module.

xdis_ provides the cool stuff to figure out the lines containing
Python statements.

.. |License| image:: https://img.shields.io/pypi/l/pyficache.svg
    :target: https://pypi.python.org/pypi/pyficache
    :alt: License
.. _xdis: https://pypi.org/project/xdis/
.. _linecache: https://rubygems.org/gems/linecache

.. |Downloads| image:: https://img.shields.io/pypi/dm/pyficache.svg
.. |TravisCI| image:: https://travis-ci.org/rocky/python-filecache.svg
   :target: https://travis-ci.org/rocky/python-filecache/
.. |CircleCI| image:: https://circleci.com/gh/rocky/python-filecache.svg?style=svg
    :target: https://circleci.com/gh/rocky/python-filecache
.. |Supported Python Versions| image:: https://img.shields.io/pypi/pyversions/pyficache.svg
.. |Pypi Installs| image:: https://pepy.tech/badge/pyficache/month
.. |packagestatus| image:: https://repology.org/badge/vertical-allrepos/python:pyficache.svg
		 :target: https://repology.org/project/python:pyficache/versions
