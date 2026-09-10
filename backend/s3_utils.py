import os
import uuid
from datetime import datetime
from io import BytesIO
from typing import Optional

S3_BUCKET = os.getenv("AWS_S3_BUCKET") or os.getenv("S3_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

_s3_client = None

def get_s3_client():
    global _s3_client
    if not S3_BUCKET:
        return None
    if _s3_client is None:
        try:
            import boto3
            _s3_client = boto3.client("s3", region_name=AWS_REGION)
        except Exception as e:
            print(f"Warning: Failed to initialize boto3 S3 client: {e}")
            return None
    return _s3_client

def upload_image_to_s3(image_bytes: bytes, animal_id: str, content_type: str = "image/jpeg") -> Optional[str]:
    """Uploads an image to S3 if configured. Returns public S3 URL or None."""
    client = get_s3_client()
    if not client or not S3_BUCKET:
        return None
    
    timestamp = datetime.utcnow().strftime("%Y/%m/%d")
    clean_id = (animal_id or "animal").strip().replace(" ", "_").replace("/", "_")
    unique_name = f"uploads/{timestamp}/{clean_id}_{uuid.uuid4().hex[:8]}.jpg"
    
    try:
        client.put_object(
            Bucket=S3_BUCKET,
            Key=unique_name,
            Body=image_bytes,
            ContentType=content_type,
        )
        url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{unique_name}"
        return url
    except Exception as exc:
        print(f"S3 upload error (non-fatal): {exc}")
        return None
