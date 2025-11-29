# src/feature_extract.py

import argparse
import boto3
import tempfile
import open3d as o3d
import numpy as np
import json
from utils import ensure_json_serializable

def extract_features_from_pointcloud(pcd):
    points = np.asarray(pcd.points)

    centroid = points.mean(axis=0).tolist()
    min_bound = points.min(axis=0).tolist()
    max_bound = points.max(axis=0).tolist()

    features = {
        "num_points": len(points),
        "centroid": centroid,
        "min_bound": min_bound,
        "max_bound": max_bound
    }

    return ensure_json_serializable(features)

def process_s3(bucket, key):
    s3 = boto3.client("s3")

    with tempfile.NamedTemporaryFile(suffix=".ply") as tmp:
        s3.download_file(bucket, key, tmp.name)
        pcd = o3d.io.read_point_cloud(tmp.name)

        features = extract_features_from_pointcloud(pcd)

        output_key = key.replace("processed/", "features/").replace(".ply", ".json")

        print(f"Uploading feature file to s3://{bucket}/{output_key}")
        s3.put_object(
            Bucket=bucket,
            Key=output_key,
            Body=json.dumps(features).encode("utf-8"),
            ContentType="application/json"
        )

        print("✔ Features extracted + uploaded.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--key", required=True, help="S3 key under processed/")
    args = parser.parse_args()

    process_s3(args.bucket, args.key)
