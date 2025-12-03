import argparse 
# argparse is a Python library for reading command-line arguments.
import boto3
# boto3 is a file transfer tool that uploads any file (3D or non-3D) to S3. boto3 is the official and most reliable library.
# Sometimes for 3D pipelines we need more than just uploading files. Depending on your needs, you may also use:
    # ✔ Open3D - For reading, writing, converting, preprocessing .ply and .pcd.
    #     import open3d as o3d
    #     pc = o3d.io.read_point_cloud("cloud.pcd")
    # ✔ PDAL - For large, heavy LiDAR or LAS datasets.
    # ✔ PyTorch3D or Trimesh - For more advanced 3D operations.
import os
import json
import hashlib
from datetime import datetime
from utils import ensure_trailing_slash

SUPPORTED_FORMATS = (".ply", ".pcd")
 # Common 3D Data Formats
    #     Point Clouds: .ply, .pcd, .xyz, .las , .laz, 
    #     Meshes: .obj, .stl, .off, .gltf / .glb, .fbx
    #     Voxel grids: .binvox, .npy (NumPy voxel arrays), .vox
    #     Depth maps: .png / .exr (depth images)
    #     3D scenes: .usd / .usdz
    
    # Create folders per data type in S3: 
    #     s3://bucket/raw/point_clouds/
    #     s3://bucket/raw/meshes/
    #     s3://bucket/raw/voxels/
    #     s3://bucket/raw/scenes/

   

def compute_sha256(path, block_size=65536):
    """Compute SHA-256 hash of a file for integrity/metadata."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(block_size), b""):
            h.update(blk)
    return h.hexdigest()

def upload_raw(bucket, folder):
    s3 = boto3.client("s3")
    folder = ensure_trailing_slash(folder)

    if not os.path.exists(folder):
        raise FileNotFoundError(f"Local folder does not exist: {folder}")

    # Only .ply and .pcd files
    files = [f for f in os.listdir(folder) if f.lower().endswith(SUPPORTED_FORMATS)]

    if not files:
        raise FileNotFoundError("No .ply or .pcd point cloud files found in the folder.")

    for f in files:
        local_path = os.path.join(folder, f)
        s3_key = f"raw/{f}"

        print(f"Uploading {local_path} → s3://{bucket}/{s3_key}")
        s3.upload_file(local_path, bucket, s3_key)

        # Metadata extraction
        metadata = {
            "filename": f,
            "size_bytes": os.path.getsize(local_path),
            "sha256": compute_sha256(local_path),
            "uploaded_at": datetime.utcnow().isoformat() + "Z",
            "format": os.path.splitext(f)[1].lower()
        }

        metadata_key = f"raw/{f}.metadata.json"
        s3.put_object(
            Bucket=bucket,
            Key=metadata_key,
            Body=json.dumps(metadata, indent=2).encode("utf-8")
        )
        print(f"Metadata uploaded → s3://{bucket}/{metadata_key}")

    print("\n✔ Upload completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--local-folder", required=True)
    args = parser.parse_args()

    upload_raw(args.bucket, args.local_folder)
