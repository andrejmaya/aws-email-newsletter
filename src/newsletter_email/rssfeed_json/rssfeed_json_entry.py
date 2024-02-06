from dateutil import parser
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class rssfeed_json_entry:
  """
    title: str
    link: str
    published: date
  """
  def isAddable(self, cutoff_date):
     return self.published > cutoff_date

  def __init__(self, entry, feed):
    #e.g. entry['startDateTime'] == "2022-10-06T20:39:20+00:00"
    logging.info(f"rssfeed_json_entry:{entry}")
    startDateTime = entry['startDate'] if 'startDate' in entry else "1970-01-01T00:00:00+00:00"

    self.title = entry['headline']
    self.link = entry['headlineUrl']
    self.level = entry['expertise'] if 'expertise' in entry else "unknown"
    try:
        self.published = parser.parse(startDateTime).date()
    except ValueError:
        logging.error(f"Invalid date string:{startDateTime}")


