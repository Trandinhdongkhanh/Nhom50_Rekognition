import boto3

class Client():
    def __init__(self, service, access_key_id, secret_access_key, session_token, region):
        self.service = service
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.session_token = session_token
        self.region = region
    def init_client(self):
        return boto3.client(
            service_name=self.service,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            aws_session_token=self.session_token,
            region_name=self.region
        )