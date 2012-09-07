# -*- coding: utf-8 -*-
## ----------------------------------------------------------------
## Cache
## 
## @Interface
## ----------------------------------------------------------------
class Cache(object):
    cache = None
    def __init__(self): pass
    def get(self, name): raise CacheErrorException
    def set(self, name, value): raise CacheErrorException
    def purge(self): raise CacheErrorException
    def remove(self, name): raise CacheErrorException


## ----------------------------------------------------------------
## MemcacheStore
## 
## @
## ----------------------------------------------------------------
class MemcacheStore(Cache):

    cache = None

    def __init__(self):
        import memcache
        self.cache = memcache.Client(['localhost:11211'])

    def get(self, name):
        return self.cache.get(name)

    def set(self, name, value):
        return self.cache.set(name, value)


import sys
sys.path.append('/opt/tornado')
from app.models.Error import Error
## ----------------------------------------------------------------
## CacheErrorException
## 
## @
## ----------------------------------------------------------------
class CacheErrorException(Error):
    pass
