# src/download_from_s3.py
"""
Download a file from S3 to local path.

Usage:
python src/download_from_s3.py --bucket your-bucket-name --key processed/sample_processed.ply --out /tmp/sample.ply
"""
import argparse
import boto3
from pathlib import Path
import sys

s3 = boto3.client("s3")

def download_file(bucket: str, key: str, out_path: str):
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading s3://{bucket}/{key} -> {out}")
    try:
        with open(out, "wb") as f:
            s3.download_fileobj(bucket, key, f)
    except Exception as e:
        print("Download failed:", e)
        sys.exit(1)
    print("Download finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download single S3 object to local file.")
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--key", required=True)
    parser.add_argument("--out", required=True, help="Local output path")
    args = parser.parse_args()
    download_file(args.bucket, args.key, args.out)
