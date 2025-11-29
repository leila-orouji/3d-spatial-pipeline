# 3D Spatial Data Pipeline on AWS for Digital Twin

A small, realistic pipeline to ingest 3D spatial (point-cloud) data, preprocess it, extract basic features, and store outputs in AWS S3. The pipeline runs locally, inside Docker, or on an EC2 instance with an IAM role.

---

## Features / Deliverables
- `src/upload_to_s3.py` — upload local sample files to `s3://<bucket>/raw/`
- `src/preprocess.py` — download raw point cloud from S3, voxel downsample with Open3D, upload processed result to `s3://<bucket>/processed/`
- `src/download_from_s3.py` — download any S3 object to a local path
- Dockerfile and entrypoint to run scripts inside a reproducible container
- `requirements.txt` with dependencies
- README with step-by-step setup and commands

---

## Recommended S3 bucket structure
