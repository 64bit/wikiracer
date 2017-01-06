# Wikiracer
Finds path between two Wikipedia pages , using BFS or ID-DFS

# Usage

```bash
./wikirace '{
    "start":"https://en.wikipedia.org/wiki/Malaria",
    "end":"https://en.wikipedia.org/wiki/Geophysics"
}'
```
Dependencies:
* pip install requests
* pip install neo4j-driver==1.1.0b1
* Download Neo4j & set password to "nj" (see settings.cgf)
* Create index by running query: ```CREATE INDEX ON :Page(pageid)```

A sample sqlite [graph.db](https://www.dropbox.com/s/8g54yihcjm46rx2/graph.db?dl=0) (51.66 MB) , I built locally for usage example above and some others.
