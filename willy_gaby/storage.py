from google.cloud import storage


def list_blobs_with_prefix(bucket_name, prefix):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix)

    for blob in blobs:
        blob.download_as_bytes()
        print(blob.name)


def upload_blob(bucket_name, blob_name, data):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.upload_from_string(data)

    print(f"Blob {blob_name} uploaded.")
