from cache import Cache

class DBCache(Cache):
  
  def __init__(self, dbstore):
    #setup db
    self.dbstore = dbstore

  def get(self, key):
    return self.dbstore.get_page_links(key)

  def put(self, key, value):
    self.dbstore.save_page_links(key, value)
