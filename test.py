import subprocess
import json
import pandas as pd
import boto3


def get_profile():
    available_profiles = boto3.Session().available_profiles
    selected_profile = ""

    if not available_profiles:
        print("no avaible profile found")
    else:
        for i, profile in enumerate(available_profiles, start=0):
            print(f"{i}. {profile}")

        while True:
            selected_index = int(
                input("Select a profile by entering corresponding number: ")
            )
            if 0 <= selected_index < len(available_profiles):
                selected_profile = available_profiles[selected_index]
                break
            else:
                raise ValueError
    return selected_profile


def create_excel():
    selected_profile = get_profile()

    aws_cli_command = (
        "aws ec2 describe-network-interfaces --query 'NetworkInterfaces[*].{NetworkInterfaceId:NetworkInterfaceId, SecurityGroupID:Groups[*].GroupId}' --profile "
        + selected_profile
    )
    output_json = subprocess.check_output(aws_cli_command, shell=True).decode("utf-8")

    # Load JSON data
    data = json.loads(output_json)

    # Create a pandas DataFrame
    df = pd.DataFrame(data)

    # Create a new DataFrame to hold the expanded data
    expanded_data = []

    # Iterate through each row in the original DataFrame
    for index, row in df.iterrows():
        network_interface_id = row["NetworkInterfaceId"]
        security_group_ids = row["SecurityGroupID"]

        # For each SecurityGroupID, create a new row in the expanded DataFrame
        for security_group_id in security_group_ids:
            expanded_data.append(
                {
                    "SecurityGroupID": security_group_id,
                    "NetworkInterfaceId": network_interface_id,
                }
            )

    # Create an expanded DataFrame from the list of dictionaries
    expanded_df = pd.DataFrame(expanded_data)
    expanded_df = expanded_df.drop_duplicates("SecurityGroupID", ignore_index=True)

    # Save the expanded DataFrame to Excel
    excel_file = selected_profile + "_SG_NI.xlsx"
    expanded_df.to_excel(excel_file, index=False)
    print(f"Data saved to {excel_file}")


create_excel()
