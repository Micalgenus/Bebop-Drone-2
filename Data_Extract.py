#!/usr/bin/env python

import gzip
import os
import random

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
		error = True
	
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
#			f = open(directory + "/" + filename + "_" + file_dummy.encode('hex'), "wb")
			f = open(directory + "/" + filename, "wb")
			f.write(file_data)
			f.close()
			os.remove(tfile)
			return None

