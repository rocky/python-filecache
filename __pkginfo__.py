# Copyright (C) 2009 Rocky Bernstein <rocky@gnu.org>
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

modname = 'pyficache'

numversion = (0, 1, 0)
version = '.'.join([str(num) for num in numversion])

short_desc = \
'Cache lines and information of files which are often Python programs'

author = "Rocky Bernstein"
author_email = "rocky@gnu.org"

classifiers =  ['Development Status :: 4 - Beta',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: GNU General Public License (GPL)',
                'Programming Language :: Python',
                'Topic :: Software Development :: Libraries :: Python Modules',
                ]
# download_url = '%s-%s.egg' % (modname, version,)

install_requires   = ['coverage']
py_modules = [modname]

web = 'http://code.google.com/p/pyficache'

zip_safe = False # tracebacks in zip files are funky and not debuggable
