import boto3, logging, os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

FILE_NAME = "subscribe.html"

def lambda_handler(event, context):
    with open(FILE_NAME, 'r') as file:
        data = file.read().replace("###URL###", os.environ['API_URL'])
    logging.info(f"Upload data from {FILE_NAME} to {os.environ['WEBSITE_BUCKET']}")
    s3 = boto3.resource("s3")
    s3.Object(os.environ['WEBSITE_BUCKET'], FILE_NAME).put(Body=data, ContentType='text/html')
