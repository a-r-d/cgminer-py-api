"""
This file will contain beans that are
not actual entities passed back from cgminer
or our pool API.

"""
class PoolParams():
    def __init__(self):
        pass
    
    url = None
    username = None
    password = None
    threadconcur = 4800
    intensity = 12
    numthreads = 1
    worksize = 256
    extra = "--scrypt"