#!/usr/bin/env python

import gzip
import os
import random

#def Link():
#	

def Extract(data, start, end):
#	print start, end
#	tmp_file = result_dir + "tmp." + str(random.randrange(1000000, 9999999))
	tmp_file = "tmp." + str(random.randrange(1000000, 9999999))
	tmp_file_gz = tmp_file + ".gz"
#	print tmp_file
	tmp = open(tmp_file_gz, "wb")
	tmp.write(data[start:end])
	tmp.close()
	
	if data[start:start+3] == "\x1F\x8B\x08":
		gtmp = gzip.open(tmp_file_gz, "rb")
		data = gtmp.read()
		otmp = open(tmp_file, "wb")
		otmp.write(data)

		gtmp.close()
		otmp.close()

		os.remove(tmp_file_gz)
		error = False
	else:
#		error = True
		error = False
		tmp_file = tmp_file_gz
	
#	os.remove(tmp_file_gz)
	return error, tmp_file

def MakeFile(tfile, path):
	f = open(tfile, "rb")
	fdata = f.read()
	file_name = ""
	file_dummy = ""
	file_data = ""
	i = 0
	while True:
		try:
			if fdata[i] != "\x00":
				file_name += fdata[i]
				i += 1
			else:
				break
		except IndexError:
			return None

#	print file_name
	i += 1
	while True:
		try:
			if fdata[i] != "\x00":
				file_dummy += fdata[i]
				i += 1
			else:
				break
		except IndexError:
			return None

	i += 10

	while True:
		try:
			file_data += fdata[i]
			i += 1
		except IndexError:
			f.close()

			directory = path + "/" + os.path.dirname(file_name)
			filename = os.path.basename(file_name)
			if not os.path.exists(directory):
				os.makedirs(directory)

			if file_dummy == "\xFF\xA1":
#				Link
#				print file_data[len(file_data) - 1].encode('hex')
				if file_data[len(file_data) - 1] == "\x00":
#					os.system("ln -s " + path + "/" + filename + " " + file_data[:len(file_data) - 2])
					os.system("ln -s " + file_data[:len(file_data) - 1] + " " + path + "/" + file_name)
#					os.symlink(filename, file_data[:len(file_data) - 2])
#					file_data.strip('\x00')
#					file_data.replace("\x00", "")
#				print file_data[len(file_data) - 2].encode('hex')
				else:
					os.system("ln -s " + file_data + " " + path + "/" + file_name)
#					os.symlink(filename, file_data)

				os.remove(tfile)
				return None

			elif file_dummy == "\xED\x41":
#				Directory
				os.makedirs(path + "/" + file_name)
#				print file_data.encode('hex')
				os.remove(tfile)
				return None

#			f = open(directory + "/" + filename + "_" + file_dummy.encode('hex'), "wb")
			f = open(directory + "/" + filename, "wb")
#			print directory + "/" + filename
			f.write(file_data)
			f.close()
			os.remove(tfile)
			return None

