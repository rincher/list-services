def fetch_and_format_cf_data(client):

    try :
        cf_response = client.list_distributions()
        cf_data_set = []
        for distribution in cf_response.get("DistributionList").get("Items"):
            cf_data = {}
            cf_distribution_id = distribution.get("Id")
            cf_domain_name = distribution.get("DomainName")
            cf_alternate_doamin = distribution.get("Aliases").get("Items",[])
            cf_origins = [items.get("Id")for items in distribution.get("Origins").get("Items")]

            cf_data["Id"] = cf_distribution_id
            cf_data["DomainName"] = cf_domain_name
            cf_data["AlternateDomain"] = cf_alternate_doamin
            cf_data["Origin"] =  "\n".join(cf_origins)

            cf_data_set.append(cf_data)
        return cf_data_set
    except Exception as e:
        print(e)




