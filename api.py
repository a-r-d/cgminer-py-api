import socket
import sys
import json
import pprint
import time
from entities import *

DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = 4028
SOCKET_cxn = None

def setParams( ip, port):
    global DEFAULT_IP
    global DEFAULT_PORT
    DEFAULT_IP = ip
    DEFAULT_PORT = port

    
def failon( testname ):
    global SOCKET_cxn
    msg = "FAILED: " + testname + "\n"
    print msg * 7
    SOCKET_cxn.close()
    #sys.exit()

    
def doSendRecieve(message):
    global SOCKET_cxn
    try :
        #Set the whole string
        SOCKET_cxn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SOCKET_cxn.connect((DEFAULT_IP , DEFAULT_PORT))
        #print 'Socket Connected to ' + DEFAULT_IP + ' on ip ' + DEFAULT_IP + ":" + str(DEFAULT_PORT)
        SOCKET_cxn.sendall(message)
    except socket.error, e:
        failon( "doSendRecieve " + str(e) + message )
    #Now receive data
    reply = SOCKET_cxn.recv(4096).strip()
    SOCKET_cxn.close()
    return reply.replace('\x00', '') #there is crud at the end of the socket reply

    
def getGPU( whichOne = 0 ):
    """
    whichOne is an int, the gpu
    returns GPU()
    """
    try:
        message = '{"command":"gpu","parameter":"' + str(whichOne) + '"}'
        reply = doSendRecieve(message)
        gpus = GPUs(reply)
        return gpus.gpus[0]
    except Exception, e:
        failon( "gpu " + str(e) )
        return None
        
def getPools():
    """
    gets all pools
    """
    try:
        message = '{"command":"pools"}'
        reply = doSendRecieve(message)
        if reply == None:
            failon( "pools, empty reply")
        pools = Pools(reply)
        return pools
    except Exception, e:
        failon( "pools " + str(e) )
        return None
    
def getGpuCount():
    """
    gets the count of GPUs
    """
    try:
        message = '{"command":"gpucount"}'
        reply = doSendRecieve(message)
        gpucount = GPUCount(reply)
        return gpucount
    except Exception, e:
        failon( "getGpuCount " + str(e) )
        return None
        
    
def getAllGPUs():
    gpucount = getGpuCount()
    gpus = []
    for i in range(gpucount.count):
        gpu = getGPU(i)
        gpus.append( gpu )
    return gpus
    
    
def setIntensityDifferenceAllGpus( diffAmount ):
    try:
        gpus = getAllGPUs()
        for gpu in gpus:
            new_intensity = gpu.intensity + diffAmount
            message = '{"command":"gpuintensity","parameter":"' + str(gpu.index) + ',' + str(new_intensity) + '"}'
            reply = doSendRecieve(message)
        return True
    except Exception, e:
        failon( "testChangeIntesity " + str(e) )
        return False
        
def setIntensityDifferenceTargetGPU( diffAmount, gpuIndex = 0):
    """
    diffAmount e.g. 1 or -1 will change by this amount
    gpuIndex, which GPU to change.
    """
    try:
        gpus = getAllGPUs()
        for gpu in gpus:
            if gpu.index == gpuIndex:
                new_intensity = gpu.intensity + diffAmount
                message = '{"command":"gpuintensity","parameter":"' + str(gpu.index) + ',' + str(new_intensity) + '"}'
                reply = doSendRecieve(message)
        return True
    except Exception, e:
        failon( "testChangeIntesity " + str(e) )
        return False
        
        
def setIntensityTargetGPU( newIntensity, gpuIndex = 0):
    """
    newIntensity e.g. 1 or -1 will change by this amount
    gpuIndex, which GPU to change.
    """
    try:
        message = '{"command":"gpuintensity","parameter":"' + str(gpuIndex) + ',' + str(newIntensity) + '"}'
        reply = doSendRecieve(message)
        return True
    except Exception, e:
        failon( "testChangeIntesity " + str(e) )
        return False
        

        