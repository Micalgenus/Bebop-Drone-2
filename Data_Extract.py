#!/usr/bin/env python

import gzip
import os
import random

from PLF_Analyzer import result_dir as result_dir

def Extract(data, start, end):
#	print start, end
	tmp_file = result_dir + "tmp." + str(random.randrange(1000000, 9999999))
	tmp_file_gz = tmp_file + ".gz"
#	print tmp_file
	tmp = open(tmp_file_gz, "wb")
	tmp.write(data[start:end])
	tmp.close()
	
	try:
		gtmp = gzip.open(tmp_file_gz, "r")
	except IOError:
		os.remove(tmp_file_gz)
	data = gtmp.read()
	otmp = open(tmp_file, "wb")
	otmp.write(data)

	os.remove(tmp_file_gz)
