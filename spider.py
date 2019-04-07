#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 12:34:56 2019

@author: stark
"""
import requests
from PageLinker import LinkFinder
from domain import *
from utility import *

class Spider:
    
    projectName = ''
    baseURL = ''
    domainName = ''
    queueFile = ''
    crawledFile = ''
    queue = set()
    crawled = set()
    failed = set()
    
    def __init__(self,projectName,baseURL,domainName):
        Spider.projectName = projectName
        Spider.baseURL = baseURL
        Spider.domainName = domainName
        Spider.queueFile = pathJoin(Spider.projectName,'queue.txt')
        Spider.crawledFile = pathJoin(Spider.projectName,'crawled.txt')
        Spider.boot()
        Spider.crawlPage('First Page', Spider.baseURL)
        
    #Creates directory and files for the first run and starts the spider
    @staticmethod
    def boot():
        createProjectDir(Spider.projectName)
        createDataFiles(Spider.projectName,Spider.baseURL)
        Spider.queue = fileToSet(Spider.queueFile)
        Spider.crawled = fileToSet(Spider.crawledFile)
        Spider.queue.add(Spider.baseURL)
        
    #Updates user display, fills queue and update files
    @staticmethod
    def crawlPage(threadName,pageURL):
        if pageURL not in Spider.crawled:
            print(threadName +': now crawling : '+ pageURL)
            print('Queue : ' + str(len(Spider.queue)) + ' | Crawled : ' + str(len(Spider.crawled)))
            
            Spider.queue.remove(pageURL)
            Spider.addLinksToQueue(Spider.gatherLinks(pageURL))
            Spider.crawled.add(pageURL)
            Spider.updateFiles()
            
            
    #COnverts raw response data into readable information and checks for proper html formating
    @staticmethod
    def gatherLinks(pageURL):
        try:
            response = requests.get(pageURL)
            if response.status_code == 200:
                if 'text/html' in response.headers['Content-Type']:
                    response.encoding = 'UTF-8'
                    htmlString = response.text
                    finder = LinkFinder(Spider.baseURL,pageURL,Spider.projectName)
                    finder.feeder(htmlString)
                else:
                    return set()
            else:
                raise Exception('Request staus code' , response.status_code)
        except Exception as e:
                print(str(e))
                if(pageURL not in Spider.failed):
                    Spider.queue.add(pageURL)
                    Spider.failed.add(pageURL)
                print(Spider.failed)
                return set()
            
        return finder.returnLinks()

    
    #Save queue data to project files
    @staticmethod
    def addLinksToQueue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if(Spider.domainName != get_domain_name(url)):
                continue
            Spider.queue.add(url)
            
    @staticmethod
    def updateFiles():
        setToFile(Spider.queueFile,Spider.queue)
        setToFile(Spider.crawledFile,Spider.crawled)
    
    
            
            
            
            
            
            
            
            
            
            
            
            
            
            