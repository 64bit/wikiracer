from cache import Cache

class HierarchicalCache(Cache):
  def __init__(self, caches):
    self.caches = caches

  def get(self, key):
    found_index = -1
    value = [] 
    for idx, cache in enumerate(self.caches):
      value = cache.get(key)
      if(value == []):
        continue
      else:
        found_index = idx
        break
    
    if(found_index >= 0):
      self.add(key, value, found_index)
    return value
     
  def add(self, key, value, upto = 0):
    for i in range(upto):
      self.caches[i].put(key, value)
      

  def put(self, key, value):
    self.add(key, value, len(self.caches)) 
