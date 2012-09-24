#!/usr/bin/python

# Source code from
# http://stackoverflow.com/questions/3983946/get-active-window-title-in-x

from subprocess import Popen, PIPE
from time import sleep, time, strftime, localtime, timezone
from random import uniform
from collections import defaultdict
from datetime import date
from productive import is_productive

import re, operator, sys
import shlex

import ctypes
import os

class XScreenSaverInfo( ctypes.Structure):
  """ typedef struct { ... } XScreenSaverInfo; """
  _fields_ = [('window',      ctypes.c_ulong), # screen saver window
              ('state',       ctypes.c_int),   # off,on,disabled
              ('kind',        ctypes.c_int),   # blanked,internal,external
              ('since',       ctypes.c_ulong), # milliseconds
              ('idle',        ctypes.c_ulong), # milliseconds
              ('event_mask',  ctypes.c_ulong)] # events

xlib = ctypes.cdll.LoadLibrary( 'libX11.so')
dpy = xlib.XOpenDisplay( os.environ['DISPLAY'])
root = xlib.XDefaultRootWindow( dpy)
xss = ctypes.cdll.LoadLibrary( 'libXss.so')
xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)


def get_active_window_title():
    root_check = ''
    root = Popen(['xprop', '-root'],  stdout=PIPE)

    win_title = ''
    win_class = ''

    if root.stdout != root_check:
        root_check = root.stdout

        for i in root.stdout:
            if '_NET_ACTIVE_WINDOW(WINDOW):' in i:
                id_ = i.split()[4]
                id_w = Popen(['xprop', '-id', id_], stdout=PIPE)
        id_w.wait()
        buff = []
        for j in id_w.stdout:
            buff.append(j)

        for line in buff:
            #print "line:", line
            match = re.match("WM_NAME\((?P<type>.+)\) = (?P<name>.+)", line)
            match1 = re.match("WM_CLASS\((?P<type>.+)\) = (?P<name>.+)", line)

            if match1 != None:
                type = match1.group("type")
                if type == "STRING" or type == "COMPOUND_TEXT":
                    win_class = match1.group("name").split(',')[1].strip(" ").lower()

            if match != None:
                type = match.group("type")
                if type == "STRING" or type == "COMPOUND_TEXT":
                    win_title = match.group("name").strip(" ")

    if win_title == '' and win_class == '':
        return ("Active window not found", '')
    else:
        return (win_class, win_title)

by_class_title=defaultdict(float)
by_class=defaultdict(float)
by_title=defaultdict(float)


def is_ignored(program_class, program_name):
    #ignored_name = ['Duolingo']
    ignored_name = []

    for n in ignored_name:
        if program_name.lower().find(n.lower()) >= 0:
            return True

    return False


