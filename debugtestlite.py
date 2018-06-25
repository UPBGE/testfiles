import sys
import os
from sh import find, Command, rm

if len(sys.argv) == 1:
	print("1: program")
	print("2: directory/file")
	print("3: no sensor time")
	print("4: sensor time")
	sys.exit(0)

cwd = os.getcwd()
dir = cwd + "/" + sys.argv[2]

files = sorted(list(find(dir, "-type", "f", "-name", "*.blend")))

def msg(*args):
	print(*args, end="")

lastfilename = cwd + "/lasttestfile.txt"

nosensortime = sys.argv[3]
sensortime = sys.argv[4]

if os.path.isfile(lastfilename):
	with open(lastfilename, "r") as lasttestfile:
		lastfile = lasttestfile.read()
		if lastfile in files:
			index = files.index(lastfile)
			continuefile = input("Continue from file name: %s, index: %s ? (y/n) " % (lastfile[0:-1], index))
			if continuefile == "y":
				files = files[index:]
		else:
			print("Cannot found last file: %s" % lastfile[0:1])

filefailed = []

def exit(filename):
	with open(lastfilename, "w") as lasttestfile:
		lasttestfile.write(filename)
	sys.exit(-1);

for i, file in enumerate(files):
	try:
		print("[{}/{}] Run file: {}".format(i, len(files), file))
		cmd = Command(sys.argv[1])
		if "--no-p" in sys.argv:
			cmd(file[:-1], _err=msg, _out=msg)
		else:
			cmd("-p", cwd + "/PythonMain/UserTestMain.py", file[:-1], "-", nosensortime, sensortime, _err=msg, _out=msg)
	except KeyboardInterrupt:
		print("Interrupt at file: %s" % file)
		exit(file)
	except:
		print("Failed run file: %s" % file)
		filefailed.append(file)
		if not "--report" in sys.argv:
			exit(file);

print("Failed files:")
for file in filefailed:
	print("\t", file)

