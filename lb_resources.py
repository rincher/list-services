def fetch_and_format_lb_data(session):
    lb_client = session.client("elbv2")
    lb_response = lb_client.describe_load_balancers()
    for lbs in lb_response.get("LoadBalancers"):
        lb_domain = lbs.get("DNSName")
        lb_arn = lbs.get("LoadBalancerArn")
        lb_name = lbs.get("LoadBalancerName")
        lb_vpc = lbs.get("VpcId")


        #Describe Target Group
        tg_response = lb_client.describe_target_groups()
        for target_group in tg_response.get("TargetGroups"):
            target_arn = target_group.get("TargetGroupArn")
            target_name =  target_group.get("TargetGroupName")
            target_vpc = target_group.get("VpcId")
