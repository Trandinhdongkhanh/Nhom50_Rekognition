import application
from client import Client
from credentials import *
from rekognitionAPI import Rekognition
from s3 import S3
from application import App
from dynamodb import DynamoDB
import celebs

def set_up(collection_id, bucket_name):
    client = Client('rekognition', access_key_id, secret_access_key, session_token, region)
    s3 = S3('s3', access_key_id, secret_access_key, session_token, region)
    rekApi = Rekognition(client.init_client())
    rekApi.delete_collection(collection_id)
    rekApi.create_collection(collection_id)
    rekApi.list_collection()
    bucket = s3.resource().Bucket(bucket_name)
    summaries = bucket.objects.all()
    for summary in summaries:
        rekApi.index_faces(collection_id, summary.bucket_name, summary.key)
    rekApi.list_faces(collection_id)

def main():
    client = Client('rekognition', access_key_id, secret_access_key, session_token, region)
    s3 = S3('s3', access_key_id, secret_access_key, session_token, region)
    dynamodb = DynamoDB('dynamodb', access_key_id, secret_access_key, session_token, region)
    bucket_name = 'tddk-bucket'
    table = 'celebs'
    partition_key = 'face_id'       #primary key
    collection_id = 'celebrities'
    # img = 'Images/celeb1.jpg'

    # set_up(collection_id, bucket_name)      #run this once, then comment it

    application.CLIENT = client.init_client()
    application.BUCKET = bucket_name
    application.S3_RESOURCE = s3.resource()
    application.TABLE = table
    application.DynamoDB = dynamodb
    application.COLLECTION_ID = collection_id
    application.PARTITION_KEY = partition_key

    app = App()
    app.win.mainloop()

if __name__ == "__main__":
    main()