class TimeTracker:
    def __init__(self):
        self.productive = 0
        self.unproductive = 0
        self.prev_class_and_title = ('','')
        self.prev_idle_time = time()
        self.prev_start_time = time()
        self.prev_time = time()
        self.start_time = time()
        self.total_time = 0.
        self.xss_info = xss.XScreenSaverAllocInfo()

        try:
            self.ct_file = open('saved/been_run.csv', 'r+')
        except IOError as e:
            self.ct_file = open('saved/been_run.csv', 'w+')


    def add_increment(self, class_and_title, prev_time, time_incr, idle, write=False):
        if not idle and class_and_title != ('',''):
            self.total_time += time_incr

            if write:
                # we don't want to save entries that have been read before
                if self.prev_class_and_title == class_and_title:
                    self.ct_file.seek(self.prev_tell)
                    self.ct_file.write("%f %f %s\n" % ( self.prev_start_time, time(), " ".join(class_and_title)))
                else:
                    self.prev_start_time = prev_time
                    self.prev_class_and_title = class_and_title
                    self.prev_tell = self.ct_file.tell()
                    self.ct_file.write("%f %f %s\n" % ( self.prev_start_time, time(), " ".join(class_and_title)))
                    self.ct_file.flush()

            class_and_title = (class_and_title[0].strip('"'), class_and_title[1].strip('"'))

            by_class_title[class_and_title] += time_incr
            by_title[class_and_title[1]] += time_incr
            by_class[class_and_title[0]] += time_incr

            if not is_ignored(class_and_title[0], class_and_title[1]):
                if is_productive(class_and_title[0], class_and_title[1]):
                    self.productive += time_incr
                else:
                    self.unproductive += time_incr
        else:
            self.prev_idle_time = time()

        #most = sorted(by_class_title.iteritems(), key=operator.itemgetter(1), reverse=True)
        most = sorted(by_class.iteritems(), key=operator.itemgetter(1), reverse=True)
        most1 = sorted(by_class_title.iteritems(), key=operator.itemgetter(1), reverse=True)

        print chr(27) + "[2J" + chr(27) + "[;H"

        '''
        print "xss_info.window:", xss_info.contents.window
        print "xss_info.state:", xss_info.contents.state
        print "xss_info.kind:", xss_info.contents.kind
        print "xss_info.since:", xss_info.contents.since
        print "xss_info.idle:", xss_info.contents.idle
        '''

        if self.productive > self.unproductive:
            print "%.3f %s %s" % ( self.productive / (self.productive + self.unproductive), strftime("%H:%M:%S", localtime(self.productive + timezone)) , "productive")
            print "%.3f %s %s" % ( self.unproductive / (self.productive + self.unproductive), strftime("%H:%M:%S", localtime(self.unproductive + timezone)) , "unproductive")
        else:
            print "%.3f %s %s" % ( self.unproductive / self.total_time, strftime("%H:%M:%S", localtime(self.unproductive + timezone)) , "unproductive")
            print "%.3f %s %s" % ( self.productive / self.total_time, strftime("%H:%M:%S", localtime(self.productive + timezone)) , "productive")

        print

        '''

        if self.unproductive < 0.25 * self.total_time:
            print "Free time: %s" % ( strftime("%H:%M:%S", localtime(0.25 * self.total_time - self.unproductive + timezone)))
        '''
        if self.unproductive < (1/3.) * self.productive:
            print "Free time: %s" % ( strftime("%H:%M:%S", localtime((1/3.) * self.productive - self.unproductive + timezone)))
        else:
            print "Free time: 00:00:00 Time to make up: %s" % ( strftime("%H:%M:%S", localtime((self.unproductive * 3.) - self.productive + timezone)))

        print '---------------------------------------------------------'

        for i in xrange(min(10, len(most))):
            #print "%.3f %6.1f %s" % ( most[i][1] / self.total_time, most[i][1] , most[i][0])
            print "%.3f %s %s" % ( most[i][1] / self.total_time, strftime("%H:%M:%S", localtime(most[i][1] + timezone)) , most[i][0])

        print
        print
        print "Active time: %s Total active time: %s Total time: %s is_idle: %s" % ( strftime("%H:%M:%S", localtime(time() - self.prev_idle_time + timezone)), strftime("%H:%M:%S", localtime(self.total_time + timezone)), strftime("%H:%M:%S", localtime(time() - self.start_time + timezone)),  idle )
        print '---------------------------------------------------------'

        for i in xrange(min(10, len(most1))):
            #print "%.3f %6.1f %s" % ( most[i][1] / self.total_time, most[i][1] , most[i][0])
            print "%.3f %s %s" % ( most1[i][1] / self.total_time, strftime("%H:%M:%S", localtime(most1[i][1] + timezone)) , most1[i][0])


        self.prev_time = time()

        sys.stdout.flush()

    def run(self):
        self.ct_file.seek(0, 2)
        self.prev_tell = self.ct_file.tell()

        while(True):
            class_and_title = get_active_window_title()

            time_incr = time() - self.prev_time

            xss.XScreenSaverQueryInfo( dpy, root, self.xss_info)
            #print "Idle time in milliseconds: %d" % ( xss_info.contents.idle, )
            idle = False


            if self.xss_info.contents.idle > (2. * 60. * 1000.):
                idle = True
                class_and_title=('','')
                self.prev_class_and_title=('','')

            self.add_increment(class_and_title, self.prev_time, time_incr, idle, write=True)

            sleep(1.)

    def is_today(self, t):
        '''
        Is a particular time t, today?
        '''
        today = date.today()
        lt = localtime(t + timezone)

        if lt.tm_mday == today.day and lt.tm_mon == today.month and lt.tm_year == today.year:
            return True

        return False

    def load_previous_data(self, today=True):
        self.ct_file.seek(0)

        lines = self.ct_file.readlines()
        for line in reversed(lines):
            try: 
                parts = shlex.split(line)
            except ValueError:
                continue

            prev_time = float(parts[0])
            time_incr = float(parts[1]) - prev_time

            if not self.is_today(prev_time):
                continue

            if len(parts) == 3:
                class_and_title = (parts[2], '')
            elif len(parts) == 2:
                class_and_title = ('', '')
            else:
                class_and_title = (parts[2], parts[3])

            self.add_increment(class_and_title, prev_time, time_incr, False, write=False)
            self.start_time = prev_time

tt = TimeTracker()
tt.load_previous_data()
tt.run()
