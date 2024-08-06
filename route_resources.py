def fetch_and_format_route_data(session):
    route_client = session.client("ec2")
    response = route_client.describe_route_tables()
    route_data_set = []
    for route_table in response.get("RouteTables"):
        route_data = {}
        route_vpc = route_table.get("VpcId")
        route_name = ""
        if len(route_table.get("Tags")) > 0:
            for tag in route_table.get("Tags"):
                if tag.get("Key") == "Name":
                    route_name = tag.get("Value")

        for association in route_table.get("Associations"):
            route_table_id = association.get("RouteTableId")
            subnet_id = association.get("SubnetId", "")
            subnet_cidr = ""
            subnet_ip_count = ""
            subnet_az = ""
            subnet_az_id = ""
            subnet_state = ""
            subnet_name = ""

            try:
                subnet_response = route_client.describe_subnets(SubnetIds=[subnet_id])
                for subnet in subnet_response.get("Subnets"):
                    subnet_cidr = subnet.get("CidrBlock", "")
                    subnet_ip_count = subnet.get("AvailableIpAddressCount", "")
                    subnet_az = subnet.get("AvailabilityZone", "")
                    subnet_az_id = subnet.get("AvailabilityZoneId", "")
                    subnet_state = subnet.get("State", "")
                    if len(subnet.get("Tags")) > 0:
                        for tag in subnet.get("Tags"):
                            if tag.get("Key") == "Name":
                                subnet_name = tag.get("Value")

            except Exception as e:
                continue

            route_data["Subnet Name"] = "".join(subnet_name)
            route_data["Subnet ID"] = subnet_id
            route_data["State"] = subnet_state
            route_data["VPC"] = route_vpc
            route_data["IPv4 CIDR"] = subnet_cidr
            route_data["IPv6 CIDR"] = ""
            route_data["Available IPv4 Address"] = subnet_ip_count
            route_data["Availability Zone"] = subnet_az
            route_data["Availability Zone Id"] = subnet_az_id
            route_data["Route Table"] = f"{route_table_id} {route_name}"
            route_data_set.append(route_data)

    return route_data_set
