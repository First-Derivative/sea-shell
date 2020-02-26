#!/usr/bin/env python

import sys
import time

# ECS518U
# Lab 5 zzz
# Have a nap

# The snooze time in secs, or forever if no argument is supplied
if len(sys.argv) > 1:
	num_sec = int(sys.argv[1])
	inc = 1
else:
	num_sec = 1
	inc = 0

if num_sec % 2:
	returnCode = 1
else:
	returnCode = 0

count = 0
# print 'num_sec, inc, count'
while count < num_sec:
	# print 'num_sec, inc, count'
	print("z ")
	count += inc

    # wait for a second
	time.sleep(1)

print("\n")
sys.exit(returnCode)
