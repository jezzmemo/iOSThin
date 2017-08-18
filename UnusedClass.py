#!usr/bin/python
## -*- coding: UTF-8 -*-
#
#
#



def findAllClass(classFile):

	file = open(classFile)
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

def findUsedClass(usedClassFile):
	
	file = open(usedClassFile)
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


def findClassNameByAddress(addressArray,addressMap):

	file = open(addressMap,'r')

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



if __name__ == '__main__':


  #otool -s -v __DATA	__objc_classlist xxx.app/xxx > allClass.txt
	allClass = findAllClass('allClass.txt')

	print 'All class size:%d' % (len(allClass))

  #otool -s -v __DATA	__objc_classrefs xxx.app/xxx > usedClass.txt
	usedClass = findUsedClass('usedClass.txt')

	print 'Used class size:%d' % (len(usedClass))

	unUsedClass = list(set(allClass).difference(set(usedClass)))

	print 'UnUsed class size:%d' % (len(unUsedClass))

	if len(unUsedClass) > 0
    #otool -o xxx.app/xxx > map.txt
		findClassNameByAddress(unUsedClass,'map.txt')


