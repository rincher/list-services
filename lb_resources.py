def fetch_and_format_lb_data(session, route53_data):
    lb_client = session.client("elbv2")
    lb_response = lb_client.describe_load_balancers()
    lb_data_set = []
    for lbs in lb_response.get("LoadBalancers"):
        lb_data = {}
        records = []
        lb_dns = lbs.get("DNSName")
        lb_arn = lbs.get("LoadBalancerArn")
        lb_name = lbs.get("LoadBalancerName")
        lb_vpc = lbs.get("VpcId")
        lb_scheme = lbs.get("Scheme")
        lb_type = lbs.get("Type")

        records = fetch_lb_record(route53_data, lb_dns)
        lb_records = ", ".join(records)

        lb_az = []
        for az in lbs.get("AvailabilityZones"):
            zone = az.get("ZoneName")
            subnet_id = az.get("SubnetId")
            lb_az.append(zone + " - " + subnet_id)

        # LB Data
        lb_data["Type"] = lb_type
        lb_data["Resource Name"] = lb_name
        lb_data["용도"] = lb_scheme
        lb_data["ELB Domain"] = lb_dns
        lb_data["Service Domain"] = lb_records
        lb_data["Regions"] = "ap-northeast-2"
        lb_data["Vpc"] = lb_vpc
        lb_data["AZ"] = "\n".join(lb_az)

        print(lb_data.get("AZ"))
        # Describe Target Group
        tg_response = lb_client.describe_target_groups()
        for target_group in tg_response.get("TargetGroups"):
            target_arn = target_group.get("TargetGroupArn")
            target_name = target_group.get("TargetGroupName")
            target_vpc = target_group.get("VpcId")


def fetch_lb_record(route53_data, lb_dns):
    records_list = []
    for route53_info in route53_data:
        if route53_info.get("Type") == "A" or route53_info.get("Type") == "CNAME":
            route_value = route53_info.get("Value").split(".")[1:]
            final_value = ".".join(route_value)
            final_value = final_value.rsplit(".", 1)[0]
            if lb_dns == final_value:
                records_list.append(route53_info.get("Record Name").rsplit(".", 1)[0])

    return records_list
