#!/usr/bin/env python2
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

import time
import urllib2
import argparse
from HTMLParser import HTMLParser
from gi.repository import Notify
from StringIO import StringIO

version = "%(prog)s 0.1"
defaults = {
    'URL':  'http://server.themanaworld.org/online.html'
}

aparser = argparse.ArgumentParser(description="Notify when users join in the server of The Mana Worl(default to server.themanaworld.org)")
# Add arguments
aparser.add_argument('--time', '-t', type=int, help='Time to update user list(default read from server)')
aparser.add_argument('--server', '-s', default='http://server.themanaworld.org', type=str, help='Server to  monitor')
aparser.add_argument('--version', '-v', action='version', version=version)

opts = aparser.parse_args()

class UserParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._users = []
        self._options = {}
        self._grabdata = False

    def handle_starttag(self, tag, attrs):
        istime = False
        if tag == "meta":
            for attr in attrs:
                if attr[0] == 'http-equiv':
                    istime = True
                elif attr[0] == "content" and istime:
                    self._options.update(time=attr[1])
        elif tag == "td":
            self._grabdata = True

    def handle_endtag(self, tag):
        if tag == "td":
            self._grabdata = False

    def handle_data(self, data):
        if self._grabdata:
            self._users.append(data)

    def feed(self, data):
        HTMLParser.feed(self, data)
        return [self._users, self._options]

Notify.init('TmwNotify')
def notify(user, new):
    if new:
        msg = Notify.Notification.new('TmwNotify', 'New user connected: ' + user, 'dialog-information')
        msg.show()
    else:
        msg = Notify.Notification.new('TmwNotify', 'User disconnected: ' + user, 'dialog-information')
        msg.show()

def parse_html():
    tmwserver = urllib2.urlopen(opts.server + '/online.html')
    html = tmwserver.read()
    parser = UserParser()
    return parser.feed(html)

oldlist = []

def do_loop(htime):
    global oldlist

    while (True):
        time.sleep(htime)
        result = parse_html()
        
        for user in result[0]:
            if not user in oldlist:
                notify(user, True)
        for user in oldlist:
            if not user in result[0]:
                notify(user, False)
        oldlist = result[0]

if opts.time == None:
    result = parse_html()
    htime = int(result[1]['time'])
    oldlist = result[0]
    do_loop(htime)
else:
    result = parse_html()
    oldlist = result[0]
    do_loop(opts.time)
