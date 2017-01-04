from cache.hierarchical_cache import HierarchicalCache as HierCache
from cache.memory_cache import MemoryCache as MemCache
from cache.db_cache import DBCache
import api

class WikiGraph():

  def __init__(self, config):
    # in memory cache
    memcache = MemCache()
    
    # db store
    dbstore = config['dbstore'] 

    # db cache
    dbcache = DBCache(dbstore)
    
    caches = [ memcache, dbcache ] 
    self.hc = HierCache(caches)
    self.dbstore = dbstore

  def adj(self, pageid):
    
    # not in cache 
    if(self.hc.get(pageid) == []):
      # network call
      pages = api.links_for_pageids(pageid)
      # cache it
      self.hc.put(pageid, pages)
      return pages
    else:
      # return from cache
      return self.hc.get(pageid)
  
  def page(self, pageid):
    return self.dbstore.get_page_from_id(pageid)

  # offloads the path computation to backend store
  def path(self, from_pageid, to_pageid):
    if self.dbstore.supports_path_query():
      return self.dbstore.get_path(from_pageid, to_pageid)
    return []
      
