from rssfeed_xml.rssfeed_xml_entry import *


class rssfeed_xml_entry_whatsnew(rssfeed_xml_entry):
    """
    product: str
  """

    def __init__(self, entry):
        super().__init__(entry)
        self.product = ''
        if 'tags' in entry:
            entry_term = entry['tags'][0].term.split(',')[0]
            if '/' in entry_term:
                entry_term = entry_term.split('/')[-1]
            self.product = entry_term.replace('-', ' ').rstrip()