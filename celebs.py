import os

def get_celeb_info(dynamodb ,table_name, partition_key, face_id):
    item = dynamodb.query(table_name, partition_key, face_id)
    return item


#remove file extension (.jpg, .jpeg, .png)
def removeFileExtension(file):
    return os.path.splitext(file)[0]