from store import Store
import copy
from neo4j.v1 import GraphDatabase, basic_auth

class Neo4jStore(Store):
  def __init__(self, config):
    self.schema = config['scheme']
    self.host = config['host']
    self.port = config['port']
    self.username = config['username']
    self.password = config['password']
    self.driver = GraphDatabase.driver(self.schema + "://" + self.host + ":" + self.port, auth=basic_auth(self.username, self.password))

  def get_page_links(self, pageid):
    session = self.driver.session()
    result = session.run("match (:Page {pageid: {pageid}})-[:L]->(p:Page) return p.pageid as pageid, p.title as title, p.fullurl as fullurl", {"pageid": pageid})  
    pages = []
    for record in result:
      d = {}
      d.update(record.items())
      pages.append(d)
    session.close()
    return pages 
    
  def save_page_links(self, pageid, pages):
    session = self.driver.session()
    pages = copy.deepcopy(pages)
    for page in pages:
      page['from_pageid'] = pageid
      session.run('match (from:Page {pageid: {from_pageid}}) merge (to:Page {pageid: {pageid}, title: {title}, fullurl: {fullurl}}) merge (from)-[:L]->(to)', page)
    session.close() 


  def save_pages(self, pages):
    session = self.driver.session()
    for page in pages:
      session.run("merge (p:Page {pageid: {pageid}, title: {title}, fullurl: {fullurl}})", page)
    session.close()   
  
  def get_page_from_id(self, pageid):
    session = self.driver.session()
    result = session.run("match (p:Page {pageid: {pageid}}) return p.pageid as pageid, p.title as title, p.fullurl as fullurl", {"pageid": pageid})
    record = result.single()
    page = {}
    page.update(record.items())
    session.close()
    return page     

  def get_page_from_url_title(self, url_title):
    session = self.driver.session()
    result = session.run('match (p:Page) where p.fullurl =~".+/'+ str(url_title) +'" return p.pageid as pageid, p.title as title, p.fullurl as fullurl')
    try:
      record = result.single()
      page = {}
      page.update(record.items())
    except:
      session.close()
      return []
    session.close()
    return [page]

  def supports_path_query(self):
    return True

  def get_path(self, start_pageid, end_pageid):
    if start_pageid == end_pageid:
      return [self.get_page_from_id(start_pageid)]

    session = self.driver.session()
    result = session.run('match p=shortestPath( (s:Page {pageid: {from_pageid}})-[:L*..10]->(e:Page {pageid: {to_pageid}}) ) return p', {'from_pageid': start_pageid, 'to_pageid': end_pageid })
    try:
      record = result .single()
      path = record.values()[0]
      nodes = path.nodes
      pages = []
      for node in nodes:
        pages.append(node.properties)
    except:
      session.close()
      return []
    return pages 
