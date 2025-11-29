# src/ingest.py

import argparse
import boto3
import os
from utils import ensure_trailing_slash

def upload_raw(bucket, folder):
    s3 = boto3.client("s3")

    folder = ensure_trailing_slash(folder)

    if not os.path.exists(folder):
        raise FileNotFoundError(f"Local folder does not exist: {folder}")

    files = [f for f in os.listdir(folder) if f.endswith((".ply", ".pcd"))]

    if not files:
        raise FileNotFoundError("No point cloud files found in the folder.")

    for f in files:
        local_path = os.path.join(folder, f)
        s3_key = f"raw/{f}"

        print(f"Uploading {local_path} → s3://{bucket}/{s3_key}")
        s3.upload_file(local_path, bucket, s3_key)

    print("\n✔ Upload completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--local-folder", required=True)
    args = parser.parse_args()

    upload_raw(args.bucket, args.local_folder)
