"""
MinIO (S3-compatible) storage client for file operations.
"""

from typing import Optional
from minio import Minio
from minio.error import S3Error
from urllib.parse import urljoin

from .config import settings
from .utils import logger


class StorageClient:
    """Client for interacting with MinIO storage."""
    
    def __init__(self):
        """Initialize MinIO client."""
        self.client: Optional[Minio] = None
        self._connect()
        self._ensure_bucket()
    
    def _connect(self) -> None:
        """Establish connection to MinIO."""
        try:
            self.client = Minio(
                settings.minio_endpoint,
                access_key=settings.minio_access_key,
                secret_key=settings.minio_secret_key,
                secure=settings.minio_use_ssl,
                region=settings.minio_region
            )
            logger.info(f"Connected to MinIO: {settings.minio_endpoint}")
        except Exception as e:
            logger.error(f"Failed to connect to MinIO: {str(e)}")
            raise
    
    def _ensure_bucket(self) -> None:
        """Ensure the bucket exists, create if it doesn't."""
        try:
            if not self.client:
                raise RuntimeError("MinIO client not initialized")
            
            if not self.client.bucket_exists(settings.minio_bucket_name):
                self.client.make_bucket(settings.minio_bucket_name)
                logger.info(f"Created bucket: {settings.minio_bucket_name}")
            else:
                logger.info(f"Bucket exists: {settings.minio_bucket_name}")
        except S3Error as e:
            logger.error(f"Error ensuring bucket exists: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error ensuring bucket: {str(e)}")
            raise
    
    def upload_file(
        self,
        file_data: bytes,
        object_name: str,
        content_type: str = "application/octet-stream"
    ) -> str:
        """
        Upload a file to MinIO.
        
        Args:
            file_data: File content as bytes
            object_name: Object name (path) in the bucket
            content_type: MIME type of the file
            
        Returns:
            Public URL of the uploaded file
            
        Raises:
            RuntimeError: If upload fails
        """
        try:
            if not self.client:
                raise RuntimeError("MinIO client not initialized")
            
            from io import BytesIO
            
            # Upload file
            self.client.put_object(
                bucket_name=settings.minio_bucket_name,
                object_name=object_name,
                data=BytesIO(file_data),
                length=len(file_data),
                content_type=content_type
            )
            
            logger.info(f"Uploaded file: {object_name}")
            
            # Generate public URL
            url = self.get_public_url(object_name)
            return url
            
        except S3Error as e:
            logger.error(f"Error uploading file to MinIO: {str(e)}")
            raise RuntimeError(f"Failed to upload file: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error uploading file: {str(e)}")
            raise RuntimeError(f"Failed to upload file: {str(e)}")
    
    def get_public_url(self, object_name: str) -> str:
        """
        Generate public URL for an object.
        
        Args:
            object_name: Object name (path) in the bucket
            
        Returns:
            Public URL string
        """
        protocol = "https" if settings.minio_use_ssl else "http"
        base_url = f"{protocol}://{settings.minio_endpoint}"
        
        # Construct URL
        if settings.minio_bucket_name:
            url = f"{base_url}/{settings.minio_bucket_name}/{object_name}"
        else:
            url = f"{base_url}/{object_name}"
        
        return url
    
    def delete_file(self, object_name: str) -> bool:
        """
        Delete a file from MinIO.
        
        Args:
            object_name: Object name (path) in the bucket
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.client:
                raise RuntimeError("MinIO client not initialized")
            
            self.client.remove_object(
                bucket_name=settings.minio_bucket_name,
                object_name=object_name
            )
            
            logger.info(f"Deleted file: {object_name}")
            return True
            
        except S3Error as e:
            logger.error(f"Error deleting file from MinIO: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting file: {str(e)}")
            return False


# Global storage client instance
storage_client = StorageClient()

