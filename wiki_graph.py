from cache.hierarchical_cache import HierarchicalCache as HierCache
from cache.memory_cache import MemoryCache as MemCache
from cache.db_cache import DBCache
from store.sqlitestore import SqliteStore
from store.neo4jstore import Neo4jStore
import api

class WikiGraph():

  def __init__(self):
    # in memory cache
    memcache = MemCache()
    
    # db store
    #dbstore = SqliteStore({"dbname": "graph.db"})
    dbstore = Neo4jStore()

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
