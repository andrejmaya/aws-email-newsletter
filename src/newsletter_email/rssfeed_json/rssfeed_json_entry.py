from datetime import datetime, date

class rssfeed_json_entry:
  """
    title: str
    link: str
    published: date  
  """

  def __init__(self, entry):
    self.title = entry['headline']
    self.headllinkineUrl = entry['headlineUrl']
    #e.g. 2022-10-06T20:39:20+00:00
    self.published = datetime.strptime(entry['startDateTime'], '%Y-%m-%dT%X%z').date()
  
