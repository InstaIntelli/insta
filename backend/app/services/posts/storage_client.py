"""
MinIO (S3-compatible) storage client for file operations.
Uses main app configuration.
"""

from typing import Optional
from minio import Minio
from minio.error import S3Error

from app.core.config import settings
import logging

logger = logging.getLogger("posts_service")


class PostsStorageClient:
    """Client for interacting with MinIO storage."""
    
    def __init__(self):
        """Initialize MinIO client."""
        self.client: Optional[Minio] = None
        self._connect()
        self._ensure_bucket()
    
    def _connect(self) -> None:
        """Establish connection to MinIO."""
        try:
            if not settings.MINIO_ENDPOINT:
                raise ValueError("MINIO_ENDPOINT not configured")
            if not settings.MINIO_ACCESS_KEY:
                raise ValueError("MINIO_ACCESS_KEY not configured")
            if not settings.MINIO_SECRET_KEY:
                raise ValueError("MINIO_SECRET_KEY not configured")
            
            # Parse endpoint (remove http:// or https:// if present)
            endpoint = settings.MINIO_ENDPOINT.replace("http://", "").replace("https://", "")
            
            self.client = Minio(
                endpoint,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=False  # Use False for local development
            )
            logger.info(f"Connected to MinIO: {endpoint}")
        except Exception as e:
            logger.error(f"Failed to connect to MinIO: {str(e)}")
            raise
    
    def _ensure_bucket(self) -> None:
        """Ensure the bucket exists, create if it doesn't."""
        try:
            if not self.client:
                raise RuntimeError("MinIO client not initialized")
            
            bucket_name = settings.MINIO_BUCKET_NAME or "instaintelli"
            
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                logger.info(f"Created bucket: {bucket_name}")
            else:
                logger.info(f"Bucket exists: {bucket_name}")
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
            
            bucket_name = settings.MINIO_BUCKET_NAME or "instaintelli"
            
            # Upload file
            self.client.put_object(
                bucket_name=bucket_name,
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
        endpoint = settings.MINIO_ENDPOINT.replace("http://", "").replace("https://", "")
        bucket_name = settings.MINIO_BUCKET_NAME or "instaintelli"
        
        # Construct URL (assuming MinIO is accessible at the endpoint)
        url = f"http://{endpoint}/{bucket_name}/{object_name}"
        
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
            
            bucket_name = settings.MINIO_BUCKET_NAME or "instaintelli"
            
            self.client.remove_object(
                bucket_name=bucket_name,
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
posts_storage_client = PostsStorageClient()

