#!/usr/bin/python

import sys
from optparse import OptionParser
from productive import is_productive
from collections import defaultdict
import time
import shlex
import matplotlib.pyplot as plt
import numpy as np

def format_time(t):
    #print "t:", t
    t = int(t)
    hours = t / 3600
    t = t - hours * 3600

    #print "hours:", hours, "t1:", t
    minutes = t / 60

    #print "minutes:", minutes, "t2:", t
    t = t - minutes * 60
    seconds = t / 1

    return "%d:%02d:%02d" % (hours, minutes, seconds)

class TimeUsageData:
    def __init__(self):
        self.productive = 0.
        self.unproductive = 0.

class SumByDay:
    def __init__(self):
        self.days = defaultdict(TimeUsageData)

    def add_data(self, prev_time, next_time, class_and_title):
        lt = time.localtime(prev_time + time.timezone)

        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        index = (lt.tm_year, lt.tm_mon, lt.tm_mday, weekdays[lt.tm_wday])

        tud = self.days[index]

        if is_productive(class_and_title[0], class_and_title[1]):
            tud.productive += next_time - prev_time
        else:
            tud.unproductive += next_time - prev_time

    def summarize(self):
        vals = self.days.items()
        #print "self.days:", self.days
        #print "vals:", vals
        vals.sort()

        for v in vals:
            print v[0], format_time(v[1].productive), format_time(v[1].unproductive)

        print
        print "Total productive:", format_time(sum([v[1].productive for v in vals]))
        print "Total unproductive:", format_time(sum([v[1].unproductive for v in vals]))

class MinuteHistogram:
    def __init__(self):
        self.productive = defaultdict(int)
        self.unproductive = defaultdict(int)

    def add_data(self, prev_time, next_time, class_and_title):
        # Make a proverbial tick for every minute
        for i in range(int(prev_time), int(next_time), 1):
            lt = time.localtime(i + time.timezone)

            if is_productive(class_and_title[0], class_and_title[1]):
                self.productive[lt.tm_hour * 60 + lt.tm_min] += 1
            else:
                self.unproductive[lt.tm_hour * 60 + lt.tm_min] += 1

    def plot(self):
        #print "self.productive:", self.productive
        (minutes_prod, productive) = zip(*self.productive.items())
        (minutes_unprod, unproductive) = zip(*self.unproductive.items())
        print "minutes:", minutes_prod
        print "productive:", productive
        ax = plt.subplot(1,1,1)

        ax.plot(np.array(minutes_prod) / 60., productive, 'go')
        ax.plot(np.array(minutes_unprod) / 60., unproductive, 'ro')

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)
        plt.show()

def main():
    parser = OptionParser()

    #parser.add_option('-o', '--options', dest='some_option', default='yo', help="Place holder for a real option", type='str')
    parser.add_option('-l', '--lines', dest='lines', default=10000000, help="The number of lines to read from the data file.", type=int)
    parser.add_option('-p', '--plot', dest='plot', default=False, help="Plot the productive and unproductive times spent.", action='store_true')

    (options, args) = parser.parse_args()
    
    data_file = open('beenrun.csv', 'r')
    counter = 0

    sbd = SumByDay()
    mh = MinuteHistogram()
    lines = data_file.readlines()

    for line in reversed(lines):
        if counter >= options.lines:
            break

        counter += 1

        try:
            parts = shlex.split(line)
        except ValueError:
            continue

        prev_time = float(parts[0])
        next_time = float(parts[1])

        if len(parts) == 3:
            class_and_title = (parts[2], '')
        elif len(parts) == 2:
            class_and_title = ('', '')
        else:
            class_and_title = (parts[2], parts[3])

        sbd.add_data(prev_time, next_time, class_and_title)

        if options.plot:
            mh.add_data(prev_time, next_time, class_and_title)

    mh.plot()
    sbd.summarize()

if __name__ == '__main__':
    main()

