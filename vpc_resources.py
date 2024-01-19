def fetch_and_format_vpc_data(session, region):
    vpc_data_set = []
    client = session.client("ec2")
    try:
        vpc_response = client.describe_vpcs()

        for vpc in vpc_response.get("Vpcs"):
            vpc_data = {}
            vpc_id = vpc.get("VpcId")
            vpc_cidr = vpc.get("CidrBlock")
            vpc_name = [
                tag.get("Value", "")
                for tag in vpc.get("Tags", "")
                if tag.get("Key") == "Name"
            ]
            # Make Dictionary
            vpc_data["VPC Name"] = "".join(vpc_name)
            vpc_data["VPC ID"] = vpc_id
            vpc_data["CIDR Block"] = vpc_cidr
            vpc_data["Region"] = region
            # append vpc data to list
            vpc_data_set.append(vpc_data)

        return vpc_data_set

    except Exception as e:
        print(e)
