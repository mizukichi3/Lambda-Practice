import boto3
import pyminizip
import tempfile
import os

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    for rec in event['Records']:
      filename = rec['s3']['object']['key']
      obj = s3.Object(rec['s3']['bucket']['name'], filename)
      response = obj.get()
      tmpdir = tempfile.TemporaryDirectory()
      fp = open(tmpdir.name + '/' + filename, 'wb')
      fp.write(response['Body'].read())
      fp.close();

# 暗号化
zipname = tempfile.mkstemp(suffix='zip')[1]
os.chdir(tmpdir.name)
pyminizip.compress(filename, './', zipname, 'mypassword', 0)

# S3にアップロード
obj = s3.Object('lambda-practice-read', filename + '.zip')
response = obj.put(
    Body=open(zipname, 'rb')
)

tmpdir.cleanup()
os.unlink(zipname)

# 以下、テスト用のプログラム
import json
if __name__ == "__main__":
    data = '''
{
  "Records": [
    {
      "s3": {
        "Object": {
          "eTag": "hoge",
          "sequencer": "fuga",
          "key": "icon.png",
          "size": "1024"
        },
      "bucket": {
        "arn": "arn:aws:s3:::lambda-practice-read",
        "name": "lambda-practice-read",
        "ownerIdentity" : {
          "principalId": "EXAMPLE"
        }
