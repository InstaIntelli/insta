"""
Profile Picture Storage Service
Handles profile picture uploads to MinIO with fast access
"""

from minio import Minio
from minio.error import S3Error
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class ProfileStorageClient:
    """Client for storing profile pictures in MinIO"""
    
    def __init__(self):
        self.client: Minio = None
        self.bucket_name = "instaintelli-media"  # Same bucket as posts
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize MinIO client"""
        try:
            if settings.MINIO_ENDPOINT and settings.MINIO_ACCESS_KEY and settings.MINIO_SECRET_KEY:
                self.client = Minio(
                    settings.MINIO_ENDPOINT,
                    access_key=settings.MINIO_ACCESS_KEY,
                    secret_key=settings.MINIO_SECRET_KEY,
                    secure=False  # Use HTTP for local development
                )
                self._ensure_bucket()
                logger.info("✅ Profile storage client initialized")
            else:
                logger.warning("⚠️ MinIO credentials not configured")
        except Exception as e:
            logger.error(f"Failed to initialize MinIO client: {str(e)}")
            self.client = None
    
    def _ensure_bucket(self):
        """Ensure bucket exists"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Created bucket: {self.bucket_name}")
        except S3Error as e:
            logger.error(f"Error ensuring bucket: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error ensuring bucket: {str(e)}")
            raise
    
    def upload_file(
        self,
        file_data: bytes,
        object_name: str,
        content_type: str = "image/jpeg"
    ) -> str:
        """
        Upload profile picture to MinIO
        
        Args:
            file_data: File content as bytes
            object_name: Object name (path) in the bucket
            content_type: MIME type of the file
            
        Returns:
            Public URL of the uploaded file
        """
        try:
            if not self.client:
                raise RuntimeError("MinIO client not initialized")
            
            from io import BytesIO
            
            # Upload file
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=BytesIO(file_data),
                length=len(file_data),
                content_type=content_type
            )
            
            logger.info(f"Uploaded profile picture: {object_name}")
            
            # Generate public URL (fast access)
            url = self.get_public_url(object_name)
            return url
            
        except S3Error as e:
            logger.error(f"Error uploading profile picture: {str(e)}")
            raise RuntimeError(f"Failed to upload profile picture: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error uploading profile picture: {str(e)}")
            raise RuntimeError(f"Failed to upload profile picture: {str(e)}")
    
    def get_public_url(self, object_name: str) -> str:
        """
        Generate public URL for profile picture (fast access)
        
        Args:
            object_name: Object name in bucket
            
        Returns:
            Public URL
        """
        # For local development, use direct MinIO URL
        # In production, you might want to use a CDN or presigned URLs
        base_url = f"http://{settings.MINIO_ENDPOINT}"
        if ":" in base_url:
            # If endpoint includes port, use as-is
            pass
        else:
            # Add default MinIO port
            base_url = f"http://{settings.MINIO_ENDPOINT}:9000"
        
        return f"{base_url}/{self.bucket_name}/{object_name}"
    
    def get_presigned_url(self, object_name: str, expires_seconds: int = 3600) -> str:
        """
        Generate presigned URL for temporary access (for private buckets)
        
        Args:
            object_name: Object name in bucket
            expires_seconds: URL expiration time in seconds
            
        Returns:
            Presigned URL
        """
        try:
            if not self.client:
                raise RuntimeError("MinIO client not initialized")
            
            from datetime import timedelta
            url = self.client.presigned_get_object(
                self.bucket_name,
                object_name,
                expires=timedelta(seconds=expires_seconds)
            )
            return url
        except Exception as e:
            logger.error(f"Error generating presigned URL: {str(e)}")
            return self.get_public_url(object_name)  # Fallback to public URL
