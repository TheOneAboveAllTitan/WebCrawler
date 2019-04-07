#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 11:39:25 2019

@author: stark
"""

import os

def createProjectDir(projectname):
    if not os.path.exists(projectname):
        print('Creating project : '+projectname)
        os.mkdir(projectname)
        os.mkdir(pathJoin(projectname,'Data'))

def createDataFiles(projectName,base_url):
    queue = os.path.join(projectName,'queue.txt')
    crawled = os.path.join(projectName,'crawled.txt')
    if not os.path.exists(queue):
      writeFile(queue,base_url)
    if not os.path.exists(crawled):
        writeFile(crawled,'')
        
def writeFile(fileName,data):
    with open(fileName,'w') as Blob:
        Blob.write(data)
        Blob.close()
        
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


def dataToSet(data):
    dataSet = set()
    dataSet.add(data)
    return dataSet

def fileToSet(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# Iterate through a set, each item will be a line in a file
def setToFile( file_name,links,):
    with open(file_name,"w") as f:
        for l in sorted(links):
            f.write(l+"\n")

pathJoin = os.path.join