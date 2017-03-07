|Linux Build Status| |Windows Build Status| |License| |Supported Python Versions|

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
different from the path on a local filesystem. In the `trepan <https://pypi.python.org/pypi/trepan>`_
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

coverage_ provides the cool stuff to figure out lines where there
statements.

Other stuff
-----------

Author:   Rocky Bernstein <rockyb@rubyforge.net>
License:  Copyright (c) 2009, 2015, 2016 Rocky Bernstein. Released under the GNU GPL 3 license

.. |License| image:: https://img.shields.io/pypi/l/pyficache.svg
    :target: https://pypi.python.org/pypi/pyfiecache
    :alt: License
.. _coverage: http://nedbatchelder.com/code/coverage/
.. _linecache: https://rubygems.org/gems/linecache
.. _trepan: :target https://pypi.python.org/pypi/trepan

.. |Downloads| image:: https://pypip.in/download/pyficache/badge.svg
.. |Linux Build Status| image:: https://travis-ci.org/rocky/python-filecache.svg
   :target: https://travis-ci.org/rocky/python-filecache/
.. |Windows Build status| image:: https://img.shields.io/appveyor/ci/rocky/python-filecache/master.svg?label=windows%20build
   :target: https://ci.appveyor.com/project/rocky/python-filecache/branch/master
.. |Latest Version| image:: https://pypip.in/version/pyficache/badge.svg?text=version
   :target: https://pypi.python.org/pypi/pyficache/
.. |Supported Python versions| image:: https://pypip.in/py_versions/pyficache/badge.svg
   :target: https://pypi.python.org/pypi/pyficache/
.. |Supported Python Versions| image:: https://img.shields.io/pypi/pyversions/pyficache.svg
   :target: https://pypi.python.org/pypi/pyficache/
