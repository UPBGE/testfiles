import sys
import os
from sh import valgrind, mkdir, find, kate

def debug(blendfile):
	dir = os.getcwd()

	logfile = dir + "/Valgrind/Logs/" + blendfile.split("/TestFiles")[0].replace(".blend", ".log")
	logdir = logfile.rsplit("/", maxsplit=1)

	mkdir("-p", logdir)

	pythonmainfile = dir + "/PythonMain/loopmain.py"

	suppfile = dir + "/suppressions.supp"
	program = "upbgedbplayer"

	print("* Debugging upbge")
	print("* Test file:", blendfile)
	print("* Log file:", logfile)

	print(">>> Start valgrind")

	options = []

	if not "--no-log" in sys.argv:
		options.append("--log-file=" + logfile)
	if not "--no-leak-check" in sys.argv:
		options.append("--leak-check=full")
	if not "--no-suppressions" in sys.argv:
		options.append("--suppressions=" + suppfile)
	if "--gdb" in sys.argv:
		options.append("--vgdb=yes")
		options.append("--vgdb-error=0")

	options.append(program)

	if not "--no-python-main" in sys.argv:
		options.append("-p")
		options.append(pythonmainfile)

	options.append(blendfile)
	command = "valgrind"

	print("* command:", command)
	print("* options:", options)

	try:
		valgrind(options)
	except:
		print("* failed run debugger")

	return logfile


blenddir = sys.argv[1]

files = list(find(blenddir, "-type", "f", "-name", "*.blend"))

print("* Files to inspect:")
for file in files:
	print("  - ", file[:-1])

loglist = []
for file in files:
	logfile = debug(file[:-1])
	loglist.append(logfile)

#if "--no-log" not in sys.argv:
#	kate(loglist)
