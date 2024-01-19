def fetch_and_format_s3_data(client):
    s3_response = client.list_buckets()
    s3_data_set = []
    for buckets in s3_response.get("Buckets"):
        s3_data = {}

        bucket_name = buckets.get("Name")
        bucket_create_date = buckets.get("CreationDate").strftime(
            "%Y-%m-%d %H:%M:%S %Z"
        )
        # Is Public or Not
        try:
            if client.get_public_access_block(Bucket=bucket_name):
                bucket_policy_status = "Bucket and objects not public"
        except:
            bucket_policy_status = "Objects can be public"

        bucket_location_response = client.get_bucket_location(Bucket=bucket_name)
        bucket_location = bucket_location_response.get("LocationConstraint")

        s3_data["BucketName"] = bucket_name
        s3_data["AWS Region"] = bucket_location
        s3_data["Access"] = bucket_policy_status
        s3_data["CreationDate"] = bucket_create_date
        try:
            if client.get_bucket_website(Bucket=bucket_name):
                s3_data["Remarks"] = "Static Website"
        except Exception as e:
            s3_data["Remarks"] = ""
        s3_data_set.append(s3_data)

    return s3_data_set
