## TODO Optimization


def fetch_and_format_sg_rules(session):
    ec2_client = session.client("ec2")
    sgs = ec2_client.describe_security_groups()
    sg_rule_set = []
    for sg in sgs.get("SecurityGroups"):
        group_id = sg.get("GroupId")
        group_name = sg.get("GroupName")

        # Inbound Permissions
        inbound_rules = sg.get("IpPermissions")
        for inbound_rule in inbound_rules:
            get_inbound_rules(sg_rule_set, inbound_rule, group_id, group_name)

        # Outbound Permissions
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
        sg_rule = {"GroupId": group_id, "GroupName": group_name, "Type": "Inbound/Ingress", "IpProtocol": ip_protocol,
                   "FromPort": from_port, "ToPort": to_port,"Ipv6Ranges": "", "UserIdGroupPairs": ""}

        ipv4_cidr = ipv4_range.get("CidrIp", "")
        in_ipv4_description = ipv4_range.get("Description", "")
        if in_ipv4_description == "":
            sg_rule["IpRanges"] = ipv4_cidr
        else:
            sg_rule["IpRanges"] = ipv4_cidr + " (" + in_ipv4_description + ")"

        plist_in_ipv4 = []
        for prefixListId in inbound_rule.get("PrefixListIds"):
            plist_in_ipv4.append(prefixListId.get("PrefixListId"))

        sg_rule["PrefixList"] = ", ".join(plist_in_ipv4)

        sg_rule_set.append(sg_rule)

    # Is source/target an IPv6
    for ipv6_range in inbound_rule.get("Ipv6Ranges"):
        sg_rule = {"GroupId": group_id, "GroupName": group_name, "Type": "Inbound/Ingress", "IpProtocol": ip_protocol,
                   "FromPort": from_port, "ToPort": to_port, "IpRanges": "", "UserIdGroupPairs" : ""}

        plist_in_ipv6 = []
        ipv6_cidr = ipv6_range.get("CidrIpv6", "")
        in_ipv6_description = ipv6_range.get("Description", "")

        if in_ipv6_description == "":
            sg_rule["Ipv6Ranges"] = ipv6_cidr
        else:
            sg_rule["Ipv6Ranges"] = ipv6_cidr + " (" + in_ipv6_description + ")"

        for prefixListId in inbound_rule.get("PrefixListIds"):
            plist_in_ipv6.append(prefixListId.get("PrefixListId"))

        sg_rule["PrefixList"] = ", ".join(plist_in_ipv6)

        sg_rule_set.append(sg_rule)

    # Is source/target a security group
    user_id_group_pairs = inbound_rule.get("UserIdGroupPairs", "")
    if user_id_group_pairs:
        for user_id_group_pair in user_id_group_pairs:
            sg_rule = {"GroupId": group_id, "GroupName": group_name, "Type": "Inbound/Ingress",
                       "IpProtocol": ip_protocol, "FromPort": from_port, "ToPort": to_port, "IpRanges": "",
                       "Ipv6Ranges": "", "PrefixList": ""}

            from_group = user_id_group_pair.get("GroupId")
            group_description = user_id_group_pair.get("Description", "")

            if group_description == "":
                sg_rule["UserIdGroupPairs"] = from_group
            else:
                sg_rule["UserIdGroupPairs"] = (from_group + " (" + group_description + ")")

            sg_rule_set.append(sg_rule)


def get_outbound_rules(sg_rule_set, outbound_rule, group_id, group_name):

    ip_protocol = outbound_rule.get("IpProtocol")
    from_port = outbound_rule.get("FromPort", "")
    to_port = outbound_rule.get("ToPort", "")

    for ipv4_range in outbound_rule.get("IpRanges"):
        sg_rule = {"GroupId": group_id, "GroupName": group_name, "Type": "Outbound/Egress", "IpProtocol": ip_protocol,
                   "FromPort": from_port, "ToPort": to_port, "UserIdGroupPairs": "", "Ipv6Ranges": ""}
        plist_out_ipv4 = []
        ipv4_cidr = ipv4_range.get("CidrIp", "")
        out_ipv4_description = ipv4_range.get("Descriptions", "")

        if out_ipv4_description == "":
            sg_rule["IpRanges"] = ipv4_cidr
        else:
            sg_rule["IpRanges"] = ipv4_cidr + " (" + out_ipv4_description + ")"

        for prefixListId in outbound_rule.get("PrefixListIds"):
            plist_out_ipv4.append(prefixListId.get("PrefixListId"))
        sg_rule["PrefixList"] = ", ".join(plist_out_ipv4)

        sg_rule_set.append(sg_rule)

    for ipv6_range in outbound_rule.get("Ipv6Ranges"):
        plist_out_ipv6 = []
        sg_rule = {"GroupId": group_id, "GroupName": group_name, "Type": "Outbound/Egress", "IpProtocol": ip_protocol,
                   "FromPort": from_port, "ToPort": to_port, "IpRanges": "", "UserIdGroupPairs": ""}

        ipv6_cidr = ipv6_range.get("CidrIp", "")
        out_ipv6_description = ipv6_range.get("Descriptions", "")
        if out_ipv6_description == "":
            sg_rule["Ipv6Ranges"] = ipv6_cidr
        else:
            sg_rule["Ipv6Ranges"] = ipv6_cidr + " (" + out_ipv6_description + ")"

        for prefixListId in outbound_rule.get("PrefixListIds"):
            plist_out_ipv6.append(prefixListId.get("PrefixListId"))
        sg_rule["PrefixList"] = ", ".join(plist_out_ipv6)

        sg_rule_set.append(sg_rule)

    user_id_group_pairs = outbound_rule.get("UserIdGroupPairs", "")

    if user_id_group_pairs:
        for user_id_group_pair in user_id_group_pairs:
            sg_rule = {"GroupId": group_id, "GroupName": group_name, "Type": "Outbound/Egress",
                       "IpProtocol": ip_protocol, "FromPort": from_port, "ToPort": to_port, "Ipranges": "",
                       "Ipv6Ranges": "", "PrefixList": ""}
            to_group = user_id_group_pair.get("GroupId")
            group_description = user_id_group_pair.get("Description", "")
            if group_description == "":
                sg_rule["UserIdGroupPairs"] = to_group
            else:
                sg_rule["UserIdGroupPairs"] = to_group + " (" + group_description + ")"
            sg_rule_set.append(sg_rule)
