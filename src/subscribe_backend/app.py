import json, boto3, logging, re, os

logger = logging.getLogger()
logger.setLevel(logging.INFO)
sns_client = boto3.client('sns')

def isDomainAllowed(email):
  match = re.search(os.environ['EMAIL_WHITELIST_PATTERN'], email)
  return bool(match)

def lambda_handler(event, context):
    statusCode = 500
    message = "wrong payload"
    logging.info(f"event: {event}")
    email = json.loads(event["body"].replace("'", "\""))['email'] if "email" in event['body'] else ""
    if isDomainAllowed(email):
        logging.info(f"email: {email}, SNS_SUBSCRIBERS_ARN: {os.environ['SNS_SUBSCRIBERS_ARN']}")
        sns_client.subscribe(
            TopicArn=os.environ['SNS_SUBSCRIBERS_ARN'],
            Protocol='email',
            Endpoint=email
        )
        statusCode = 200
        message = "subscribed"

    return {
        "statusCode": statusCode,
        "headers": {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : "true"
        },
        "body": json.dumps({
            "message": message,
        }),
    }
