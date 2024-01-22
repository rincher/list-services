def fetch_and_format_route_data(session):
    route_client = session.client("ec2")
    response = route_client.describe_route_tables()
    route_data_set = []
    for route_table in response.get("RouteTables"):
        route_data = {}

        route_vpc = route_table.get("VpcId")
        route_name = [
            tag.get("Value")
            for tag in route_table.get("Tags")
            if tag.get("Key") == "Name" and tag.get("Key","") != ""
        ]
        for association in route_table.get("Associations"):
            route_table_id = association.get("RouteTableId")
            subnet_id = association.get("SubnetId")
            try:

                subnet_response = route_client.describe_subnets(SubnetIds=[subnet_id])
                for subnet in subnet_response.get("Subnets"):
                    subnet_cidr = subnet.get("CidrBlock", "")
                    subnet_ip_count = subnet.get("AvailableIpAddressCount", "")
                    subnet_az = subnet.get("AvailabilityZone", "")
                    subnet_az_id = subnet.get("AvailabilityZoneId", "")
                    subnet_state = subnet.get("State", "")
                    subnet_name = [tag.get("Value") for tag in subnet.get("Tags") if tag.get("Key") == "Name" and tag.get("Key","") != ""]
            except Exception as e:
                continue

        route_data["Name"] = "".join(subnet_name)
        route_data["Subnet ID"] = subnet_id
        route_data["State"] = subnet_state
        route_data["VPC"] = route_vpc
        route_data["IPv4 CIDR"] = subnet_cidr
        route_data["IPv6 CIDR"] = ""
        route_data["Available IPv4 Address"] = subnet_ip_count
        route_data["Availability Zone"] = subnet_az
        route_data["Availability Zone Id"] = subnet_az_id
        route_data["Route Table"] = route_table_id + " | " + "".join(route_name)
        route_data_set.append(route_data)
    return route_data_set