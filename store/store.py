class Store():

  def __init__(self):
    pass

  def pages_from_list(self, page_list):
    pages = []
    for page in page_list:
      pages.append({"pageid": page[0], "title": page[1], "fullurl": page[2]})
    return pages

  def get_page_links(self, pageid):
    pass 

  def save_page_links(self, pageid, pages):
    pass

  def save_pages(self, pages):
    pass

  def get_page_from_id(self, pageid):
    pass

  def get_page_from_url_title(self, url_title):
    pass

  def supports_path_query(self):
    return False

  def get_path(self, from_pageid, to_pageid):
    return [] 
