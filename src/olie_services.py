"""Wrapper routines for I/O"""
import os
import tempfile
import uuid

from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient
from azure.storage.blob import ContainerClient, ContentSettings


class OlieServices:
    """Wrapper routines for I/O"""

    def __init__(self):
        credential = DefaultAzureCredential()
        self.sb_namespace = os.getenv('OlieServiceBusNamespace')
        self.sb_queue = os.getenv('OlieServiceBusQueue')

        self.sb_client = ServiceBusClient(self.sb_namespace, credential)
        self.sb_reader = self.sb_client.get_queue_receiver(self.sb_queue, max_wait_time=300)

        blob_account = os.getenv('OlieBlobAccount')
        blob_container = os.getenv('OlieBlobInContainer')
        self.container_in_client = ContainerClient(blob_account, blob_container, credential)

        blob_container = os.getenv('OlieBlobOutContainer')
        self.container_out_client = ContainerClient(blob_account, blob_container, credential)

    @staticmethod
    def get_local_file(remote_path: str) -> str:
        """Create a filename in the temp folder with the passed filename"""
        temp_dir = tempfile.gettempdir()
        filename = os.path.basename(remote_path)

        result = f"{temp_dir}/{filename}"
        return result

    @staticmethod
    def get_temp_file(extension: str) -> str:
        """Create a filename in the temp folder with the passed extension"""
        temp_dir = tempfile.gettempdir()
        file_uuid = str(uuid.uuid4())

        result = f"{temp_dir}/{file_uuid}{extension}"
        return result

    @staticmethod
    def delete_file(filepath: str):
        """Delete a file"""
        os.remove(filepath)

    def download_blob(self, source: str, destination: str):
        """Download a blob to a local file"""
        # Create the blob_client object
        blob_client = self.container_in_client.get_blob_client(source)

        # Download the file
        with open(file=destination, mode="wb") as sample_blob:
            download_stream = blob_client.download_blob()
            sample_blob.write(download_stream.readall())

    def upload_blob(self, source: str, destination: str, mime: str):
        """Upload a local file to blob storage"""
        # Create the blob_client object
        blob_client = self.container_out_client.get_blob_client(destination)

        # Specify the headers
        content_settings = ContentSettings(content_type=mime,
                                           cache_control="public, max-age=604800")

        # Upload the file
        with open(file=source, mode="rb") as data:
            blob_client.upload_blob(data, overwrite=True, content_settings=content_settings)
    