from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import boto3
import os
#from boto3.dynamodb.conditions import Key

aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
region = os.environ['REGION']
table_name = os.environ['TABLE_NAME']
code_name = os.environ['CODE_NAME']

host = ''
port = 8000

class MyHandler(SimpleHTTPRequestHandler):

    def getSecret(self):

        try:
            client = boto3.client('dynamodb', region_name=region, aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key)

            response = client.get_item(
                TableName=table_name,
                Key={
                    "code_name": { "S": code_name }
                }
            )
            
            # Check if the item was found
            #if 'Item' in response:
            #    secret_code = response['Item']['secret_code']
            #    response="The secret code for " + code_name + " is: " + secret_code
            #else:
            #    response="No item found with code_name " + code_name + " in table " table_name
            
            print(response)
            return str(response)

        except Exception as response:
            print(response)
            return "ERROR: " + str(response)


    def do_GET(self):
        if self.path == '/secret':
            response=self.getSecret()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(response,"utf-8"))
        elif self.path == '/health':
            self.send_response(200)
            self.end_headers()
            health="{status: healthy, container: " + os.environ['CONTAINER'] + ", project: " +os.environ['PROJECT'] + " }"
            self.wfile.write(bytes(health,"utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')



with TCPServer((host, port), MyHandler) as server:
    print(f'Serving on http://{host}:{port}')
    server.serve_forever()
