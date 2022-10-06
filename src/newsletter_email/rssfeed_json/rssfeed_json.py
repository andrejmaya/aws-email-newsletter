import importlib

class rssfeed_json:
  """
    title: str
    link: str
    entries: []  
  """

  def __init__(self, feed, cutoff_date):
    self.link = feed['link']
    http = urllib3.PoolManager()
    resp = http.request('GET', self.link)

    resp = json.loads(resp.data.decode('utf-8'))

    
    self.entries = []

    for entry in resp['items']:
      module = importlib.import_module('rssfeed_json.'+feed['class_name'])
      class_ = getattr(module, feed['class_name'])
      entry_obj = class_(entry['item']['additionalFields'])
      self.entries.append(entry_obj) if entry_obj.published > cutoff_date else None