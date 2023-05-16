import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError
import os

class TTS:
    def __init__(self, voice_name='Joanna', region_name='us-west-2'):
        self.voice_name = voice_name
        self.region_name = region_name
        self.client = boto3.Session(
            aws_access_key_id='YOUR_KEY_ID',
            aws_secret_access_key='YOUR_SECRET_KEY',
            region_name=self.region_name).client('polly')

    def convert(self, text_input, save_path):
        try:
            response = self.client.synthesize_speech(Text=text_input, OutputFormat='mp3', VoiceId=self.voice_name)
            with open(save_path, 'wb') as f:
                f.write(response['AudioStream'].read())
        except (BotoCoreError, NoCredentialsError) as error:
            print(error)
            os.remove(save_path)  # Remove incomplete file in case of error
