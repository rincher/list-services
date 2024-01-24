def fetch_and_format_subnet_data(session):
    subnet_client = session.client("ec2")
    subnet_data_set = []
    try:
        subnet_response = subnet_client.describe_subnets()
        for subnet in subnet_response.get("Subnets"):
            subnet_data = {}
            subnet_id = subnet.get("SubnetId")
            subnet_vpc_id = subnet.get("VpcId")
            subnet_cidr = subnet.get("CidrBlock")
            subnet_az = subnet.get("AvailabilityZone")
            subnet_ipv6 = subnet.get("Ipv6Native")
            subnet_name = [
                tag.get("Value", "")
                for tag in subnet.get("Tags", "")
                if tag.get("Key") == "Name"
            ]
            subnet_routetable = [
                route_table.get("RouteTableId", "")
                for route_table in subnet_client.describe_route_tables(
                    Filters=[{"Name": "association.subnet-id", "Values": [subnet_id]}]
                ).get("RouteTables", "")
            ]

            subnet_data["SubnetId"] = subnet_id
            subnet_data["Name"] = ", ".join(subnet_name)
            subnet_data["VPCId"] = subnet_vpc_id
            subnet_data["AZ"] = subnet_az
            subnet_data["CIDR"] = subnet_cidr
            subnet_data["RouteTable"] = ", ".join(subnet_routetable)
            subnet_data["Ipv6Native"] = subnet_ipv6
            subnet_data_set.append(subnet_data)
        return subnet_data_set

    except Exception as e:
        print(e)
