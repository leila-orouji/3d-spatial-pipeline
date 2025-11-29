 # src/upload_to_s3.py
"""
Upload all files from a local folder to s3://<bucket>/raw/

Usage:
python src/upload_to_s3.py --bucket your-bucket-name --local-folder data/sample
"""
import argparse
import boto3
from pathlib import Path
import sys

def upload_file(s3_client, local_path: Path, bucket: str, key_prefix: str = "raw/"):
    if not local_path.exists():
        print(f"File not found: {local_path}")
        return
    key = f"{key_prefix}{local_path.name}"
    print(f"Uploading {local_path} -> s3://{bucket}/{key}")
    s3_client.upload_file(str(local_path), bucket, key)

def main(bucket: str, local_folder: str):
    s3 = boto3.client("s3")
    folder = Path(local_folder)
    if not folder.exists():
        print(f"Local folder does not exist: {folder}")
        sys.exit(1)
    files = list(folder.glob("*.*"))
    if not files:
        print(f"No files found in {folder}")
        sys.exit(1)
    for f in files:
        upload_file(s3, f, bucket)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload local files to s3 raw/ folder")
    parser.add_argument("--bucket", required=True, help="S3 bucket name")
    parser.add_argument("--local-folder", default="data/sample", help="Local folder with sample files")
    args = parser.parse_args()
    main(args.bucket, args.local_folder)
