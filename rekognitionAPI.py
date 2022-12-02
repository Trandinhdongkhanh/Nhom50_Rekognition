import json
class Rekognition():
    def __init__(self, client):
        self.client = client

    def recognize_celebrities(self, img):
        response = self.client.recognize_celebrities(
            Image={
                'Bytes': ImageConverter.transfer_bytes(img)
            }
        )
        print('Detected faces for ' + img)
        for celebrity in response['CelebrityFaces']:
            print('Name: ' + celebrity['Name'])
            print('Id: ' + celebrity['Id'])
            print('KnownGender: ' + celebrity['KnownGender']['Type'])
            print('Smile: ' + str(celebrity['Face']['Smile']['Value']))
            print('Position:')
            print('   Left: ' + '{:.2f}'.format(celebrity['Face']['BoundingBox']['Height']))
            print('   Top: ' + '{:.2f}'.format(celebrity['Face']['BoundingBox']['Top']))
            print('Info')
            for url in celebrity['Urls']:
                print('   ' + url)
            print
            return json.dumps(response, indent=3)

    def compare_faces(self, source_img, target_img):
        print("Comparing '" + source_img + "' with '" + target_img + "'")
        response = self.client.compare_faces(
            SourceImage={
                'Bytes': ImageConverter.transfer_bytes(source_img)
            },
            TargetImage={
                'Bytes': ImageConverter.transfer_bytes(target_img),
            },
            SimilarityThreshold=70,
            QualityFilter='AUTO'
        )
        print(response)
        for faceMatch in response['FaceMatches']:
            position = faceMatch['Face']['BoundingBox']
            similarity = str(faceMatch['Similarity'])
            print('The face at ' +
                  str(position['Left']) + ' ' +
                  str(position['Top']) +
                  ' matches with ' + similarity + '% confidence')
        return json.dumps(response, indent=3)

    def compare_faces_S3(self, source_img, target_img, bucket):
        print("Comparing '" + source_img +"' with '" + target_img + "'" )
        response = self.client.compare_faces(
            SourceImage={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': source_img,
                }
            },
            TargetImage={
                'Bytes': ImageConverter.transfer_bytes(target_img),
            },
            SimilarityThreshold=70,
            QualityFilter='AUTO'
        )
        print(response)
        for faceMatch in response['FaceMatches']:
            position = faceMatch['Face']['BoundingBox']
            similarity = str(faceMatch['Similarity'])
            print('The face at ' +
                   str(position['Left']) + ' ' +
                   str(position['Top']) +
                   ' matches with ' + similarity + '% confidence')
        return json.dumps(response, indent=3)

    #user define API
    def recognize_celebrities_v2(self, s3_resource, bucket_name, target_img):
        result = []
        bucket = s3_resource.Bucket(bucket_name)
        summaries = bucket.objects.all()
        for summary in summaries:
            print(summary)
            response = self.client.compare_faces(
                SourceImage={
                    'S3Object':{
                        'Bucket': bucket_name,
                        'Name': summary.key
                    }
                },
                TargetImage={
                    'Bytes': ImageConverter.transfer_bytes(target_img)
                },
                SimilarityThreshold=70,
                QualityFilter='AUTO'
            )
            for face in response['FaceMatches']:
                if (face['Similarity'] > 70):
                    result.append(summary.key)
        return result

    def detect_labels(self, img):
        response = self.client.detect_labels(
            Image={
                'Bytes': ImageConverter.transfer_bytes(img)
            }
        )
        return json.dumps(response, indent=3)

    def create_collection(self, collection_id):
        print('Creating collection...')
        response = self.client.create_collection(
            CollectionId=collection_id
        )

    def list_collection(self):
        print('Listing collection...')
        response = self.client.list_collections(
            MaxResults=5
        )
        print(response['CollectionIds'])
        print('Done !')
        print()

    def delete_collection(self, collection_id):
        print("Deleting collection '"  + collection_id +"'")
        response = self.client.delete_collection(
            CollectionId=collection_id
        )

    def list_faces(self, collection_id):
        print("Listing faces in '" + collection_id + "'")
        response = self.client.list_faces(
            CollectionId=collection_id,
            MaxResults=50
        )
        for face in response['Faces']:
            print('ExternalImageId: ' + face['ExternalImageId'])
            print('FaceId: ' + face['FaceId'])
            print('Confidence: ' + str(face['Confidence']))
            print()
        print('Done !')

    def search_faces_by_image(self, collection_id, bucket, name):
        print('Searching...')
        response = self.client.search_faces_by_image(
            CollectionId=collection_id,
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': name
                }
            },
            QualityFilter='AUTO',
            FaceMatchThreshold=70
        )
        face_id = None
        print('SearchedFaceConfidence: ' + str(response['SearchedFaceConfidence']))
        for face in response['FaceMatches']:
            print('Similarity: ' + str(face['Similarity']))
            print('FaceId: ' + face['Face']['FaceId'])
            face_id = face['Face']['FaceId']
            print('ExternalImageId: ' + face['Face']['ExternalImageId'])
            print('Confidence: ' + str(face['Face']['Confidence']))
        return face_id

    def index_faces(self, collection_id, bucket, name):
        print('Adding face to collection...')
        response = self.client.index_faces(
            CollectionId=collection_id,
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': name
                }
            },
            ExternalImageId=name,
            QualityFilter='AUTO'
        )
        for face in response['FaceRecords']:
            print('FaceId: ' + face['Face']['FaceId'])
            print('ExternalImageId: ' + face['Face']['ExternalImageId'])
        print('------------------------------------')

    def detect_text(self, img):
        response = self.client.detect_text(
            Image={
                'Bytes': ImageConverter.transfer_bytes(img)
            }
        )
        return json.dumps(response, indent=3)       #pretty_print json

    def facial_analysis(self, img):
        response = self.client.detect_faces(
            Image={
                'Bytes': ImageConverter.transfer_bytes(img)
            },
            Attributes= ['ALL']
        )
        return json.dumps(response, indent=3)

class ImageConverter():
    def __init__(self):
        pass

    @staticmethod
    def transfer_bytes(img):
        with open(img, 'rb') as source_img:
            source_bytes = source_img.read()
        return source_bytes