# Copyright (C) 2009, 2010, 2013 Rocky Bernstein <rocky@gnu.org>
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

copyright   = '''Copyright (C) 2008-2010, 2012-2013 Rocky Bernstein <rocky@gnu.org>.'''
classifiers =  ['Development Status :: 4 - Beta',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: GNU General Public License (GPL)',
                'Programming Language :: Python',
                'Topic :: Software Development :: Libraries :: Python Modules',
                ]

# The rest in alphabetic order
author             = "Rocky Bernstein"
author_email       = "rocky@gnu.org"
ftp_url            = None
install_requires   = ['coverage', 'pygments >= 1.4']
license            = 'GPL'
mailing_list       = None
modname            = 'pyficache'
py_modules = [modname]

short_desc = \
'Cache lines and information of files which are often Python programs'

# VERSION.py sets variable VERSION.
import os.path
execfile(os.path.join(os.path.dirname(__file__), 'VERSION.py'))

web = 'http://code.google.com/p/pyficache'

zip_safe = False # tracebacks in zip files are funky and not debuggable

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()
long_description   = ( read("README.txt") + '\n\n' +  read("NEWS") )
