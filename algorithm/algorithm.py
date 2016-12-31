from collections import deque
# base class for all shortest page algorithms on wiki graph

class Algorithm(object):
  
  def __init__(self, config, graph):
    self.config = config
    self.graph = graph
    self.start_page = config["start_page"]
    self.end_page = config["end_page"]

    # lets make source's parent itself
    self.parents = {
      self.start_page["pageid"] : self.start_page["pageid"]
    }
    # was path found by running algorithm ?
    self.found = False
    if(self.start_page["pageid"] == self.end_page["pageid"]):
      self.found = True

  def run(self):
    pass
  
  def path(self):
    if(self.found):
      path = deque()
      current = self.end_page["pageid"]
      start_pageid = self.start_page["pageid"]
      while(current != start_pageid):
        path.appendleft(self.graph.page(current)["fullurl"])
        current = self.parents[current]
      path.appendleft(self.graph.page(current)["fullurl"])
      return list(path)
    return []
