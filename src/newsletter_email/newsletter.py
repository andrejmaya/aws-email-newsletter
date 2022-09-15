from rssfeed.rssfeed import *
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
import boto3, os, logging, sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)

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

def main(event, context):
  ses_client = boto3.client('ses')
  subscriptions = get_subscribers()
  cutoff_date = (datetime.now()-timedelta(days=int(os.environ['CUTOFF_DAYS']))).date()
  logging.info(f"subscriptions:{subscriptions}")
  
  feeds = [rssfeed(feed, cutoff_date) for feed in feed_list]

  for subscriber in subscriptions:
    endpoint = subscriber['Endpoint']

    mail_body = render_mail(feeds, subscriber['SubscriptionArn'])
    logging.info(f"endpoint:{endpoint}, mail_body:{mail_body}")
    response = ses_client.send_email(
        Source=os.environ['EMAIL_SENDER'],
        Destination={
            'ToAddresses': [
                endpoint,
            ]
        },
        Message={
            'Subject': {
                'Data': 'AWS Roadmap Items of Interest',
            },
            'Body': {
                'Html': {
                    'Data': mail_body,
                    'Charset': 'UTF-8'
                }
            }
        }
    )

def get_subscribers():
  sns_client = boto3.client('sns')
  response = sns_client.list_subscriptions_by_topic(
      TopicArn=os.environ['SNS_SUBSCRIBERS_ARN']
  )
  subscriptions = get_active_subscribers(response['Subscriptions'])
  while "NextToken" in response:
      response = sns_client.list_subscriptions_by_topic(
          TopicArn=os.environ['SNS_SUBSCRIBERS_ARN'],
          NextToken=response["NextToken"]
      )  
      subscriptions.extend(get_active_subscribers(response['Subscriptions']))
  return subscriptions

def get_active_subscribers(resp_subscriptions):
  return [obj for obj in resp_subscriptions if obj['SubscriptionArn'].startswith('arn:aws:sns')]

def render_mail(feeds, subscriptionArn):
  environment = Environment(loader=FileSystemLoader("email_template/"))
  template = environment.get_template("template.jinja")

  return template.render(
    feeds=feeds,
    SubscriptionArn=subscriptionArn,
    Region=boto3.session.Session().region_name
  )

if __name__ == "__main__":
    main({},{})