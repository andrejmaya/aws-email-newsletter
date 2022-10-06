from rssfeed_xml.rssfeed_xml_entry import *

class rssfeed_xml_entry_whatsnew(rssfeed_xml_entry):
  """
    product: str
  """
  def __init__(self, entry):
    super().__init__(entry)
    self.product = entry['tags'][0].term.split(',')[0].replace('general:products/','').replace('-',' ')