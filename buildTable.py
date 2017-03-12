import sys,os

def readFile(fileHandle): 

    line = fileHandle.readline()
    
    dictName = {} 
    line = fileHandle.readline() 
    while line:
        vals = line.split()
        dictName[vals[0]] = vals[1]
        line = fileHandle.readline() 
   
    return dictName


def norm(x) :
    return float(x)/300.

ori =  readFile(open('ori.dat'))
pre2 =  readFile(open('pre2.dat'))
new = readFile(open('new.dat'))

lines = {}
vals = []
for key,vori in ori.iteritems() :
     lines[-int(float(vori)*100)] = [key, float(vori), float(pre2[key]), float(new[key])]
     vals.append(int(-float(vori)*100))

vals.sort()
for i in vals:
    print "||!%s |  %.3f |  %.3f |  %.3f ||" % (lines[i][0],norm(lines[i][1]),norm(lines[i][2]),norm(lines[i][3]))


