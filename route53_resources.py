def fetch_and_format_route53_data(client):
    # Get Host Zones
    hosted_zones = client.list_hosted_zones().get("HostedZones")
    zone_info = []
    continent_code = [
        {"Code": "AF", "Name": "Africa"},
        {"Code": "NA", "Name": "North America"},
        {"Code": "OC", "Name": "Oceania"},
        {"Code": "AN", "Name": "Antarctica"},
        {"Code": "AS", "Name": "Asia"},
        {"Code": "EU", "Name": "Europe"},
        {"Code": "SA", "Name": "South America"},
    ]

    # Get Host zone id and zone name
    for hosted_zone in hosted_zones:
        zone_id = hosted_zone.get("Id")
        zone_name = hosted_zone.get("Name")
        is_private = hosted_zone.get("Config").get("PrivateZone")
        if is_private:
            publicity = "Private"
        else:
            publicity = "Public"

        # Get Record Set
        record_response = client.list_resource_record_sets(HostedZoneId=zone_id)
        records = record_response.get("ResourceRecordSets")

        for record in records:
            # ContinentCode
            differentiator = ""
            if "GeoLocation" in record:
                routing_policy = "GeoLocation"
                if "ContinentCode" in record.get("GeoLocation"):
                    record_continent = record.get("GeoLocation").get("ContinentCode")
                    # Get Continent Name From Code
                    for continents in continent_code:
                        if record_continent == continents.get("Code"):
                            continent = continents.get("Name")
                            differentiator = continent
                        # CountryCode
                elif "CountryCode" in record.get("GeoLocation"):
                    if record.get("GeoLocation").get("CountryCode") == "*":
                        differentiator = "Default"
                    else:
                        differentiator = record.get("GeoLocation").get(
                            "SubdivisionCode"
                        )

            # Routing Policy
            elif "Region" in record:
                routing_policy = "Latency"
                differentiator = record.get("Region")
            else:
                routing_policy = "Simple"

            # Set DataSet
            record_name = record.get("Name")
            record_type = record.get("Type")
            record_ttl = record.get("TTL", 0)

            # if record is an alias: Yes
            if record_ttl == 0:
                record_alias = "Yes"
            else:
                record_alias = "No"

            record_values = []
            # if there is an alias record get it else ""
            record_alias_name = record.get("AliasTarget", "")

            if record_alias == "Yes":
                record_values.append(record_alias_name.get("DNSName"))
            else:
                for value in record.get("ResourceRecords"):
                    record_values.append(value.get("Value"))
            final_values = "\n".join(record_values)

            # Add zone + record data
            zone_info.append(
                {
                    "Hosted Zone": publicity,
                    "Zone Name": zone_name,
                    "Record Name": record_name,
                    "Type": record_type,
                    "Routing Policy": routing_policy,
                    "Differentiator": differentiator,
                    "Alias": record_alias,
                    "Value": final_values,
                    "TTL": record_ttl,
                }
            )
    return zone_info
