#!/usr/bin/python3
# coding=utf-8

import sys
import re
import pymorphy2
from slang import cleanup

import queue
import threading
import multiprocessing

if len(sys.argv)!=2:
    print("Usage:\n\t",__file__,"file.txt")
    sys.exit(0)

try:
    fd = open(sys.argv[1], encoding='utf-8')
except:
    print("Can't open file")
    sys.exit(0)

print("Loading file")
file = fd.read()
print("Loaded", len(file))

stat  = {} # word-> count
norm  = {} # norm-> count
cache = {} # word-> norm

morph = pymorphy2.MorphAnalyzer()

q = queue.Queue()

def worker():                               
    print("worker start")
    k = 0
    while True:
        l = q.get()

        try:
            (txt, tone) = cleanup(l)
        except:
            # q.task_done()
            continue
        t =''
        n =''    
        for t in txt.split(" "):
            # count word
            stat[t] = stat.get(t, 0)+1
            # get norm
            n = cache.get(t, None)
            if n == None:
                cache[t] = n = morph.parse(t)[0].normal_form
            norm[n] = norm.get(n,0)+1

        k+=1
        if k%1000 == 0:
            print(q.qsize(),t,'->',n)
        if l is None:
            break

cores = multiprocessing.cpu_count()

lines = file.split("\n")
print("Put",len(lines),"to queue")
for l in file.split('\n'):
    if len(l)>0:
        q.put(l)
q.put(None)
worker()

def write(fn, obj):
    print("Write",fn)
    fd = open(fn, "w")
    for k in sorted(obj, key=obj.get, reverse=True):
        fd.write(k+"\t"+str(obj[k])+"\n")

write("stat.tsv", stat)
write("norm.tsv", norm)
