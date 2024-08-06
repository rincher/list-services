import os
from queue import Queue

import boto3
from import_profile import get_profile
from ec2_resources import fetch_and_format_ec2_data
from rds_resources import fetch_and_format_rds_data
from s3_resources import fetch_and_format_s3_data
from vpc_resources import fetch_and_format_vpc_data
from subnet_resources import fetch_and_format_subnet_data
from nat_resources import fetch_and_format_nat_data
from vpn_resources import fetch_and_format_vpn_data
from cf_resources import fetch_and_format_cf_data
from route_resources import fetch_and_format_route_data
from role_resources import fetch_and_format_role_data
from sg_resources import fetch_and_format_sg_data
from sg_rules import fetch_and_format_sg_rules
from route53_resources import fetch_and_format_route53_data
from lb_resources import fetch_and_format_lb_data
from iam_credential_report import retrieve_credential_report
import pandas as pd
import threading


def scan_services(profile, region):
    services = ["ec2", "s3", "rds", "cloudfront"]
    session = boto3.Session(profile_name=profile, region_name=region)

    result_queue = Queue()

    def thread_function(queue, func, *args):
        result = func(*args)
        queue.put((func.__name__, result))

    # Define threads for each function call
    threads = [
        threading.Thread(target=thread_function, args=(result_queue, fetch_and_format_vpc_data, session, region)),
        threading.Thread(target=thread_function, args=(result_queue, fetch_and_format_subnet_data, session)),
        threading.Thread(target=thread_function, args=(result_queue, fetch_and_format_nat_data, session)),
        threading.Thread(target=thread_function, args=(result_queue, fetch_and_format_vpn_data, session)),
        threading.Thread(target=thread_function, args=(result_queue, fetch_and_format_route_data, session)),
        threading.Thread(target=thread_function, args=(result_queue, fetch_and_format_role_data, session)),
        threading.Thread(target=thread_function, args=(result_queue, fetch_and_format_sg_data, session)),
        threading.Thread(target=thread_function, args=(result_queue, fetch_and_format_sg_rules, session)),
        threading.Thread(target=thread_function, args=(result_queue, fetch_and_format_route53_data, session)),
        threading.Thread(target=thread_function, args=(result_queue, retrieve_credential_report, session))
    ]

    # Add service-specific threads
    for service_name in services:
        client = session.client(service_name)
        if service_name == "ec2":
            threads.append(
                threading.Thread(target=thread_function, args=(result_queue, fetch_and_format_ec2_data, client)))
        elif service_name == "rds":
            threads.append(
                threading.Thread(target=thread_function, args=(result_queue, fetch_and_format_rds_data, client)))
        elif service_name == "s3":
            threads.append(
                threading.Thread(target=thread_function, args=(result_queue, fetch_and_format_s3_data, client)))
        elif service_name == "cloudfront":
            threads.append(
                threading.Thread(target=thread_function, args=(result_queue, fetch_and_format_cf_data, client)))

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Collect results
    results = {}
    while not result_queue.empty():
        func_name, result = result_queue.get()
        results[func_name] = result

    lb_data = fetch_and_format_lb_data(session, results['fetch_and_format_route53_data'])
    # Prepare DataFrames
    vpc_df = pd.DataFrame(results['fetch_and_format_vpc_data'])
    subnet_df = pd.DataFrame(results['fetch_and_format_subnet_data'])
    nat_df = pd.DataFrame(results['fetch_and_format_nat_data'])
    vpn_df = pd.DataFrame(results['fetch_and_format_vpn_data'])
    lb_df = pd.DataFrame(lb_data)
    route_df = pd.DataFrame(results['fetch_and_format_route_data'])
    role_df = pd.DataFrame(results['fetch_and_format_role_data'])
    sg_df = pd.DataFrame(results['fetch_and_format_sg_data']).drop_duplicates("SecurityGroupId", ignore_index=True)
    iam_df = pd.DataFrame(results['retrieve_credential_report'])
    sg_rule_df = pd.DataFrame(results['fetch_and_format_sg_rules'])
    ec2_df = pd.DataFrame(results['fetch_and_format_ec2_data'])
    rds_df = pd.DataFrame(results['fetch_and_format_rds_data'])
    s3_df = pd.DataFrame(results['fetch_and_format_s3_data'])
    cf_df = pd.DataFrame(results['fetch_and_format_cf_data'])
    route53_df = pd.DataFrame(results['fetch_and_format_route53_data'])

    filename = "aws_resource_" + region + "_" + profile + ".xlsx"
    if os.path.exists(filename):
        os.remove(filename)

    with pd.ExcelWriter(
            filename,
            engine="xlsxwriter",
            mode="w",
    ) as writer:
        # writer.book.formats[0].set_text_wrap()
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
        iam_df.to_excel(writer, sheet_name="IAM Credentials", index=False)
        ec2_df.to_excel(writer, sheet_name="EC2 Resources", index=False)
        rds_df.to_excel(writer, sheet_name="RDS Resources", index=False)
        s3_df.to_excel(writer, sheet_name="S3 Resources", index=False)
        lb_df.to_excel(writer, sheet_name="Load Balancers", index=False)
        cf_df.to_excel(writer, sheet_name="CloudFront Resources", index=False)
        route_df.to_excel(writer, sheet_name="Route Table", index=False)
        role_df.to_excel(writer, sheet_name="Role Statement", index=False)
        sg_df.to_excel(writer, sheet_name="SG Summary", index=False)
        route53_df.to_excel(writer, sheet_name="Route53", index=False)
        sg_rule_df.to_excel(writer, sheet_name="SG InOut Rules", index=False)


selected_profile = get_profile()

region = input("input region: ") or "ap-northeast-2"
# region = "ap-northeast-2"

scan_services(selected_profile, region)
