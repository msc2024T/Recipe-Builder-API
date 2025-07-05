from .models import Image
from azure.storage.blob import BlobServiceClient, ContentSettings, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
from django.conf import settings
from io import BytesIO
import environ
import uuid

# Initialize environment variables
env = environ.Env()


class AzureBlobService:
    def __init__(self):
        self.connection_string = env('AZURE_BLOB_CONNECTION_STRING')
        self.client = BlobServiceClient.from_connection_string(
            self.connection_string)
        self.container = self.client.get_container_client(
            env('AZURE_STORAGE_CONTAINER_NAME'))

    def upload(self, blob_name, file, content_type="application/octet-stream"):
        blob_client = self.container.get_blob_client(blob_name)
        blob_client.upload_blob(
            file,  content_settings=ContentSettings(content_type=content_type))
        return blob_client.url

    def delete(self, blob_name):
        self.container.delete_blob(blob_name)

    def generate_sas_url(self, blob_name, content_disposition=None, expiry_minutes=15):
        blob_client = self.container.get_blob_client(blob_name)

        # Create SAS token with content disposition
        sas_token = generate_blob_sas(
            account_name=env('AZURE_STORAGE_ACCOUNT_NAME'),
            container_name=env('AZURE_STORAGE_CONTAINER_NAME'),
            blob_name=blob_name,
            account_key=env('AZURE_STORAGE_KEY'),
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(minutes=expiry_minutes),
            content_disposition=content_disposition  # Add content disposition
        )

        # Construct the full URL with SAS token
        return f"{blob_client.url}?{sas_token}"


class ImageService:
    def __init__(self, user):
        self.azure_blob_service = AzureBlobService()
        self.user = user

    def upload_image(self, image_file, user):
        if not image_file:
            raise ValueError("No image file provided")

        # chek file size is less than 5MB
        if image_file.size > 5 * 1024 * 1024:  #
            raise ValueError("Image file size exceeds 5MB limit")

        # get the file extension
        if not image_file.name:
            raise ValueError("Image file name is required")
        if '.' not in image_file.name:
            raise ValueError("Image file name must have an extension")

        extension = image_file.name.split('.')[-1].lower()

        # Create a unique blob name
        blob_name = f"{str(uuid.uuid4())}.{extension}"

        # Upload the image to Azure Blob Storage
        url = self.azure_blob_service.upload(blob_name, image_file)

        # Save the image metadata to the database
        image = Image.objects.create(
            name=blob_name,
            extension=image_file.name.split('.')[-1],
            uploaded_by=user
        )
        return image

    def get_image_url(self, image_id):
        try:
            image = Image.objects.get(id=image_id)
            blob_name = f"{image.name}"
            return self.azure_blob_service.generate_sas_url(blob_name)
        except Image.DoesNotExist:
            raise ValueError("Image not found")

    def delete_image(self, image_id):
        try:
            image = Image.objects.get(id=image_id)
            self.azure_blob_service.delete(
                f"images/{image.uploaded_by.id}/{image.name}")
            image.delete()
        except Image.DoesNotExist:
            raise ValueError("Image not found")
