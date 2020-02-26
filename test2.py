#!/usr/bin/env python
import os
import signal
import time
import sys
 
def receiveSignal(signum, frame):
	if(p==0):
		print("child recieved", signum)
		sys.exit(0)
	else:
		print("still fucked up")

def func():
	p = os.fork()
	signal.signal(2,receiveSignal)
	print("beginning prorgram",p)
	if(p==0):
		print("child PID is:", os.getpid())
		while True:
			print("..")
			time.sleep(1)
	else:
		print("parent PID is:", os.getpid())
		os.wait()
		while True:
			print("//")
			time.sleep(1)

while True:
	func()