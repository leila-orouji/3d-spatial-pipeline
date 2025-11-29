# src/preprocess.py
"""
Download a point-cloud from S3, perform voxel downsampling using Open3D,
and upload the processed point-cloud back to S3.

Usage (local or inside docker/EC2):
python src/preprocess.py --bucket your-bucket-name \
    --raw-key raw/sample.ply \
    --processed-key processed/sample_processed.ply \
    --voxel-size 0.05
"""
import argparse
import boto3
import tempfile
from pathlib import Path
import open3d as o3d
import os
import sys

s3 = boto3.client("s3")

def download_s3_to_temp(bucket: str, key: str) -> str:
    tmp = tempfile.NamedTemporaryFile(suffix=Path(key).suffix, delete=False)
    print(f"Downloading s3://{bucket}/{key} -> {tmp.name}")
    s3.download_fileobj(bucket, key, tmp)
    tmp.flush()
    return tmp.name

def upload_file_to_s3(local_path: str, bucket: str, key: str):
    print(f"Uploading {local_path} -> s3://{bucket}/{key}")
    s3.upload_file(local_path, bucket, key)

def voxel_downsample(pcd: o3d.geometry.PointCloud, voxel_size: float) -> o3d.geometry.PointCloud:
    return pcd.voxel_down_sample(voxel_size)

def main(bucket: str, raw_key: str, processed_key: str, voxel_size: float):
    try:
        local_raw = download_s3_to_temp(bucket, raw_key)
    except Exception as e:
        print("Error downloading raw file from S3:", e)
        sys.exit(1)

    # Read point cloud
    pcd = o3d.io.read_point_cloud(local_raw)
    if pcd.is_empty():
        print("Warning: downloaded point cloud is empty or unreadable.")
    print("Original points:", len(pcd.points))

    # Downsample
    pcd_down = voxel_downsample(pcd, voxel_size)
    print("Downsampled points:", len(pcd_down.points))

    # Write to temporary file and upload
    tmp_out = tempfile.NamedTemporaryFile(suffix=".ply", delete=False)
    o3d.io.write_point_cloud(tmp_out.name, pcd_down)
    upload_file_to_s3(tmp_out.name, bucket, processed_key)
    print("Processing complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess point cloud from S3 and upload processed result.")
    parser.add_argument("--bucket", required=True, help="S3 bucket name")
    parser.add_argument("--raw-key", required=True, help="S3 key for raw file (e.g., raw/sample.ply)")
    parser.add_argument("--processed-key", required=True, help="S3 key for processed file (e.g., processed/sample_processed.ply)")
    parser.add_argument("--voxel-size", default=0.05, type=float, help="Voxel size for downsampling (float)")
    args = parser.parse_args()
    main(args.bucket, args.raw_key, args.processed_key, args.voxel_size)
