#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 13:24:02 2019

@author: stark
"""

import threading
from queue import Queue
from spider import Spider
from domain import *
from utility import *


PROJECT_NAME = 'dragzon'
HOMEPAGE = 'https://dragzon.com'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


def crawl():
    queued_links = fileToSet(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()

def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()
    
def work():
    while True:
        url = queue.get()
        Spider.crawlPage(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in fileToSet(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()
    
create_workers()
crawl()