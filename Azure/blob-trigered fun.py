import logging 
import azure.functions as func 
from azure.storage.blob import BlobServiceClient 
import pyodbc 
import os 
import csv 
import io 


def main(myblob: func.InputStream): 
    logging.info(f"Processing blob: {myblob.name}, Size: {myblob.length} bytes") 

    # Read raw blob data 
    content = myblob.read().decode("utf-8") 
    reader = csv.reader(io.StringIO(content)) 
    rows = list(reader) 
  

    header = rows[0] 
    data_rows = [r for r in rows[1:] if any(cell.strip() for cell in r)] 

    # Upload processed file to Blob Storage 
    processed_name = myblob.name.replace("raw/", "processed/") 
    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING") 
    blob_service = BlobServiceClient.from_connection_string(conn_str) 
    processed_blob = blob_service.get_blob_client(container="processed", blob=processed_name) 
    output_stream = io.StringIO() 
    writer = csv.writer(output_stream) 
    writer.writerow(header) 
    writer.writerows(data_rows) 
    processed_blob.upload_blob(output_stream.getvalue(), overwrite=True) 
    logging.info(f"Uploaded processed file: {processed_name}") 

    # Write metadata to Azure SQL Database 
    conn = pyodbc.connect(os.getenv("AZURE_SQL_CONNECTION_STRING")) 
    cursor = conn.cursor() 
    cursor.execute( 
        "INSERT INTO MetadataRuns (FileName, RowsProcessed) VALUES (?, ?)", 
        (processed_name, len(data_rows)) 
    ) 
    conn.commit() 

    cursor.close() 
    conn.close() 
    logging.info("Metadata written to Azure SQL DB") 