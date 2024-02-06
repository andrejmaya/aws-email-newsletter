from rssfeed_xml.rssfeed_xml_entry import *
import re


class rssfeed_xml_entry_whatsnew(rssfeed_xml_entry):
    """
    product: str
  """

    def isAddable(self, cutoff_date):
        return (
            super().isAddable(cutoff_date)
            and not re.compile('govcloud').search(self.product.lower())
            and not re.compile('now available in').search(self.title.lower())
        )


    def __init__(self, entry):
        super().__init__(entry)
        self.product = ''
        if 'tags' in entry and len(entry['tags']) > 0:
            entry_term = entry['tags'][0].term.split(',')[0]
            if '/' in entry_term:
                entry_term = entry_term.split('/')[-1]
            self.product = entry_term.replace('-', ' ').rstrip()
