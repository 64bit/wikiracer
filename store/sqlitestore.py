import sqlite3
from store import Store

class SqliteStore(Store):

  # store (pageid, title, fullurl)
  SQL_CREATE_PAGE_TABLE = '''
    create table if not exists pages (
      pageid INT PRIMARY KEY,
      title VARCHAR(255),
      fullurl VARCHAR(255)
    )'''

  # Link from a Wikipedia page
  SQL_CREATE_LINK_TABLE = '''
    create table if not exists links (
      from_pageid INT,
      to_pageid INT,
      UNIQUE(from_pageid, to_pageid)
    )'''   

  # Insert into page table
  SQL_INSERT_PAGE = "insert or ignore into pages values (:pageid, :title, :fullurl)"
  # Insert into link table
  SQL_INSERT_LINK = "insert or ignore into links values (:from_pageid, :to_pageid)" 
   
  # Query link table
  SQL_QUERY_LINK = "select to_pageid from links where from_pageid = :from_pageid"
  # Query page table
  SQL_QUERY_PAGE = "select * from pages where pageid in (%s)"
  SQL_QUERY_PAGE_ID = "select * from pages where pageid = :pageid"
  # Query url title (end segment) in pages table
  SQL_QUERY_URL_TITLE = 'select * from pages where fullurl like ?'

  def __init__(self, config):
    self.config = config
    self.__setup__(config)

  def __setup__(self, config):
    self.conn = sqlite3.connect(config["dbname"])
    self.__create_tables__(config)
    
  def __create_tables__(self, config):
    curs = self.conn.cursor()
    curs.execute(SqliteStore.SQL_CREATE_PAGE_TABLE)
    curs.execute(SqliteStore.SQL_CREATE_LINK_TABLE)
    self.conn.commit() 
    curs.close()

  def get_page_links(self, pageid):
    curs = self.conn.cursor()
    curs.execute(SqliteStore.SQL_QUERY_LINK, {"from_pageid": pageid})
    links = curs.fetchall() 
    pageids = []
    for link in links:
      pageids.append(link[0])
    
    curs.execute(SqliteStore.SQL_QUERY_PAGE % ",".join('?' * len(pageids)), pageids)
    page_list = curs.fetchall()
    
    pages = self.pages_from_list(page_list) 
    curs.close()
    return pages

  def save_page_links(self, pageid, pages):
    curs = self.conn.cursor()
    for page in pages:
      curs.execute(SqliteStore.SQL_INSERT_PAGE, page)
      curs.execute(SqliteStore.SQL_INSERT_LINK, { "from_pageid": pageid, "to_pageid": page["pageid"]})
    self.conn.commit()
    curs.close() 

  def save_pages(self, pages):
    curs = self.conn.cursor()
    for page in pages:
      curs.execute(SqliteStore.SQL_INSERT_PAGE, page)
    self.conn.commit()
    curs.close()

  def get_page_from_id(self, pageid):
    curs = self.conn.cursor()
    curs.execute(SqliteStore.SQL_QUERY_PAGE_ID, { "pageid" : pageid})
    page = curs.fetchone()
    return {
      "pageid" : page[0],
      "title" : page[1],
      "fullurl" : page[2]
    } 

  def get_page_from_url_title(self, url_title):
    curs = self.conn.cursor()
    curs.execute(SqliteStore.SQL_QUERY_URL_TITLE, ("%/" + url_title,)) 
    page_list = curs.fetchall()
    pages = self.pages_from_list(page_list) 
    return pages
