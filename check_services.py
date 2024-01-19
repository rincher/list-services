import boto3
from import_profile import get_profile
from ec2_resources import fetch_and_format_ec2_data
from rds_resources import fetch_and_format_rds_data
from s3_resources import fetch_and_format_s3_data
from vpc_resources import fetch_and_format_vpc_data
from subnet_resources import fetch_and_format_subnet_data
from nat_resources import fetch_and_format_nat_data
from vpn_resources import fetch_and_format_vpn_data
import pandas as pd


def scan_services(profile, region):
    services = ["ec2", "s3", "rds", "lambda", "dynamodb", "apigateway"]
    session = boto3.Session(profile_name=profile, region_name=region)

    # Default Data (VPC, Subnet, NGW, IGW, VPN, VPC Peering, DX)
    # VPC
    vpc_data = fetch_and_format_vpc_data(session, region)
    # Subnet
    subnet_data = fetch_and_format_subnet_data(session)
    # Nat
    nat_data = fetch_and_format_nat_data(session)
    # VPN
    vpn_data = fetch_and_format_vpn_data(session)

    for service_name in services:
        client = session.client(service_name)

        if service_name == "ec2":
            ec2_data = fetch_and_format_ec2_data(client)
        elif service_name == "rds":
            rds_data = fetch_and_format_rds_data(client)
        elif service_name == "s3":
            s3_data = fetch_and_format_s3_data(client)

    vpc_df = pd.DataFrame(vpc_data)
    subnet_df = pd.DataFrame(subnet_data)
    nat_df = pd.DataFrame(nat_data)
    vpn_df = pd.DataFrame(vpn_data)

    ec2_df = pd.DataFrame(ec2_data)
    rds_df = pd.DataFrame(rds_data)
    s3_df = pd.DataFrame(s3_data)

    with pd.ExcelWriter(
        "aws_resource_" + region + "_" + profile + ".xlsx", engine="xlsxwriter"
    ) as writer:
        vpc_df.to_excel(
            writer, sheet_name="Network", startrow=0, startcol=0, index=False
        )
        subnet_df.to_excel(
            writer,
            sheet_name="Network",
            startrow=len(vpc_df) + 3,
            startcol=0,
            index=False,
        )
        nat_df.to_excel(
            writer,
            sheet_name="Network",
            startrow=(len(vpc_df) + 3) + (len(subnet_df) + 3),
            startcol=0,
            index=False,
        )
        vpn_df.to_excel(
            writer,
            sheet_name="Network",
            startrow=(len(vpc_df) + 3) + (len(subnet_df) + 3) + (len(nat_df) + 3),
            startcol=0,
            index=False,
        )
        ec2_df.to_excel(writer, sheet_name="EC2 Resources", index=False)
        rds_df.to_excel(writer, sheet_name="RDS Resources", index=False)
        s3_df.to_excel(writer, sheet_name="S3 Resources", index=False)


selected_profile = get_profile()

# region = input("input region: ")
region = "ap-northeast-2"

scan_services(selected_profile, region)
