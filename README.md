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
- s3://bucket/raw/point_clouds/
- s3://bucket/raw/meshes/
- s3://bucket/raw/voxels/
- s3://bucket/raw/scenes/


 # 3D Spatial Data Pipeline on Azure for Digital Twin

## Pipeline Diagram

            Local Folder  
               → azcopy sync  
               → Blob Storage (raw/)  
                   → Blob Trigger  
                       → Azure Function  
                           → Process file  
                           → Write to Blob Storage (processed/)  
                           → Write metadata to Azure SQL Database
## Features / Deliverables

              → Azure Function (triggered when new file arrives)  
               In AWS → S3 
               In Azure → Azure Blob Storage 

               → Upload data from local machine automatically 

                Equivalent of aws s3 sync, use AzCopy (recommended) 

               → Azure VM / Azure Compute Instance (optional heavy processing) 
                 Azure Virtual Machine is Equivalent of EC2. 
                 Azure Container Instances or AKS is Equivalent of AWS Fargate or ECS/Kubernetes. 

               → Azure Blob Storage (processed) 

               → Azure SQL Database (store metadata)  
                Equivalent of AWS RDS. 

  

  
