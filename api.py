import requests
import sys
  
def get_request():
  return {
    'generator': 'links',
    'prop': 'info',
    'inprop': 'url',
    'gpllimit': 'max',
    'action' : 'query',
    'format': 'json'
  }

def filter_keys():
  return [
    "lastrevid",
    "pagelanguagedir",
    "ltr",
    "editurl",
    "pagelanguagehtmlcode",
    "length",
    "contentmodel",
    "pagelanguage",
    "touched",
    "canonicalurl"
  ]

def filter_list(lst):
  for item in lst:
    for key in filter_keys():
      if key in item:
        del item[key]
  

def filter_missing_pageids(pages):
  filtered = []
  for page in pages:
    if "pageid" in page:
      filtered.append(page)
  return filtered

def links_for_titles(titles):
  request = get_request()  
  request['titles'] = titles
  return fetch(request)

def links_for_pageids(pageids):
  request = get_request()
  request['pageids'] = pageids 
  return fetch(request) 

def info_for_titles(titles):
  titles = "|".join(titles)
  request =  {
    'prop': 'info',
    'inprop': 'url',
    'action' : 'query',
    'format': 'json',
    'titles' : titles
  }
  return fetch(request)

def debug(result, request, istitle=True):
  if(not istitle):
    sys.stdout.write("Fetched {} links for pageids: {} \r".format(len(result["pages"]), request["pageids"]))
    sys.stdout.flush()
  if(istitle):
    sys.stdout.write("Fetched {} links for titles: {}\r".format(len(result["pages"]), request["titles"]))
    sys.stdout.flush()

def fetch(request):
  all = []
  for result in query(request):
    #debug(result, request, "titles" in request.keys())
    newpages = result["pages"].values()
    filter_list(newpages)
    all = all + newpages 
  return filter_missing_pageids(all)

# method query(...) copied from documentation : https://www.mediawiki.org/wiki/API:Query

def query(request):
    request['action'] = 'query'
    request['format'] = 'json'
    lastContinue = {'continue': ''}
    while True:
        # Clone original request
        req = request.copy()
        # Modify it with the values returned in the 'continue' section of the last result.
        req.update(lastContinue)
        # Call API
        result = requests.get('https://en.wikipedia.org/w/api.php', params=req).json()
        if 'error' in result:
            raise Error(result['error'])
        if 'warnings' in result:
            print(result['warnings'])
        if 'query' in result:
            yield result['query']
        if 'continue' not in result:
            break
        lastContinue = result['continue']
