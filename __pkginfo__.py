# Copyright (C) 2009-2010, 2013, 2015, 2017,
# 2020-2021, 2024 Rocky Bernstein <rocky@gnu.org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""packaging information"""
import sys

copyright = """
Copyright (C) 2008-2010, 2012-2013, 2015-2018, 2020-2021, 2024 Rocky Bernstein <rocky@gnu.org>.
"""
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Programming Language :: Python",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Programming Language :: Python :: 2.4",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.0",
    "Programming Language :: Python :: 3.1",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: Implementation :: PyPy",
]

SYS_VERSION = sys.version_info[0:2]
if (3, 0) <= SYS_VERSION < (3, 3):
    pygments_version = "pygments == 2.0.0"  # I have my own patch for this
else:
    pygments_version = "pygments>= 2.2.0"


# The rest in alphabetic order
author = "Rocky Bernstein"
author_email = "rocky@gnu.org"
ftp_url = None
install_requires = [
    pygments_version,
    "xdis >= 6.0.0, < 6.2.0",
    "term-background >= 1.0.1",
]

license = "GPL"
mailing_list = None
modname = "pyficache"
py_modules = [modname]

short_desc = "Cache lines and file information which are generally Python programs"

# version.py sets variable __version__.
import os.path as osp

exec(
    compile(
        open(osp.join(osp.dirname(__file__), "pyficache", "version.py")).read(),
        osp.join(osp.dirname(__file__), "version.py"),
        "exec",
    )
)

web = "http://github.com/rocky/python-filecache"

zip_safe = False  # tracebacks in zip files are funky and not debuggable


def read(*rnames):
    return open(osp.join(osp.dirname(__file__), *rnames)).read()


long_description = read("README.rst") + "\n"
