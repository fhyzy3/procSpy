#!/usr/bin/env python3

import mysql.connector
import argparse
import sys
from os import path
from collections import namedtuple


MODE_FILE = 'file'
MODE_DB = 'db'

DB_CFG_FILE = './procSpyDb.cfg'
PROCSPY_FILE_INIT = "PROCSPY_FILE_HEADER"

PROCESS = namedtuple('PROCESS', 'pid ppid uid user cmdline starttime endtime')
PROC_DEAD = "DEADPROC"

C_RESET = '\033[0m'
C_RED = '\033[1;31m'
C_GREEN = '\033[1;32m'
C_GRAY = '\033[1;37m'
GREEN_PLUS = f"{C_GREEN}[+]{C_RESET}"
RED_MINUS = f"{C_RED}[-]{C_RESET}"


def parseFile(filename):

	procs = []

	with open(filename, 'r') as f:
		lineList = f.readlines()	

	deadProcs = []
	for line in lineList:
		
		if PROC_DEAD in line:
			deadProcs.append(line.split(":::"))


	for line in lineList:
		
		if PROC_DEAD not in line:

			lineData = line.split(":::")
			starttime = lineData[0].strip()
			pid = int(lineData[1].strip())
			ppid = int(lineData[2].strip())
			uid = int(lineData[3].strip())
			user = lineData[4].strip()
			cmd = lineData[5].strip()

			for i in deadProcs:
				if int(i[1]) == pid:
					endtime = i[0]

			procs.append(PROCESS(pid=pid, ppid=ppid, uid=uid, user=user, cmdline=cmd, starttime=starttime, endtime=endtime))


	return procs


def checkHeader(filename):

	with open(filename, 'r') as f:
		firstline = firstline.readline().strip()


	return firstline == PROC_SPY_FILE_INIT



def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('--mode', nargs='?', help='Specifies the mode to parse data from')
	parser.add_argument('-a', action='store_true', help='Displays the entire command history')
	parser.add_argument('-i', action='store_true', help='Enter interactive mode.')
	parser.add_argument('-s', nargs='?', help='Source file for file mode.')


	args = parser.parse_args()
	modeArg = args.mode
	mode = ""
	
	if modeArg == MODE_FILE:

		if not args.s:
			print(f"{RED_MINUS} No source file specified. Please specify a source file with '-s'")
			sys.exit(1)

		elif args.s:
			fileExists = path.isfile(args.s)
			if not fileExists:
				print(f"{RED_MINUS} Specified file could not be located. Please specify a valid procSpy file.")
				sys.exit(1)

		#	if not checkHeader(args.s):
		#		print(f"{RED_MINUS} The specified file doesn't appear to be a procSpy file.")
		#		sys.exit(1)

		
			
			procList = parseFile(args.s)
			processFilters(procList, args)
				


	elif modeArg == MODE_DB:
		mode = modeArg

	else:
		print(f"{RED_MINUS} Invalid Mode Specified. Please state 'file' or 'db'")
		sys.exit(1)


		
	
	
	



main()		
