# src/utils.py

import json

def ensure_trailing_slash(path):
    return path if path.endswith("/") else path + "/"

def ensure_json_serializable(obj):
    """Converts NumPy arrays and non-serializable objects to Python lists."""
    if isinstance(obj, dict):
        return {k: ensure_json_serializable(v) for k, v in obj.items()}
    if hasattr(obj, "tolist"):
        return obj.tolist()
    if isinstance(obj, (list, tuple)):
        return [ensure_json_serializable(v) for v in obj]
    return obj
