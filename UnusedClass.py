#!usr/bin/python
## -*- coding: UTF-8 -*-
#
#
#

import os
import sys


def findAllClass(file):

	result = False

	returnResult = []
	
	for line in file.readlines():
		
		if line.find("architecture armv7") != -1:
			result = True
			continue
		if result:
			contents = line.split('	')
			addressArray = []
			if len(contents) > 1:
				addressArray.extend(contents[1].split(' '))
			for address in addressArray:
				if address == '00000001':
					continue
				if address != '\n':
					returnResult.append(address)
				
	return returnResult

def findUsedClass(file):
	
	result = False

	returnResult = []
	
	for line in file.readlines():
		
		if line.find("architecture armv7") != -1:
			result = True
			continue
		if result:
			contents = line.split('	')
			addressArray = []
			if len(contents) > 1:
				addressArray.extend(contents[1].split(' '))
			for address in addressArray:
				if address == '00000001':
					continue
				if address == '00000000':
					continue
				if address != '\n':
					returnResult.append(address)
				
	return returnResult


def findClassNameByAddress(addressArray,file):

	# file = open(addressMap,'r')

	for address in addressArray:
		file.seek(0)
		find  = False
		for line in file.readlines():
			if line.find(address) != -1:
				find = True
				continue
			if find and line.find("name") != -1:
				lineArray = line.split(' ')
				if len(lineArray) > 0:
					name = lineArray[len(lineArray) - 1].replace('\n','')
					print "%s %s" %(address,name)
				break


def checkAppBinary(argv):
	if len(argv) < 2:
		print '输入有效地址'
		return False

	path = argv[1]

	if not os.path.isfile(path):
		print '文件不存在'
		return False
	return True

def readAllClass(path):
	file = os.popen('otool -v -s __DATA	__objc_classlist %s' % (path))

	return file

def readUsedClass(path):
	file = os.popen('otool -v -s __DATA	__objc_classrefs %s' % (path))
	return file

def readClassName(path):
	file = os.popen('otool -o %s' % (path))

	content = file.read()
	file.close()

	fo = open('map.txt', "w")
	fo.write(content)
	fo.close()

	return open(os.path.abspath('map.txt'))


if __name__ == '__main__':

	if checkAppBinary(sys.argv):
		path = sys.argv[1]

		allClassFile = readAllClass(path)
		allClass = findAllClass(allClassFile)

		print 'All class size:%d' % (len(allClass))

		usedClassFile = readUsedClass(path)
		usedClass = findAllClass(usedClassFile)

		print 'Used class size:%d' % (len(usedClass))

		unUsedClass = list(set(allClass).difference(set(usedClass)))

		if len(unUsedClass) > 0:
			classNameFile = readClassName(path)
			findClassNameByAddress(unUsedClass,classNameFile)

	#Clean map file
	mapPath = os.path.abspath('map.txt')
	if os.path.isfile(mapPath):
		os.remove(mapPath)


