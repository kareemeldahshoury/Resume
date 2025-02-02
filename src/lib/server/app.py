from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import boto3
from botocore.exceptions import ClientError
import logging
from mangum import Mangum


app = Flask(__name__, static_folder="static", static_url_path="/")
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# AWS DynamoDB Set up

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table_name = "VisitorCount"
table = None # For the error?

try:
  dynamodb.meta.client.describe_table(TableName=table_name)
  table = dynamodb.Table(table_name)
except dynamodb.meta.client.exceptions.ResourceNotFoundException:
  table = dynamodb.create_table(
    TableName = table_name,
    KeySchema=[
      {"AttributeName": "visitors", "KeyType": "HASH"}
    ],
    AttributeDefinitions=[
      {"AttributeName": "visitors", "AttributeType": "S"} #JSON sends numbers as strings so the table should be recieving a string, might cause error
    ],
    ProvisionedThroughput={
      "ReadCapacityUnits": 1,
      "WriteCapacityUnits": 1
    },
  )
  table.wait_until_exists()


@app.route("/api", methods=["GET"])
def visit():
  # print(request.cookies)
  # if request.cookies.get("visited"):
  #   print("Visitor has already been counted.")

  #   try:
  #     response = table.get_item(Key={"visitors": "visitor_count"})
  #     count = response.get("Item", {}).get("count", 0)
  #     return jsonify({"visits": count})
  #   except ClientError as err:
  #     return jsonify({"error": str(err)}), 500

  try:
    response = table.get_item(Key={"visitors": "visitor_count"})
    count = response.get("Item", {}).get("count", 0)

    new_count = count + 1
    table.put_item(Item={"visitors": "visitor_count", "count": new_count})

    # response = make_response(jsonify({"visits": new_count}))
    # response.set_cookie("visited", "true", max_age=30, samesite='Lax')  # Cookie expires in 1 hour
    # print(f"Visitor count (backend): {new_count}")
    print(request.cookies)
    return response
  except ClientError as err:
        return jsonify({"error": str(err)}), 500

  
lambda_handler = Mangum(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
