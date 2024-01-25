import time
import base64
from datetime import datetime 

def retrieve_credential_report(session):
    iam_client = session.client("iam")
    response = iam_client.generate_credential_report()
    while True:
        report_state = iam_client.generate_credential_report(State="Generating")

        if report_state.get("State") == "COMPLETE":
            break

        time.sleep(5)

    credential_report = iam_client.get_credential_report()

    content = credential_report.get("Content")
    credential_data_set = []
    decoded_content = content.decode("utf-8")
    header = decoded_content.split("\n")[0]
    keys = header.split(",")
    rows = decoded_content.split("\n")[1:]
    for row in rows:
        values = row.split(",")
        password_last_changed = values[5]
        password_age = 
        credential_data = dict(zip(keys, values))
        credential_data_set.append(credential_data)

    print(decoded_content)
