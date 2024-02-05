def fetch_and_format_sg_rules(session):
    ec2_client = session.client("ec2")
    sgs = ec2_client.describe_security_groups()
    sg_rule_set = []
    for sg in sgs.get("SecurityGroups"):
        sg_rule = {}
        group_id = sg.get("GroupId")
        group_name = sg.get("GroupName")
        sg_rule["GroupId"] = group_id
        sg_rule["GroupName"] = group_name

        inbound_rules = sg.get("IpPermissions")
        for inbound_rule in inbound_rules:
            sg_rule["Type"] = "Inbound/Ingress"
            if inbound_rule.get("IpProtocol") == "-1":
                ip_protocol = ("All",)
                sg_rule["IpProtocol"] = ip_protocol
                to_port = "All"
            else:
                ip_protocol = inbound_rule.get("IpProtocol")
                form_port = inbound_rule.get("FromPort")
                to_port = inbound_rule.get("ToPort")
                if to_port == -1:
                    to_port = "N/A"
            # Is source/target an IPv4
            if len(inbound_rule.get("IPRanges")) > 0:
                for ip4_range in inbound_rule.get("IpRanges"):
                    ip4_cidr = ip4_range.get("CidrIp")

            # Is source/target an IPv6
            if len(inbound_rule.get("Ipv6Ranges")) > 0:
                for ip6_range in inbound_rules.get("Ipv6Ranges"):
                    ip4_cidr = ip6_range.get("CidrIpv6")

            # Is source/target a security group
            if len(inbound_rule.get("UserIdGroupPairs") > 0):
                for source in inbound_rule.get("UserIdGroupPairs"):
                    from_source = source.get("GroupId")
