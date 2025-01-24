"""
题目就是写个类似于cache的class，提供add（key，value，timeToLiveInSeconds），提供get（key）。
也就是说add进来的entry首先会override existing entry if same key，然后这个value会在TTL之后expire。
所以不同时间get会得到不同的结果。写完后要实地测一测。

Follow Up是新进来的entry只会override和自己时间窗overlap的时间窗，不影响别的时间窗。比如第0秒放入（k1，v1，10），第3秒放入（k1，v2，2）。
那么第4秒的get k1会得到v2，第9秒的get k1会得到v1，因为v2只生存于3秒和5秒之间。写完后要‍‌‌‍‌‌‍‍‍‍‌‌‌‍‌‌‍实地测一测。
"""

import time
class TTLCache:
    def __init__(self):
        self.cache={}
    
    def add(self, key, value, timeToLiveInSeconds):
        expire_time=time.time()+ timeToLiveInSeconds
        self.cache[key]=(value, expire_time)
    
    def get(self, key):
        if key in self.cache:
            value, expire_time=self.cache[key]
            if time.time()<expire_time:
                return value
            else:
                del self.cache[key]
        return None
    


import time
class TTLCache:
    def __init__(self):
        self.cache={}
    
    def add(self, key, value, timeToLiveInSeconds):
        curr_time=time.time()
        expire_time=curr_time+ timeToLiveInSeconds

        if key not in self.cache:
            self.cache[key]=[(value, curr_time, expire_time)]
        else:
            update=[]
            for v, start, end in self.cache[key]:
                if end<=curr_time or start>=expire_time:
                    self.cache[key].append((v, start, end))
                else:
                    if start<curr_time:
                        update.append((v, start, curr_time))
                    if end>expire_time:
                        update.append((v, expire_time, end))
            update.append((value, curr_time, expire_time))
            self.cache[key]=sorted(update, key=lambda x: x[1])
    
    def get(self, key):
        curr=time.time()
        if key in self.cache:
            for v, start, end in self.cache[key]:
                if start<=curr<expire_time:
                    return v
        return None
    

