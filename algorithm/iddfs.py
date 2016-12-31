from algorithm import Algorithm

class IDDFS(Algorithm):

  def __init__(self, config, graph):
    super(IDDFS, self).__init__(config, graph)
    self.max_depth = 10

  def run(self):
    
    for depth in range(self.max_depth):
      # initialize parents in the beginning of each dfs ( it also serves the marker of discovery)
      self.parents = {
        self.start_page["pageid"] : self.start_page["pageid"]
      }
      
      self.found = self.dfs(self.start_page["pageid"], 0, depth)
      if(self.found):
        return
 
  def dfs(self, pageid, current_depth, max_depth):

    if(pageid == self.end_page["pageid"] and current_depth == max_depth):
      return True

    if(current_depth < max_depth):
      for page in self.graph.adj(pageid):
        # skip self link
        if(page["pageid"] == pageid):
          continue
        
        # already visited
        if(page["pageid"] in self.parents):
          continue
      
        self.parents[ page["pageid"]] = pageid   
        isfound = self.dfs(page["pageid"], current_depth + 1, max_depth)
        if(isfound):
          return True 
    return False
