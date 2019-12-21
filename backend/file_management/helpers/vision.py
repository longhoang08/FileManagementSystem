import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account


def generate_image_tag(file_name):
    
    credentials = service_account.Credentials.from_service_account_file(
    'key.json')
    client = vision.ImageAnnotatorClient(credentials=credentials)

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image files
    response = client.label_detection(image=image)
    labels = response.label_annotations
    lb = [label.description for label in labels]
    return lb