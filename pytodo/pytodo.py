#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------
# pytodo 0.1
# ----------------------------------------------
# Generates a TODO file from python scripts.
# type python pytodo --help for help instructions
# more info:
# http://github.com/beshrkayali/pytodo
# -----------------------------------------------
# Copyright (C) 2009 Beshr Kayali <beshrkayali@gmail.com>
# http://beshrkayali.com
# latest version of pytodo is available on:
# http://github.com/beshrkayali/pytodo

import sys, os

# templates
final_todo = []
project_name = ""
extra_header = ""
extra_footer = ""

settings_template = """# pytodo settings file
# project name
project_name = ""

# Extra Header
extra_header = "TODO for version x.x"

# Extra Footer
extra_footer = ""


# add scripts that you want pytodo to process.
scripts = (#'script1',
       	   #'script2',
       	   #'path/to/script3',
       	   #'',
	   	   )"""


def parse(script_file):
	# open script file
	script = open(script_file).readlines()
	
	line_number = 0
	for line in script:
		line_number += 1
		if (line.strip().upper()[0:7] == '# TODO:'):
			final_todo.append((line.strip()[8:],script_file, line_number))

def create_todo():
	try:
		# import the settings file, if it exists
		import pytodo_settings
		# get the list of scripts to process
		# TODO: implement a way to deal with directories in scripts_list.
		scripts_list = getattr(pytodo_settings, 'scripts')
	# pytodo_settings.py not found
	except ImportError:
		print "pytodo_settings.py not found, please run [pytodo --init] first"
		sys.exit()		
	# scripts_tuple not found
	except AttributeError:
		print "scripts tuple not found in your pytodo_settings.py file, please create it and include all scripts that pytodo should process."
		sys.exit()
		
	# get project name from settings [if existed]
	try:
		project_name = getattr(pytodo_settings, 'project_name')
	except AttributeError:
		print "Project name not detected, using [unnamed]"
		project_name = "unnamed"
	
	# get extra_header from settings [if existed]
	try:
		extra_header = getattr(pytodo_settings, 'extra_header')
	except AttributeError:
		extra_header = ""
	
	# get extra_footer from settings [if existed]
	try:
		extra_footer = getattr(pytodo_settings, 'extra_footer')
	except AttributeError:
		extra_footer = ""
	

	# process scripts
	for script in scripts_list:
		print "Processing %s" % script
		if not os.path.isfile(script):
			# if it's not found print a message and continue to the next one
			print "Error: script \"%s\" not found" % script
			continue

		# parse script
		parse(script)
	
	# finally, generate TODO file
	answered = False
	if os.path.isfile('TODO'):
		while not answered:
			answer = raw_input("TODO already exists, overwrite? (yes/no): ")
			if not(answer == 'no' or answer == 'yes'):
				print "Please enter either \"yes\" or \"no\""
				continue
			if answer == 'no':
				print "Aborting..."
				sys.exit()
			if answer == 'yes':
				break
	
	# creating TODO file
	todo_file = open('TODO', 'w')
	
	todo_file.write ("TODO for %s\n" % project_name)
	todo_file.write ("==================================\n")
	
	if extra_header:
		todo_file.write("%s\n\n" % extra_header)
	
	for todo in final_todo:
		todo_file.write(" - %s - [script: %s, line: %s]\n" % (todo[0],todo[1], todo[2]))
	
	if extra_footer:
		todo_file.write("\n%s\n\n" % extra_footer)
	
	print "Finished... "
	todo_file.close()
	
def initialize_settings():
	if os.path.isfile('pytodo_settings.py'):
		print "pytodo_settings already exists!"
		sys.exit()
		
	settings_file = open('pytodo_settings.py', 'w')
	settings_file.write(settings_template)
	settings_file.close()
	print "pytodo_settings.py created..."
	
def usage():
	print """Usage: pytodo [command]
       commands:
       ==========	
       -h, --help: view this screen.
       -g, --generate: create TODO file.
       -i, --init: initialize a pytodo_settings.py file [if it doesn't exist]"""

def main():
	# check command line args
	if not len(sys.argv) == 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
		usage()
		sys.exit()
	if not len(sys.argv) == 2 or sys.argv[1] == '-g' or sys.argv[1] == '--generate':
		create_todo()
		sys.exit()
	if not len(sys.argv) == 2 or sys.argv[1] == '-i' or sys.argv[1] == '--init':
		initialize_settings()
		sys.exit()
	
	# TODO: add a command to render TODO as a webpage
	
	# not a command
	print "%s: invalid command" % sys.argv[1]
	usage()
	

# run if not imported
if __name__ == "__main__":
	main()

