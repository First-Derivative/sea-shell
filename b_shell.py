#! /usr/bin/env python3
import subprocess
import signal 
import os, sys
import shutil
from datetime import datetime
# Here the path is hardcoded, but you can easily optionally get your PATH environ variable
# by using: path = os.environ['PATH'] and then splitting based on ':' such as the_path = path.split(':')
#pp = os.environ['PATH'] #FULL PATH FOUND IN THIS STRING 
#print(pp)
THE_PATH = ["/bin/", "/usr/bin/", "/usr/local/bin/", "./"]


# ========================
#    Run command
#    Run an executable somewhere on the path
#    Any number of arguments
# ========================

def runCmd(fields,process):
	if(process==0):
		global PID, THE_PATH
		cmd = fields[0]
		cnt = 0
		args = []
		while cnt < len(fields):
			args.append(fields[cnt])
			cnt += 1
		execname = add_path(cmd, THE_PATH)
		#run the executable
		if not execname:
			print('Executable file ' + str(cmd) +' not found')
		else:
		# execute the command
			print(execname)
		# execv executes a new program, replacing the current process; on success, it does not return. 
		# On Unix, the new executable is loaded into  the current process, and will have the same process id as the caller.
		try:	
			os.execv(execname, args)
		except :
			print('Something went wrong there')
			os._exit(0)
	else:
		signal.signal(2,receiveSignal)
		os.wait()

def receiveSignal(signum, frame):
	if(process==0):
		print("child recieved", signum)
		sys.exit(0)
	else:
		print("error traceback call")
		return

# ========================
#    Constructs the full path used to run the external command
#    Checks to see if the file is executable
# ========================
def add_path(cmd, path):
	if cmd[0] not in ['/', '.']:
		for d in path:
			execname = d + cmd
			if(os.path.isfile(execname) and os.access(execname, os.X_OK)):
				return execname
		return False
	else:
		return cmd

def help_cmd():
	commands = {"info X:": "check if file/dir X exists", "files:": "displays all files in current directory", "delete X:": "deletes existing files named X", "copy X Y:": "copies an existing file X to a non-existing file Y", "where:":"print working directory", "down D:": "changes to directory D if it exists", "up:":"acesses directory one level closer to the root from currenty directory","finish:":"exists shell script" ,"help:": "you're reading it"}
	print("HELP PAGE 1 OF 1")
	print("=============================================================================")
	count = 1
	for entries in commands:
		print(str(count) + ".",entries, commands[entries])
		count += 1
	print("=============================================================================")


# ========================
#    files command
#    List file and directory names
#    No arguments
# ========================
def files_cmd(fields):
	if(checkArgs(fields, 0)):
		count = 1
		if(len(os.listdir('.')) == 0):
			print("The current directory is empty")
		for filename in os.listdir('.'):
			print(str(count)+".",filename)
			count += 1


# ========================
#  info command
#     List file information
#     1 argument: file name
# ========================
def info_cmd(fields):
	if(checkArgs(fields, 1)):
		filename = str(fields[1])
		if(os.path.exists(filename)):
			if(os.path.isfile(filename)):
				info_helper_printer(True, filename)
			else: 
				info_helper_printer(False, filename)
		else:
			print("File " + filename + " not found in current directory ")
	
# ========================
#  info command helpers
#  info printer - handles the formatting for the file description
# ========================
def info_helper_printer(isFile, filename):
	headers = ["Name", "Owner", "Type", "Modification Time"]  # column headers
	width = [20, 10, 10, 20]  # max width of data in each column
	details = os.stat(filename)
	time = details.st_mtime
	time = datetime.fromtimestamp(time).strftime('%b %d %Y %H:%M')
	info = []
	exe = False
	if(isFile):
		if(os.access(filename, os.X_OK)): exe = True;
		headers.append("Size")
		width.append(10)
		headers.append("Executable")
		width.append(10)
		info.append(filename)
		info.append(details.st_uid)
		info.append("File")
		info.append(time)
		info.append(details.st_size)
		info.append(str(exe))
		info_helper_printer_header(width, headers)
		info_helper_printer_table(width, info)
	else:
		info.append(filename)
		info.append(details.st_uid)
		info.append("Dir")
		info.append(time)
		info_helper_printer_header(width, headers)
		info_helper_printer_table(width, info)

