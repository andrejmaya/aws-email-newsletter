from datetime import datetime, date

class rssfeed_json_entry:
  """
    title: str
    link: str
    published: date  
  """

  def __init__(self, entry):
    #e.g. entry['startDateTime'] == "2022-10-06T20:39:20+00:00"
    startDateTime = entry['startDateTime'] if 'startDateTime' in entry else "1970-01-01T00:00:00+00:00"

    self.title = entry['headline']
    self.link = entry['headlineUrl']
    self.level = entry['expertise']
    self.published = datetime.strptime(startDateTime, '%Y-%m-%dT%X%z').date()
