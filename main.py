import base64
import os


def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    os.system('python run_spyder_infoworld.py')
    os.system('python run_spyder_devmozilla.py')
    
    return 'ok'