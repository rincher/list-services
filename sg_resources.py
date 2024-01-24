import pandas as pd


def fetch_and_format_sg_data(session):
    ec2_client = session.client("ec2")
    sg_data_set = []
    response = ec2_client.describe_network_interfaces()
    for network_interface in response.get("NetworkInterfaces"):
        sg_data = {}
        network_interface_id = network_interface.get("NetworkInterfaceId")
        security_group_ids = [
            sg.get("GroupId") for sg in network_interface.get("Groups")
        ]
        sg_data["NetworkInterfaceId"] = network_interface_id
        sg_data["SecurityGroupIds"] = security_group_ids
        sg_data_set.append(sg_data)

    expanded_data = []
    df = pd.DataFrame(sg_data_set)
    for index, row in df.iterrows():
        ni_id = row["NetworkInterfaceId"]
        sg_ids = row["SecurityGroupIds"]

        if len(sg_ids) > 0:
            for sg_id in sg_ids:
                expanded_data.append(
                    {
                        "SecurityGroupId": sg_id,
                        "NetworkInterfaceId": ni_id,
                    }
                )
    return expanded_data
