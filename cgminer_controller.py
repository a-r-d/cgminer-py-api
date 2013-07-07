#threaded cgminer checker.
"""
What:

This class is essentially 
1. takes pool arguments,
2. spawns the cgminer process.
3. checks up on the cgminer.

Note: we do this threaded so we have locks for printing...

"""
import os
import subprocess
import time
        
class CGminerController():
    def __init__(self):
        print("init CGminerController")
        
    ### anytime we do any work with this process, lets get a lock    
    def spawnCGMiner():
        params = "-o %s -u %s -p %s --thread-concurrency %s -I %s -g %s -w %s %s" % (
            self.poolURL, 
            self.username, 
            self.password, 
            str(self.threadconcur), 
            str(self.intensity), 
            str(self.numthreads), 
            str(self.worksize), 
            self.extra
            )
        
        path = os.getcwd() + \
            "\cgminer\cgminer.exe --api-listen --api-allow  W:127.0.0.1 --text-only " + \
            params
            
        print "Starting cgminer... " + path 
        self.current_process = subprocess.Popen(path, stdout=subprocess.PIPE) #, stderr=subprocess.PIPE
        #self.current_process.wait()
        #time.sleep(15) #pointless on another thread.
    
    def killProcess():
        current_process.terminate()
        self.status = 0
    
    def getStatus():
        """
        Returns None if still running.
        Otherwise returns a returncode.
        If we return a code, should try to restart.
        """
        self.status = current_process.returncode
        return self.status
            
    # should only ever spawn one?
    current_process = None
    status = 0 # None ia no returncode = still runing, 0 = finished. 1 = error
    
    ## miner details- must be set:
    poolURL = None
    username  = None
    password  = None
    threadconcur = None
    intensity = 0
    numthreads = 0
    worksize  = 0
    extra = "--scrypt"
    