# ========================
#  info command helpers
#  info printer header - prints header for info
# ========================
def info_helper_printer_header(width,headers):
	length = sum(width)
	field_num = 0
	output = ''
	print('-' * length)
	while field_num < len(headers):
		output += '{field:{fill}<{width}}'.format(field=headers[field_num], fill=' ', width=width[field_num])
		field_num += 1
	print(output)
	print('-' * length)
	
# ========================
#  info command helpers
#  info printer header - prints table body for info
# ========================
def info_helper_printer_table(width, info):
	fieldNum = 0
	output = ''
	while fieldNum < len(info):
		output += '{field:{fill}<{width}}'.format(field=info[fieldNum], fill=' ', width=width[fieldNum])
		fieldNum += 1
	print(output)

# ========================
#    copy X Y 
#    copies an existing file X to a non-existing file Y
#    2 arguments
# ========================
def copy_cmd(fields):
	if(checkArgs(fields, 2)):
		fileA = str(fields[1])
		fileB = str(fields[2])
		cond1 = os.path.isfile(fileA)
		cond2 = os.path.isfile(fileB)
		if(cond1 and not cond2):
			shutil.copyfile(fileA,fileB)
			if(os.path.isfile(fileB)):
				"copy successfull"
			else:
				"error copying"
		else:
			if(not cond1 and cond2): print("file " + fileA + " not found")
			if(cond2): print("file " + fileB + " already exists")

# ========================
#    delete
#    deletes existing files named X
#    1 arguments
# ========================
def delete_cmd(fields):
	if(checkArgs(fields, 1)):
		filename = fields[1]
		if(os.path.isfile(filename)):
			os.unlink(filename)
			if(not os.path.isfile(filename)):
				print("delete success")
				return
		print(filename + ": no such file")

# ========================
#    where command
#    prints current directory
#    No arguments
# ========================
def where_cmd(fields):
	if(checkArgs(fields, 0)):
		print(os.getcwd())

# ========================
#    down command
#    changes to directory D if it exists
#    1 argument 
# ========================
def down_cmd(fields):
	if(checkArgs(fields, 1)):
		newPath = str(fields[1])
		if(os.path.isdir(newPath)):
			os.chdir(newPath)
		else:
			print("specified directory path not found")

# ========================
#    up command
#    acesses directory one level closer to the root from currenty directory
#    1 argument 
# ========================
def up_cmd(fields):
	if(checkArgs(fields, 0)):
		if(os.getcwd() == "/"):
			print("At root level directory /")
		else:
			os.chdir('..')


# ========================
#    exit command
#    Exists program
# ========================
def exit_cmd(fields):
	print("Terminating program...")
	sys.exit(0)

# ----------------------
# Other functions
# ----------------------
def checkArgs(fields, num):
	numArgs = len(fields) - 1
	if numArgs == num:
		return True
	if numArgs > num:
		print("  Unexpected argument " + fields[num+1] + " for command " + fields[0])
	else:
		print("  Missing argument for command " + fields[0])
	return False

# ----------------------------------------------------------------------------------------------------------------------

while True:
	line = input("b_Shell>")  # NOTE! This is only for python 2. Should be 'input' for python 3
	fields = line.split()
	if(fields[0] == "files"):
		files_cmd(fields)
	elif(fields[0] == "where"):
		where_cmd(fields)
	elif(fields[0] == "down"):
		down_cmd(fields)
	elif(fields[0] == "up"):
		up_cmd(fields)
	elif(fields[0] == "finish"):
		exit_cmd(fields)
	elif(fields[0] == "copy"):
		copy_cmd(fields)
	elif(fields[0] == "delete"):
		delete_cmd(fields)
	elif(fields[0] == "info"):
		info_cmd(fields)
	elif(fields[0] == "help"):
		help_cmd()
	else:
		process = os.fork()
		runCmd(fields, process)