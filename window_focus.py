#!/usr/bin/python

# Source code from
# http://stackoverflow.com/questions/3983946/get-active-window-title-in-x

from subprocess import Popen, PIPE
from time import sleep, time, strftime, localtime, timezone
from random import uniform
from collections import defaultdict

import re, operator, sys

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
xss_info = xss.XScreenSaverAllocInfo()


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

def is_productive(program_class):
    '''
    Check if this program is in the list of productive programs.
    '''
    productive = ['terminal', 'texmaker', 'freemind', 'evince', 'inkscape']

    for p in productive:
        if program_class.find(p) >= 0:
            return True

    return False

try:
    ct_file = open('saved/been_run.csv', 'r+')
except IOError as e:
    ct_file = open('saved/been_run.csv', 'w+')

ct_file.seek(0, 2)



class TimeTracker:
    def __init__(self):
        self.productive = 0
        self.unproductive = 0
        self.prev_class_and_title = ('','')
        self.prev_idle_time = time()
        self.prev_tell = ct_file.tell()
        self.prev_start_time = time()
        self.prev_time = time()
        self.start_time = time()

    def add_increment(self, class_and_title, prev_time, time_incr, idle):
        if not idle and class_and_title != ('',''):
            if self.prev_class_and_title == class_and_title:
                ct_file.seek(self.prev_tell)
                ct_file.write("%f %f %s\n" % ( self.prev_start_time, time(), " ".join(class_and_title)))
            else:
                self.prev_start_time = prev_time
                self.prev_class_and_title = class_and_title
                self.prev_tell = ct_file.tell()
                ct_file.write("%f %f %s\n" % ( self.prev_start_time, time(), " ".join(class_and_title)))
                ct_file.flush()

            by_class_title[class_and_title] += time_incr
            by_title[class_and_title[1]] += time_incr
            by_class[class_and_title[0]] += time_incr

            if is_productive(class_and_title[0]):
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
            print "%.3f %s %s" % ( self.productive / self.total_time, strftime("%H:%M:%S", localtime(self.productive + timezone)) , "productive")
            print "%.3f %s %s" % ( self.unproductive / self.total_time, strftime("%H:%M:%S", localtime(self.unproductive + timezone)) , "unproductive")
        else:
            print "%.3f %s %s" % ( self.unproductive / self.total_time, strftime("%H:%M:%S", localtime(self.unproductive + timezone)) , "unproductive")
            print "%.3f %s %s" % ( self.productive / self.total_time, strftime("%H:%M:%S", localtime(self.productive + timezone)) , "productive")

        print
        print '---------------------------------------------------------'

        for i in xrange(min(20, len(most))):
            #print "%.3f %6.1f %s" % ( most[i][1] / self.total_time, most[i][1] , most[i][0])
            print "%.3f %s %s" % ( most[i][1] / self.total_time, strftime("%H:%M:%S", localtime(most[i][1] + timezone)) , most[i][0])

        print
        print
        print "Idle time: %s Active time: %s Total time: %s is_idle: %s" % ( strftime("%H:%M:%S", localtime(xss_info.contents.idle / 1000. + timezone)), strftime("%H:%M:%S", localtime(time() - self.prev_idle_time + timezone)), strftime("%H:%M:%S", localtime(time() - self.start_time + timezone)),  idle )
        print '---------------------------------------------------------'

        for i in xrange(min(20, len(most1))):
            #print "%.3f %6.1f %s" % ( most[i][1] / self.total_time, most[i][1] , most[i][0])
            print "%.3f %s %s" % ( most1[i][1] / self.total_time, strftime("%H:%M:%S", localtime(most1[i][1] + timezone)) , most1[i][0])


        self.prev_time = time()

        sys.stdout.flush()

    def run(self):
        self.total_time = 0
        while(True):
            class_and_title = get_active_window_title()

            time_incr = time() - self.prev_time
            self.total_time += time_incr

            xss.XScreenSaverQueryInfo( dpy, root, xss_info)
            #print "Idle time in milliseconds: %d" % ( xss_info.contents.idle, )
            idle = False


            if xss_info.contents.idle > (3. * 60. * 1000.):
                idle = True
                class_and_title=('','')
                self.prev_class_and_title=('','')

            tt.add_increment(class_and_title, self.prev_time, time_incr, idle)

            sleep(1.)


tt = TimeTracker()
tt.run()
