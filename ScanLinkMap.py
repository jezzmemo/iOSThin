#!usr/bin/python
## -*- coding: UTF-8 -*-
#
#使用简介：python linkmap.py XXX-LinkMap-normal-xxxarch.txt 或者 python linkmap.py XXX-LinkMap-normal-xxxarch.txt -g
#使用参数-g会统计每个模块.o的统计大小
#
__author__ = "zmjios"
__date__ = "2016-07-27"

import os
import re
import shutil
import sys

class SymbolModel:
    file = ""
    size = 0

def verify_linkmapfile(args):
    if len(sys.argv) < 2:
        print("请输入linkMap文件")
        return False

    path = args[1]

    if not os.path.isfile(path):
        print("请输入文件")
        return False

    file = open(path)
    content    = file.read()
    file.close()

    #查找是否存在# Object files:
    if content.find("# Object files:") == -1:
        print("输入linkmap文件非法")
        return False
    #查找是否存在# Sections:
    if content.find("# Sections:") == -1:
        print("输入linkmap文件非法")
        return False
    #查找是否存在# Symbols:
    if content.find("# Symbols:") == -1:
        print("输入linkmap文件非法")
        return False

    return True 

def symbolMapFromContent():
    symbolMap = {}
    reachFiles = False
    reachSections = False
    reachSymblos = False
    file = open(sys.argv[1])
    for line in file.readlines():
        if line.startswith("#"):
            if line.startswith("# Object files:"):
                reachFiles = True
            if line.startswith("# Sections:"):
                reachSections = True
            if line.startswith("# Symbols:"):
                reachSymblos = True
        else:
            if reachFiles == True and reachSections == False and reachSymblos == False:
                #查找 files 列表，找到所有.o文件
                location = line.find("]")
                if location != -1:
                    key = line[:location+1]
                    if  symbolMap.get(key) is not None:
                        continue
                    symbol = SymbolModel()
                    symbol.file = line[location + 1:]
                    symbolMap[key] = symbol
            elif reachFiles == True and reachSections == True and reachSymblos == True:
                #'\t'分割成三部分，分别对应的是Address，Size和 File  Name
                symbolsArray = line.split('\t')
                if len(symbolsArray) == 3:
                    fileKeyAndName = symbolsArray[2]
                    #16进制转10进制
                    size = int(symbolsArray[1],16)
                    location = fileKeyAndName.find(']')
                    if location != -1:
                        key = fileKeyAndName[:location + 1]
                        symbol = symbolMap.get(key)
                        if symbol is not None:
                            symbol.size = symbol.size + size
    file.close()

    return symbolMap

def sortSymbol(symbolList):
     return sorted(symbolList, key=lambda s: s.size,reverse = True)

def buildResultWithSymbols(symbols):
    results = ["文件大小\t文件名称\r\n"]
    totalSize = 0
    for symbol in symbols:
        results.append(calSymbol(symbol))
        totalSize += symbol.size
    results.append("总大小: %.2fM" % (totalSize/1024.0/1024.0))
    return results

def buildCombinationResultWithSymbols(symbols):
    #统计不同模块大小
    results = ["库大小\t库名称\r\n"]
    totalSize = 0
    combinationMap = {}

    for symbol in symbols:
        names = symbol.file.split('/')
        name = names[len(names) - 1].strip('\n')
        location = name.find("(")
        if name.endswith(")") and location != -1:
            component = name[:location]
            combinationSymbol = combinationMap.get(component)
            if combinationSymbol is None:
                combinationSymbol = SymbolModel()
                combinationMap[component] = combinationSymbol

            combinationSymbol.file = component
            combinationSymbol.size = combinationSymbol.size + symbol.size
        else:
            #symbol可能来自app本身的目标文件或者系统的动态库
            combinationMap[symbol.file] = symbol
    sortedSymbols = sortSymbol(combinationMap.values())

    for symbol in sortedSymbols:
        results.append(calSymbol(symbol))
        totalSize += symbol.size
    results.append("总大小: %.2fM" % (totalSize/1024.0/1024.0))

    return results

def calSymbol(symbol):
    size = ""
    if symbol.size / 1024.0 / 1024.0 > 1:
        size = "%.2fM" % (symbol.size / 1024.0 / 1024.0)
    else:
        size = "%.2fK" % (symbol.size / 1024.0)
    names = symbol.file.split('/')
    if len(names) > 0:
        size = "%s\t%s" % (size,names[len(names) - 1])
    return size

def analyzeLinkMap():
    if verify_linkmapfile(sys.argv) == True:
        print("**********正在开始解析*********")
        symbolDic = symbolMapFromContent()
        symbolList = sortSymbol(symbolDic.values())
        if len(sys.argv) >= 3 and sys.argv[2] == "-g":
            results = buildCombinationResultWithSymbols(symbolList)
        else:
            results = buildResultWithSymbols(symbolList)
        for result in results:
            print(result)
        print("***********解析结束***********")


if __name__ == "__main__":
    analyzeLinkMap()
