#!/usr/bin/env python


import os
import time
os.chdir('..')
print("The current working directory is:", os.getcwd())
time.sleep(3)
p = os.fork()
if(p==0):
	print("child here with process id:", p)
	print("child executing command: 'ls'")
	os.system("ls")
else:
	time.sleep(5)
	print("parent executing command 'find *.py'")
	os.system("find *.py ")
#	os.wait() #if you toggle this line then you'll see the parent process being suspended and then the child process running
	print("parent here with process id:", p)
