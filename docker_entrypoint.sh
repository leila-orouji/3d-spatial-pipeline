#!/bin/bash
# docker_entrypoint.sh
# Simple entrypoint: if no args are provided it prints a usage hint.
set -e

if [ "$#" -eq 0 ]; then
  echo "No command provided. Example usage:"
  echo " docker run --rm -e AWS_REGION=us-east-1 -e AWS_PROFILE=default -e BUCKET=your-bucket-name <image> python preprocess.py --bucket \$BUCKET --raw-key raw/sample.ply --processed-key processed/sample_proc.ply"
  exec /bin/bash -l
else
  exec "$@"
fi
