import boto3
import pyminizip
import tempfile
import os

filename = 'icon.png'
s3 = boto3.resource('s3')

# ファイルの読み込み
obj = s3.object('lambra-practice-read', filename)
response = obj.get()
tmpdir = tempfile.TemporaryDirectory()
fp = open(tmpdir.name + '/' + filename, 'wb')
fp.write(response['Body'].read())
fp.close();

# 暗号化
zipname = tempfile.mkstemp(suffix='zip')[1]
os.chdir(tmpdir.name)
pyminizip.compress(filename, zipname, 'mypassword', 0)

# S3にアップロード
obj = s3.object('lambra-practice-read', filename + '.zip')
response = obj.put(
    Body=open(zipname, 'rb')
)

tmpdir.cleanup()
os.unlink(zipname)
