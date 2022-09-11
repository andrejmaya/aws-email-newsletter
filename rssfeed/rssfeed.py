import feedparser, importlib, logging
from datetime import datetime, timedelta

class rssfeed:
  """
    title: str
    link: str
    entries: []  
  """

  def __init__(self, feed):
    self.link = feed['link']
    feed_output = feedparser.parse(self.link)
    self.title = feed_output.feed.title
    self.entries = []

    for entry in feed_output.entries:
      module = importlib.import_module('rssfeed.'+feed['class_name'])
      class_ = getattr(module, feed['class_name'])
      #logger.debug(f"instantiating class_: {class_} for feed: {feed}")
      self.entries.append(
        class_(entry)
      )

  def get_entries_for_last_x_days(self, cutoff_days=7):
    """
      Return entries after cutoff date
    """
    cutoff_date = (datetime.now()-timedelta(days=cutoff_days)).date()

    out = "<table>" + self.entries[0].get_header()
    for entry in self.entries:
      if entry.published > cutoff_date:
        out += entry.to_string()
    
    return out+"</table>"