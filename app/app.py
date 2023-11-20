from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import boto3
import os
#from boto3.dynamodb.conditions import Key

with open('aws_creds.txt', 'r') as f:
    aws_access_key_id = f.readline().strip()
    aws_secret_access_key = f.readline().strip()
    region = f.readline().strip()
    table_name = f.readline().strip()
    code_name = f.readline().strip()

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
