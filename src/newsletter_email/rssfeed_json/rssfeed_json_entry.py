from datetime import datetime, date
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class rssfeed_json_entry:
  """
    title: str
    link: str
    published: date
  """

  def __init__(self, entry):
    #e.g. entry['startDateTime'] == "2022-10-06T20:39:20+00:00"
    logging.info(f"rssfeed_json_entry:{entry}")
    startDateTime = entry['startDate'] if 'startDate' in entry else "1970-01-01T00:00:00+00:00"

    self.title = entry['headline']
    self.link = entry['headlineUrl']
    self.level = entry['expertise']
    if "-" in startDateTime:
      self.published = datetime.strptime(startDateTime,'%d-%b-%y').date()
    elif "," in startDateTime:
      self.published = datetime.strptime(startDateTime,'%b %d, %Y').date()
    else:
      self.published = datetime.strptime('01-01-70','%d-%m-%y').date()
      raise Exception(f"unknown date format: {startDateTime}")

