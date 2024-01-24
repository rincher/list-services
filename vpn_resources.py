def fetch_and_format_vpn_data(session):
    vpn_client = session.client("ec2")

    vpn_data_set = []
    try:
        vpn_response = vpn_client.describe_vpn_connections()
        for vpn_connection in vpn_response.get("VpnConnections", ""):
            vpn_data = {}
            vpn_connection.get("VpnConnectionId", "")
            vpn_state = vpn_connection.get("State", "")
            vpn_cgi = vpn_connection.get("CustomerGatewayId", "")
            vpn_gw_id = vpn_connection.get("VpnGatewayId", "")
            # Find VPC ID
            vgw_vpc = ""
            if vpn_gw_id != "":
                vgw_response = vpn_client.describe_vpn_gateways(
                    VpnGatewayIds=[vpn_gw_id]
                )
                for vgw in vgw_response.get("VpnGateways"):
                    vgw_vpc = vgw.get("VpcAttachments", "")[0].get("VpcId", "")

            vpn_name = [
                tag.get("Value")
                for tag in vpn_connection.get("Tags", "")
                if tag.get("Key", "") == "Name"
            ]
            vpn_tgw = vpn_connection.get("TransitGatewayId", "")
            vpn_id = vpn_connection.get("VpnConnectionId", "")
            vpn_ipversion = vpn_connection.get("Options", "").get(
                "TunnelInsideIpVersion", ""
            )
            vpn_type = vpn_connection.get("Type", "")
            vpn_routing = (
                "Static"
                if vpn_connection.get("Options").get("StaticRoutesOnly") == True
                else "Dynamic"
            )
            vpn_outside = vpn_connection.get("Options").get("OutsideIpAddressType", "")
            vpn_category = vpn_connection.get("Category")
            vpn_acceleration = (
                "False"
                if vpn_connection.get("Options").get("EnableAcceleration") == False
                else "True"
            )
            vpn_localip = vpn_connection.get("Options", "").get("LocalIpv4NetworkCidr")
            vpn_remoteip = vpn_connection.get("Options", "").get(
                "RemoteIpv4NetworkCIdr"
            )
            vpn_association = vpn_connection.get("GatewayAssociationState", "")
            vpn_gw_ip = (
                vpn_connection.get("CustomerGatewayConfiguration", "")
                .split("<ip_address>")[1]
                .split("</ip_address>")[0]
                .strip()
            )
            vpn_virtual_gw = vpn_connection.get("VpnGatewayId", "")

            # create dictionary
            vpn_data["Name"] = ", ".join(vpn_name)
            vpn_data["VPN ID"] = vpn_id
            vpn_data["State"] = vpn_state
            vpn_data["Virtual Gateway"] = vpn_virtual_gw
            vpn_data["Transit Gateway"] = vpn_tgw
            vpn_data["Customer Gateway"] = vpn_cgi
            vpn_data["Customer Gateway Address"] = vpn_gw_ip
            vpn_data["Inside IP Version"] = vpn_ipversion
            vpn_data["Type"] = vpn_type
            vpn_data["Category"] = vpn_category
            vpn_data["VPC"] = vgw_vpc
            vpn_data["Routing"] = vpn_routing
            vpn_data["Acceleration Enabled"] = vpn_acceleration
            vpn_data["Authentication"] = "Pre-shared-key"
            vpn_data["Local IPV4 Network CIDR"] = vpn_localip
            vpn_data["Remote IPV4 Network CIDR"] = vpn_remoteip
            vpn_data["Gateway Association State"] = vpn_association
            vpn_data["Outside IP address type"] = vpn_outside
            vpn_data_set.append(vpn_data)
        return vpn_data_set

    except Exception as e:
        print(e)
