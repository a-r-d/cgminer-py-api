import socket
import sys
import json
import pprint
import time
import os
import subprocess
from threading import Thread, Lock, currentThread
from entities import *
from api import *
from cgminer_controller import *
from beans import *
'''
Note: 
cgminer must be started with --api-listen and --api-allow  W:127.0.0.1

Example:
C:\Users\usr\Desktop\cgminer-2.11.1-win32\cgminer.exe  --scrypt -o http://notroll.in:6332 -u meard.1 -p 12345 --thread-concurrency 4800 -I 13 -g 1 -w 256 --api-listen --api-allow W:127.0.0.1

JSON request example:
{"command":"gpufan","parameter":"0,80"}
'''
# cd 'D:\Dropbox\client work\coincepts project\py-client'

THREAD_INTENSITY_CHECKER = None
THREAD_MINER = None
CGMINER = None

### GLOBALS
VERBOSITY = 5

### THREAD LOCKS:
PRINT_LOCK = Lock()
CGMINER_PROCESS_LOCK = Lock()


def smart_print(level, txt):
    if VERBOSITY > level:
        PRINT_LOCK.acquire()
        thread_name = currentThread().name
        print thread_name, ": ", txt
        PRINT_LOCK.release()


def startCGMINER( pparams ):
    """
    pparams = PoolParams() bean class
    
    """
    ## set pool params
    CGMINER = CGminerController()
    CGMINER.poolURL = pparams.url
    CGMINER.username = pparams.username 
    CGMINER.password = pparams.password
    CGMINER.threadconcur = pparams.threadconcur
    CGMINER.intensity = pparams.intensity
    CGMINER.numthreads = pparams.numthreads
    CGMINER.worksize = pparams.worksize
    CGMINER.extra = pparams.extra
    
    ## spawn the miner!
    CGMINER_PROCESS_LOCK.acquire()
    CGMINER.spawnCGMiner()
    CGMINER_PROCESS_LOCK.release()


def testIntensityAdjuster():
    HIGH_INTENSITY = 95
    LOW_INTENSITY = 90
    time.sleep(20) # give cgminer time to start
    while(1):
        time.sleep(3)
        
        if CGMINER == None:
            continue
        
        CGMINER_PROCESS_LOCK.acquire()
        if CGMINER.getStatus() == None:
            # miner is dead. should wait 60 seconds of death before restart attempt.
            CGMINER_PROCESS_LOCK.release()
            continue
        CGMINER_PROCESS_LOCK.release()
        
        try:
            gpus = getAllGPUs()
            for gpu in gpus:
                smart_print(3, "current intensity: " + str(gpu.intensity))
                smart_print(3, "current activity: " + str(gpu.gpu_activity))
                #this is a GPU() proper.
                
                if gpu.gpu_activity > HIGH_INTENSITY:
                    smart_print(1, "decrease intensity")
                    setIntensityDifferenceTargetGPU( -1, gpu.index)
                    continue
                    
                if gpu.gpu_activity < LOW_INTENSITY:
                    smart_print(1, "increase intensity")
                    setIntensityDifferenceTargetGPU( 1, gpu.index)
                    continue
                    
        except Exception, e:
            smart_print(1, "Exception on intensity checker: " + str(e))


def testAllApis():
    gpucount = getGpuCount()
    pprint.pprint(vars(gpucount))
    
    gpus = getAllGPUs()
    for gpu in gpus:
        pprint.pprint( vars(gpu) )

    pools = getPools()
    for pool in pools.pools:
        pprint.pprint( vars(pool) )
        
    setIntensityDifferenceAllGpus(1)
    
    #time.sleep(5)
    gpus = getAllGPUs()
    for gpu in gpus:
        pprint.pprint( vars(gpu) )
            
    setIntensityDifferenceAllGpus(-1)


def cgminerThread():
    pparams = PoolParams()
    pparams.url = "http://notroll.in:6332"
    pparams.username = "meard.1"
    pparams.password = "12345"
    
    global THREAD_INTENSITY_CHECKER
    global THREAD_MINER
    
    THREAD_INTENSITY_CHECKER = Thread(target=testIntensityAdjuster)
    THREAD_MINER = Thread(target=startCGMINER, args=(pparams,)) #must be a tuple
    
    THREAD_INTENSITY_CHECKER.name = "Intensity checker thread"
    THREAD_MINER.name = "Miner control thread"
    THREAD_MINER.start()
    THREAD_INTENSITY_CHECKER.start()
    

if __name__ == "__main__":
    #testAllApis()
    print "Begin test suite: "
    cgminerThread()
    
    
    