def fetch_and_format_cf_data(session):
    cf_client = session.client("cloudfront")
    cf_response = cf_client.list_distributions()
    for distribution in cf_response.get("DistributionsList").get("Items"):
        cf_distribution_id = distribution.get("Id")