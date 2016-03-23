#!/usr/bin/env python

import struct
import sys
import os

index = 0
next_index = 0

def Init() :
	global bin, result, input_file
	argc = len(sys.argv)
	if argc < 2 :
		print "Usage: " + sys.argv[0] + " FILE [RESULT]"
		print "  FILE: PLF File"
		print "  RESULT: Make result directory"
		print "          default: plf"
		sys.exit()
	if argc >= 2 :
		try :
			input_file = open(sys.argv[1], "rb")
		except IOError :
			print "I/O error: file doesn't exist"; sys.exit()
	if argc >= 3 :
		result_dir = sys.argv[2]
	else :
		result_dir = "plf"

	if not os.path.exists(result_dir) :
		os.mkdir(result_dir)
	else :
		print "Directory does exist"
		sys.exit()

	result = open(result_dir + "/log.txt", "wb")
	bin = input_file.read()

def EndianConvert(number):
  return 0x1000000 * ord(number[3]) + 0x10000 * ord(number[2]) + 0x100 * ord(number[1]) + ord(number[0])
	
def sPLFFile(index):
	global file_size	
	result.writelines("====== PLF Header("+str(index)+") ======\n")
	result.writelines("dwMagic : "+ bin[index:index+4].encode("hex") + '\n');index+=4
	result.writelines("dwHdrVersion : "+ bin[index:index+4].encode("hex") + "\n");index+=4
	result.writelines("dwHeaderSize : "+ bin[index:index+4].encode("hex") + "\n");index+=4
	result.writelines("dwEntryHeaderSize : "+ bin[index:index+4].encode("hex") + "\n");index+=4
	result.writelines("uk_0x10 : "+ bin[index:index+4].encode("hex") + "\n");index+=4
	result.writelines("uk_0x14 : "+ bin[index:index+4].encode("hex") + "\n");index+=4
	result.writelines("uk_0x18 : "+ bin[index:index+4].encode("hex") + "\n");index+=4
	result.writelines("uk_0x1C : "+ bin[index:index+4].encode("hex") + "\n");index+=4
	result.writelines("uk_0x20 : "+ bin[index:index+4].encode("hex") + "\n");index+=4
	result.writelines("dwVersionMajor : "+ bin[index:index+4].encode("hex") + "\n");index+=4
	result.writelines("dwVersionMinor : "+ bin[index:index+4].encode("hex") + "\n");index+=4
	result.writelines("dwVersionBugfix : "+ bin[index:index+4].encode("hex") + "\n");index+=4
	result.writelines("uk_0x30 : "+ bin[index:index+4].encode("hex") + "\n");index+=4
	result.writelines("dwFileSize : "+ bin[index:index+4].encode("hex") + "\n\n")
	file_size=int(EndianConvert(bin[index:index+4]));index+=4
	return index
	
def sPLFEntryTag(index):
	result.writelines("====== PLFEntryTag("+str(index)+") ======\n")
	result.writelines("dwSectionType : "+ bin[index:index+4].encode("hex") + '\n');index+=4
	result.writelines("dwEntrySize : "+ bin[index:index+4].encode("hex") + '\n')
	next_index=int(EndianConvert(bin[index:index+4]));index+=4
	result.writelines("dwCRC32 : "+ bin[index:index+4].encode("hex") + '\n');index+=4
	result.writelines("uk_0x0C : "+ bin[index:index+4].encode("hex") + '\n');index+=4
	result.writelines("dwUncompressedSize : "+ bin[index:index+4].encode("hex") + '\n\n');index+=4
	index+=next_index
	return index
	

if __name__ == "__main__":
  Init()
  while(1):
  	if bin[index:index+4].encode("hex") == "504c4621":
  		index = sPLFFile(index)
  	elif bin[index:index+4].encode("hex") == "00000000" or "00000003" or "00000007" or "00000009" or "0000000b" or "0000000c":
  		if index%4 != 0 :
  			index+=4-(index%4)
  		index = sPLFEntryTag(index)
  		if file_size <= index:
  			break
  
  input_file.close()
  result.close()
  print " Result File store in " + sys.argv[1] + "/log.txt"

##
