## TODO Optimization


def fetch_and_format_sg_rules(session):
    ec2_client = session.client("ec2")
    sgs = ec2_client.describe_security_groups()
    sg_rule_set = []
    for sg in sgs.get("SecurityGroups"):
        group_id = sg.get("GroupId")
        group_name = sg.get("GroupName")

        #### Inbound Permissions ####
        inbound_rules = sg.get("IpPermissions")
        for inbound_rule in inbound_rules:
            get_inbound_rules(sg_rule_set, inbound_rule, group_id, group_name)

        #### Outbound Permissions ####
        outbound_rules = sg.get("IpPermissionsEgress")
        for outbound_rule in outbound_rules:
            get_outbound_rules(sg_rule_set, outbound_rule, group_id, group_name)

    return sg_rule_set


def get_inbound_rules(sg_rule_set, inbound_rule, group_id, group_name):
    ip_protocol = inbound_rule.get("IpProtocol")
    from_port = inbound_rule.get("FromPort", "")
    to_port = inbound_rule.get("ToPort", "")

    # Is source/target an IPv4
    for ipv4_range in inbound_rule.get("IpRanges"):
        sg_rule = {}
        ipv4_cidr = ipv4_range.get("CidrIp", "")

        sg_rule["GroupId"] = group_id
        sg_rule["GroupName"] = group_name
        sg_rule["Type"] = "Inbound/Ingress"
        sg_rule["IpProtocol"] = ip_protocol
        sg_rule["FromPort"] = from_port
        sg_rule["ToPort"] = to_port

        in_ipv4_description = ipv4_range.get("Description", "")
        if in_ipv4_description == "":
            sg_rule["IpRanges"] = ipv4_cidr
        else:
            sg_rule["IpRanges"] = ipv4_cidr + " (" + in_ipv4_description + ")"

        sg_rule["Ipv6Ranges"] = ""
        sg_rule["prefixList"] = ", ".join(inbound_rule.get("PrefixListIds"))
        sg_rule["UserIdGroupPairs"] = ""

        sg_rule_set.append(sg_rule)

    # Is source/target an IPv6
    for ipv6_range in inbound_rule.get("Ipv6Ranges"):
        sg_rule = {}
        sg_rule["GroupId"] = group_id
        sg_rule["GroupName"] = group_name
        sg_rule["Type"] = "Inbound/Ingress"
        sg_rule["IpProtocol"] = ip_protocol
        sg_rule["FromPort"] = from_port
        sg_rule["ToPort"] = to_port
        sg_rule["IpRanges"] = ""

        ipv6_cidr = ipv6_range.get("CidrIpv6", "")
        in_ipv6_description = ipv6_range.get("Description", "")
        if in_ipv6_description == "":
            sg_rule["Ipv6Ranges"] = ipv6_cidr
        else:
            sg_rule["Ipv6Ranges"] = ipv6_cidr + " (" + in_ipv6_description + ")"

        sg_rule["prefixList"] = ", ".join(inbound_rule.get("PrefixListIds"))
        sg_rule["UserIdGroupPairs"] = ""

        sg_rule_set.append(sg_rule)
    # Is source/target a security group
    user_id_group_pairs = inbound_rule.get("UserIdGroupPairs", "")
    if user_id_group_pairs != []:
        for user_id_group_pair in user_id_group_pairs:
            sg_rule = {}
            sg_rule["GroupId"] = group_id
            sg_rule["GroupName"] = group_name
            sg_rule["Type"] = "Inbound/Ingress"
            sg_rule["IpProtocol"] = ip_protocol
            sg_rule["FromPort"] = from_port
            sg_rule["ToPort"] = to_port
            sg_rule["IpRanges"] = ""
            sg_rule["Ipv6Ranges"] = ""
            sg_rule["prefixList"] = ", ".join(inbound_rule.get("PrefixListIds"))
            from_group = user_id_group_pair.get("GroupId")
            group_description = user_id_group_pair.get("Description", "")
            if group_description == "":
                sg_rule["UserIdGroupPairs"] = from_group
            else:
                sg_rule["UserIdGroupPairs"] = (
                    from_group + " (" + group_description + ")"
                )
            sg_rule_set.append(sg_rule)


def get_outbound_rules(sg_rule_set, outbound_rule, group_id, group_name):

    ip_protocol = outbound_rule.get("IpProtocol")
    from_port = outbound_rule.get("FromPort", "")
    to_port = outbound_rule.get("ToPort", "")

    for ipv4_range in outbound_rule.get("IpRanges"):
        sg_rule = {}
        sg_rule["GroupId"] = group_id
        sg_rule["GroupName"] = group_name
        sg_rule["Type"] = "Outbound/Egress"
        sg_rule["IpProtocol"] = ip_protocol
        sg_rule["FromPort"] = from_port
        sg_rule["ToPort"] = to_port

        ipv4_cidr = ipv4_range.get("CidrIp", "")
        out_ipv4_description = ipv4_range.get("Descriptions", "")
        if out_ipv4_description == "":
            sg_rule["IpRanges"] = ipv4_cidr
        else:
            sg_rule["IpRanges"] = ipv4_cidr + " (" + out_ipv4_description + ")"

        sg_rule["Ipv6Ranges"] = ""
        sg_rule["prefixList"] = ", ".join(outbound_rule.get("PrefixListIds"))
        sg_rule["UserIdGroupPairs"] = ""
        sg_rule_set.append(sg_rule)

    for ipv6_range in outbound_rule.get("Ipv6Ranges"):
        sg_rule = {}
        sg_rule["GroupId"] = group_id
        sg_rule["GroupName"] = group_name
        sg_rule["Type"] = "Outbound/Egress"
        sg_rule["IpProtocol"] = ip_protocol
        sg_rule["FromPort"] = from_port
        sg_rule["ToPort"] = to_port
        sg_rule["IpRanges"] = ""

        ipv6_cidr = ipv6_range.get("CidrIp", "")
        out_ipv6_description = ipv6_range.get("Descriptions", "")
        if out_ipv6_description == "":
            sg_rule["Ipv6Ranges"] = ipv6_cidr
        else:
            sg_rule["Ipv6Ranges"] = ipv6_cidr + " (" + out_ipv6_description + ")"

        sg_rule["PrefixList"] = ", ".join(outbound_rule.get("PrefixListIds"))
        sg_rule["UserIdGroupPairs"] = ""
        sg_rule_set.append(sg_rule)

    user_id_group_pairs = outbound_rule.get("UserIdGroupPairs", "")
    if user_id_group_pairs != []:
        for user_id_group_pair in user_id_group_pairs:
            sg_rule = {}
            sg_rule["GroupId"] = group_id
            sg_rule["GroupName"] = group_name
            sg_rule["Type"] = "Outbound/Egress"
            sg_rule["IpProtocol"] = ip_protocol
            sg_rule["FromPort"] = from_port
            sg_rule["ToPort"] = to_port
            sg_rule["Ipranges"] = ""
            sg_rule["Ipv6Ranges"] = ""
            sg_rule["PrefixList"] = ""
            to_group = user_id_group_pair.get("GroupId")
            group_description = user_id_group_pair.get("Description", "")
            if group_description == "":
                sg_rule["UserIdGroupPairs"] = to_group
            else:
                sg_rule["UserIdGroupPairs"] = to_group + " (" + group_description + ")"
            sg_rule_set.append(sg_rule)
