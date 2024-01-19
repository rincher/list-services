def fetch_and_format_nat_data(session):
    nat_client = session.client("ec2")
    nat_response = nat_client.describe_nat_gateways()
    nat_data_set = []

    for nat_gateway in nat_response.get("NatGateways"):
        nat_data = {}

        nat_gateway_id = nat_gateway.get("NatGatewayId")
        nat_vpc_id = nat_gateway.get("VpcId")
        nat_status = nat_gateway.get("State")
        nat_subnet = nat_gateway.get("SubnetId")
        nat_connectivity = nat_gateway.get("ConnectivityType")
        nat_created = nat_gateway.get("CreateTime").strftime("%Y-%m-%d %H:%M:%S %Z")
        nat_name = [
            tag.get("Value", "")
            for tag in nat_gateway.get("Tags", "")
            if tag.get("Key") == "Name"
        ]

        for nat_gateway_address in nat_gateway.get("NatGatewayAddresses"):
            nat_network_interface_id = nat_gateway_address.get("NetworkInterfaceId")
            nat_private_ip = nat_gateway_address.get("PrivateIp")
            nat_public_ip = nat_gateway_address.get("PublicIp")

        nat_data["Name"] = nat_name
        nat_data["NatGatewayId"] = nat_gateway_id
        nat_data["Connectivity"] = nat_connectivity
        nat_data["State"] = nat_status
        nat_data["Elastic IP Address"] = nat_public_ip
        nat_data["Private IP"] = nat_private_ip
        nat_data["Network Interface ID"] = nat_network_interface_id
        nat_data["VPC"] = nat_vpc_id
        nat_data["Subnet"] = nat_subnet
        nat_data["Created"] = nat_created
        nat_data_set.append(nat_data)
    return nat_data_set
