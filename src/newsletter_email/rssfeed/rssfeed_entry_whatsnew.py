from rssfeed.rssfeed_entry import *

class rssfeed_entry_whatsnew(rssfeed_entry):
  """
    product: str
  """
  def __init__(self, entry):
    super().__init__(entry)
    self.product = entry['tags'][0].term.split(',')[0].replace('general:products/','').replace('-',' ')