from rssfeed_xml.rssfeed_xml_entry import *
from dateutil import parser
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class rssfeed_xml_entry_yt(rssfeed_xml_entry):
    """
      title: str
      summary: str
      link: str
      published: date
    """

    def isAddable(self, cutoff_date):
        return super().isAddable(cutoff_date)

    def __init__(self, entry):
        self.title = entry['title']
        self.summary = entry['summary']
        self.link = entry['link']
        try:
            self.published = parser.parse(entry['published']).date()
        except ValueError:
            logging.error(f"Invalid date string:{entry['published']}")
