from algorithm import Algorithm
from collections import deque

class BFS(Algorithm):

  def __init__(self, config, graph):
    super(BFS, self).__init__(config, graph)

  def debug(self, size):
    if(size % 100 == 0):
      print("current bfs Q size: %d" % size)

  def run(self):
    q  = deque()
    q.append(self.start_page["pageid"])

    while( len(q) > 0 and not self.found):
      #self.debug(len(q)) 
      pageid = q.popleft()
      page_links = self.graph.adj(pageid)
      for page_link in page_links:
        
        # skip self links:
        if( pageid ==  page_link["pageid"]):
          continue
       
        # already visited 
        if( page_link["pageid"] in self.parents):
          continue
        
        self.parents[ page_link["pageid"] ] = pageid
        if(page_link["pageid"] == self.end_page["pageid"]):
          self.found = True
          break
        q.append(page_link["pageid"])
 
