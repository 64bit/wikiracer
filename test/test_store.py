import unittest
import sys
sys.path.append("../")
from store.store import Store
from store.neo4jstore import Neo4jStore
from store.sqlitestore import SqliteStore

from neo4j.v1 import GraphDatabase, basic_auth

class TestStore(unittest.TestCase):
  
  def setUp(self):
    self.store = Neo4jStore() 
    self.pages = [ 
      { 
        'pageid': 1,
        'title': 'one',
        'fullurl' : 'https://wiki.com/one'
      },
      { 
        'pageid': 2,
        'title': 'two',
        'fullurl' : 'https://wiki.com/two'
      },
    ]
  
    self.pages_dist_1 = [
      { 
        'pageid': 3,
        'title': 'three',
        'fullurl' : 'https://wiki.com/three'
      },
      { 
        'pageid': 4,
        'title': 'four',
        'fullurl' : 'https://wiki.com/four'
      },
    ] 

    self.pages_dist_2 = [
      { 
        'pageid': 5,
        'title': 'five',
        'fullurl' : 'https://wiki.com/five'
      },
      { 
        'pageid': 6,
        'title': 'six',
        'fullurl' : 'https://wiki.com/six'
      },
    ] 

  def tearDown(self):
    pass

  def test_save_pages(self):
    self.store.save_pages(self.pages)
    for page in self.pages:
      read_page = self.store.get_page_from_id(page['pageid'])
      self.assertEqual(read_page, page) 
    

  def test_save_and_get_page_links(self):
    self.store.save_pages(self.pages)
    self.store.save_page_links(1, self.pages_dist_1) 
    self.store.save_page_links(3, self.pages_dist_2) 
    read_page_links = self.store.get_page_links(1)
    self.assertEqual(2, len(read_page_links)) 

    page_3 = filter(lambda p: p['pageid'] == 3, read_page_links)[0]    
    page_4 = filter(lambda p: p['pageid'] == 4, read_page_links)[0]    
    self.assertEqual(self.pages_dist_1[0],  page_3)
    self.assertEqual(self.pages_dist_1[1],  page_4)

    read_page_links2 = self.store.get_page_links(3)
    self.assertEqual(2, len(read_page_links2)) 

    page_5 = filter(lambda p: p['pageid'] == 5, read_page_links2)[0]    
    page_6 = filter(lambda p: p['pageid'] == 6, read_page_links2)[0]    
    self.assertEqual(self.pages_dist_2[0],  page_5)
    self.assertEqual(self.pages_dist_2[1],  page_6)
     

    self.assertEqual([], self.store.get_page_links(2))
    self.assertEqual([], self.store.get_page_links(4))
    self.assertEqual([], self.store.get_page_links(5))
    self.assertEqual([], self.store.get_page_links(6))

  def test_get_page_from_url_title(self):
    self.store.save_pages(self.pages)
    page1 = self.store.get_page_from_url_title('one')
    self.assertEqual(1, len(page1))
    self.assertEqual(self.pages[0], page1[0])
    

if __name__ == "__main__":
  unittest.main()
