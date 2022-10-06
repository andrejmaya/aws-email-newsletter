from datetime import datetime, date

class rssfeed_xml_entry:
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
    #e.g. Thu, 06 Oct 2022 18:44:38 +0000
    self.published = datetime.strptime(entry['published'], '%a, %d %b %Y %X %z').date()
  
