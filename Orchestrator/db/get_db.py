import boto3
import json
import logging
import os
logging.basicConfig(level=logging.DEBUG)
logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def get_item_from_dynamodb(rut):
  # removing unwanted new lines or tab
  rut = rut.strip('\n').strip('\t')
  logging.info("Querying database using rut %s", rut)
  dynamodb = boto3.client("dynamodb", region_name=os.environ.get("DATABASE_AWS_REGION"))
  found_customer = dynamodb.get_item(TableName=os.environ.get("DYNAMODB_TABLE"), Key={os.environ.get("TABLE_PARTITION_KEY"):{'S':os.environ.get("TABLE_PARTITION_VALUE")}, 'rut':{'S': str(rut)}})
  logging.debug("Item found in Database for rut %s: %s", rut, found_customer)
  return found_customer['Item']