import json
from rssfeed.rssfeed import *

feed_list = [
  {
    'link':'https://aws.amazon.com/about-aws/whats-new/recent/feed/',
    'class_name':'rssfeed_entry_whatsnew',
  },
  {
    'link':'https://aws.amazon.com/blogs/aws/feed/',
    'class_name':'rssfeed_entry',
  },
  {
    'link':'https://aws.amazon.com/blogs/security/feed/',
    'class_name':'rssfeed_entry',
  },
  {
    'link':'https://aws.amazon.com/blogs/architecture/feed/',
    'class_name':'rssfeed_entry',
  },
  {
    'link':'https://aws.amazon.com/security/security-bulletins/rss/feed/',
    'class_name':'rssfeed_entry',
  }
]

feed = rssfeed(feed_list[0])
out = feed.get_entries_for_last_x_days()
print(out)

#for feed_item in feed_list:
#  feed = rssfeed(feed_item)