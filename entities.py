import json

DEBUG_ENTITIES = False

def dprint(statement):
    if DEBUG_ENTITIES:
        print statement

class Pool():
    def __init__(self, jsonData):
        dprint("init a pool")
        if jsonData == None:
            return
        self.raw_data = jsonData
        self.url = jsonData["URL"]
        self.index = jsonData["POOL"]
        self.user = jsonData["User"]
        if jsonData["Status"] == "Alive":
            self.status = True
    raw_data = None
    url = None
    index = 0
    user = None
    status = False # True == alive

class Pools():
    def __init__(self, jsonData):
        dprint("init pools")
        jsonLoaded = json.loads( jsonData )
        pool_list = jsonLoaded["POOLS"]
        self.pools = []
        for pool in pool_list:
            thisPool = Pool(pool)
            self.pools.append( thisPool )
    pools = []

class GPU():
    def __init__(self, jsonData):
        if jsonData == None:
            return
        dprint("init a gpu")
        self.raw_data = jsonData
        if jsonData["Enabled"] == "Y":
            self.enabled = True
        self.gpu_activity = float(jsonData["GPU Activity"])
        self.diff_work = float(jsonData["Diff1 Work"])
        self.index = int(jsonData["GPU"])
        self.fan_percentage = float(jsonData["Fan Percent"])
        self.intensity = float(jsonData["Intensity"])
        
    intensity = 0
    raw_data = None
    enabled = False
    index = 0
    status = False
    gpu_activity = 0 # a percentage
    mhs_av = 0 # for litecoin * 1000 for kh/s
    diff_work = 0
    fan_percentage = 0
    temperature = 0
    
class GPUs():
    def __init__(self, jsonData):
        if jsonData == None:
            return
        self.raw_data = jsonData
        dprint("init gpus")
        jsonLoaded = json.loads( jsonData )
        gpu_list = jsonLoaded["GPU"]
        self.gpus = []
        for gpu in gpu_list:
            thisGPU = GPU(gpu)
            self.gpus.append( thisGPU )
    raw_data = None
    gpus = []
    
    
class GPUCount():
    def __init__(self, jsonData):
        if jsonData == None:
            return
        self.raw_data = jsonData
        jsonLoaded = json.loads( jsonData )
        gpu_count_list = jsonLoaded["GPUS"]
        self.count = int( gpu_count_list[0]["Count"] )
    raw_data = None
    count = 0
    
    
    
    