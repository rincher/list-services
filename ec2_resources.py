def fetch_and_format_ec2_data(client):
    response = client.describe_instances()
    instances = []
    instance_name = ""

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_data = {}
            for tag in instance["Tags"]:
                if tag["Key"] == "Name":
                    instance_name = tag["Value"]

                instance_data["InstanceName"] = instance_name
                instance_data["InstanceId"] = instance.get("InstanceId", "")
                instance_data["InstanceType"] = instance.get("InstanceType", "")
                instance_data["State"] = instance.get("State", {}).get("Name", "")
                instance_data["PrivateIp"] = instance.get("PrivateIpAddress", "")
                instance_data["PublicIp"] = instance.get("PublicIpAddress", "")
                instance_data["SubnetId"] = instance.get("SubnetId", "")
                instance_data["VpcId"] = instance.get("VpcId", "")
                instance_data["IAMProfile"] = instance.get(
                    "IamInstanceProfile", {}
                ).get("Arn", "")
                for i in range(len(instance.get("SecurityGroups"))):
                    instance_data[f"SecurityGroup{i+1}"] = instance.get(
                        "SecurityGroups"
                    )[i].get("GroupId", "")

                for j in range(len(instance.get("BlockDeviceMappings"))):
                    instance_data[f"EBS{j+1}"] = instance.get("BlockDeviceMappings")[
                        j
                    ].get("DeviceName", "")
                if instance_data["IAMProfile"] != "":
                    instance_data["IAMProfile"] = instance_data["IAMProfile"].split(
                        "/"
                    )[1]

            instances.append(instance_data)
    return instances
