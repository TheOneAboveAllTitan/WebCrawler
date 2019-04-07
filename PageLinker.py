#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 11:18:38 2019

@author: stark
"""

from html.parser import HTMLParser
from urllib import parse
from utility import writeFile,pathJoin

class LinkFinder(HTMLParser):
    def __init__(self,baseURL,pageURL,projectName):
        HTMLParser.__init__(self)
        self.baseURL = baseURL
        self.pageURL = pageURL
        self.projectName = projectName
        self.Links = set()
        self.titleMatch = False
        self.webData = ''

    def feeder(self,webPage):
        self.webData = webPage
        self.feed(webPage)
        
    def handle_starttag(self,tag,attrs):
        if 'a' in tag :
            for (attribute,value) in attrs:
                if attribute == 'href':
                    if '#' not in value:
                        url = parse.urljoin(self.baseURL,value)
                        self.Links.add(url)
        if 'title' == tag:
            self.titleMatch = True
            
            
    def handle_data(self,data):
        if self.titleMatch == True:
            filename = pathJoin(self.projectName,'Data',self.parseTitle(data) + '.html')
            writeFile(filename,self.webData)
            self.titleMatch = False
        
    def parseTitle(self,filename):
        filename.replace('|','')
        filename.replace('/','')
        return filename
    
    def returnLinks(self):
        return self.Links
    
