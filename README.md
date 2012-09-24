bidoin
======

Monitor what's in focus right now. Bidoin wakes up every second and records the name and type of the program in focus at that moment. It then stores this information and displays the statistics in a top-like format.

Usage:

./bidoin.py

Or...

python bidoin.py

The statistics are stored in a file in 'beenrun.csv'. A daily summary of the statistics can be created by running the summarize.py. Programs are classified into productive and unproductive classes according to their type and name. A program is considered unproductive by default. To be classified as productive, an entry needs to be made in the appropriate list in productive.py. For example, if one were working on a paper about cheese, the terms 'gruyere' and 'emmentaler' may indicate that the work being done in productive.

By default, bidoin assumes that you should spend about 75% of your time working. To this end, it shows how much free time is available. If the amount of unproductive work exceeds 25% of the total time recorded, then the time needed to bring it up to 25% is shown as 'Time to make up.'

The 'Active time' indicates how long the computer has been continuously active (i.e. not idle). The 'Total Active Time' is the total time active for the current day and the 'Total Time' is the difference between the time now and the time of the first activity for the day.

