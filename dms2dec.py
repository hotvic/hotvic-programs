# -*- coding: UTF-8 -*-
#
# Copyright © 2013 Victor Aurélio <victoraur.santos@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, getopt, re

sopts="hc:"
lopts="help google-coordinates=".split()

opts, args = getopt.getopt(sys.argv[1:], sopts, lopts)

coo = False
hel = """\
Usage: dms2dec [options]
Options:
  -c|--google-coordinates          Set coordinates, if isn't set script will ask"""

for o, v in opts:
    if o in ["-c", "--google-coordinates"]:
        coo = v
    elif o in ["-h", "--help"]:
        print hel
        exit(-1)

if not coo:
    coo = raw_input('Please Enter G. Earth Coordinates(WGS84, i.e: 6°58\'34.96"S, 35°47\'59.60"O)=> ')

exp = re.compile("(\d+)°(\d+)'([0-9.]+)\\\"(.)")
ll = [exp.search(coo.split(",")[0]),
      exp.search(coo.split(",")[1])]

lad = float(ll[0].group(1))
lam = float(ll[0].group(2))
las = float(ll[0].group(3))
lap = ll[0].group(4)
lod = float(ll[1].group(1))
lom = float(ll[1].group(2))
los = float(ll[1].group(3))
lop = ll[1].group(4)


ladec = ((lam * 60.0) + las) / (60.0 * 60.0)
lodec = ((lom * 60.0) + los) / (60.0 + 60.0)

latitude = lad + ladec
longitude = lod + lodec

if lap == "S":
    latitude *= -1

if lop == "O":
    longitude *= -1

print "Decimal Degress: ({0}, {1})".format(latitude, longitude)
print "  Latitude:", latitude
print "  Longitude:", longitude

print "\nOriginal (WGS84, DMS): ({0}, {1})".format(ll[0].group(0), ll[1].group(0))
print "  Degress lat: {0} lon: {1}".format(lad, lod)
print "  Minutes lat: {0} lon: {1}".format(lam, lom)
print "  Seconds lat: {0} lon: {1}".format(las, los)
print "  Direction lat: {0} lon: {1}".format(lap, lop)
