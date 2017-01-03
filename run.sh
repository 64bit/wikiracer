#!/bin/bash

./wikirace '{
    "start":"https://en.wikipedia.org/wiki/Malaria",
    "end":"https://en.wikipedia.org/wiki/Geophysics"
}' 

# By default it runs BFS algorithm , to run
# ID-DFS pass one more parameter in the end: 

#./wikirace '{
#    "start":"https://en.wikipedia.org/wiki/Malaria",
#    "end":"https://en.wikipedia.org/wiki/Geophysics"
#}' IDDFS
