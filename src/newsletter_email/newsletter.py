from rssfeed_xml.rssfeed_xml import *
from rssfeed_json.rssfeed_json import *
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
import boto3, os, logging, sys, json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

with open("rssfeed_xml/feedlist.json", "r") as feed_list_xml_f:
    feed_list_xml = json.load(feed_list_xml_f)
with open("rssfeed_json/feedlist.json", "r") as feed_list_json_f:
    feed_list_json = json.load(feed_list_json_f)


def main(event, context):
    ses_client = boto3.client('ses')
    subscriptions = get_subscribers()
    cutoff_days = os.environ['CUTOFF_DAYS'] if is_local_test() == False else 7
    cutoff_date = (datetime.now()-timedelta(days=int(cutoff_days))).date()
    logging.info(f"subscriptions:{subscriptions}")

    feeds = [rssfeed_xml(feed, cutoff_date) for feed in feed_list_xml]
    feeds += [rssfeed_json(feed, cutoff_date) for feed in feed_list_json]

    mail_body_part = render_mail(
        feeds=feeds,
        template="body.jinja"
    )

    for subscriber in subscriptions:
        endpoint = subscriber['Endpoint']

        mail_body = mail_body_part + render_mail(
            SubscriptionArn=subscriber['SubscriptionArn'],
            template="footer.jinja"
        )

        logging.info(f"endpoint:{endpoint}, mail_body:{mail_body}")
        if is_local_test() == False:
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
    if is_local_test() == False:
        response = sns_client.list_subscriptions_by_topic(
            TopicArn=os.environ['SNS_SUBSCRIBERS_ARN']
        )
        subscriptions = get_active_subscribers(response['Subscriptions'])
        while "NextToken" in response:
            response = sns_client.list_subscriptions_by_topic(
                TopicArn=os.environ['SNS_SUBSCRIBERS_ARN'],
                NextToken=response["NextToken"]
            )
            subscriptions.extend(
                get_active_subscribers(response['Subscriptions']))
    else:
        subscriptions = [{'SubscriptionArn': '12345',
                          'Endpoint': 'johndoe@example.com'}]
    return subscriptions


def get_active_subscribers(resp_subscriptions):
    return [obj for obj in resp_subscriptions if obj['SubscriptionArn'].startswith('arn:aws:sns')]


def render_mail(**kwargs):
    environment = Environment(loader=FileSystemLoader("email_template/"))
    template = environment.get_template(kwargs.get("template"))

    return template.render(
        kwargs,
        Region=boto3.session.Session().region_name
    )


def is_local_test():
    if 'LOCAL_TEST' in os.environ and os.environ['LOCAL_TEST'] == 'true':
        return True
    else:
        return False


if __name__ == "__main__":
    main({}, {})
