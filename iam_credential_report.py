import time
import base64


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

    decoded_content = content.decode("utf-8")
    header = decoded_content.split("\n")[0]
    rows = decoded_content.split("\n")[0:]
    for row in rows:
        print(row)

    print(decoded_content)
