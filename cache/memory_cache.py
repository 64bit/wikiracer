from cache import Cache
from collections import defaultdict
class MemoryCache(Cache):
  def __init__(self):
    self.cache = defaultdict(lambda: [])

  def get(self, key):
    return self.cache[key]

  def put(self, key, value):
    self.cache[key] = value  
