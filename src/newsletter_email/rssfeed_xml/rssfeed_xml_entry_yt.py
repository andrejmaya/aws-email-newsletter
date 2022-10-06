from datetime import datetime, date

class rssfeed_xml_entry_yt:
  """
    title: str
    summary: str
    link: str
    published: date  
  """

  def __init__(self, entry):
    self.title = entry['title']
    self.summary = entry['summary']
    self.link = entry['link']
    #e.g. 2022-10-06T20:39:20+00:00
    self.published = datetime.strptime(entry['published'], '%Y-%m-%dT%X%z').date()
  
