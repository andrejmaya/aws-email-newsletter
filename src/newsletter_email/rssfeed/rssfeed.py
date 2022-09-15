import feedparser, importlib

class rssfeed:
  """
    title: str
    link: str
    entries: []  
  """

  def __init__(self, feed, cutoff_date):
    self.link = feed['link']
    feed_output = feedparser.parse(self.link)
    self.title = feed_output.feed.title
    self.entries = []

    for entry in feed_output.entries:
      module = importlib.import_module('rssfeed.'+feed['class_name'])
      class_ = getattr(module, feed['class_name'])
      entry_obj = class_(entry)
      self.entries.append(entry_obj) if entry_obj.published > cutoff_date else None