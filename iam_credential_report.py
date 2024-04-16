import time
from datetime import datetime, timezone


def retrieve_credential_report(session):
    iam_client = session.client("iam")
    while True:
        report_state = iam_client.generate_credential_report(State="Generating")

        if report_state.get("State") == "COMPLETE":
            break

        time.sleep(5)

    credential_report = iam_client.get_credential_report()

    content = credential_report.get("Content")
    credential_data_set = []
    decoded_content = content.decode("utf-8")
    rows = decoded_content.split("\n")[1:]
    current_datetime = datetime.now(timezone.utc)

    for row in rows:
        values = row.split(",")
        password_age = 0
        access_key1_age = 0
        access_key2_age = 0
        credential_data = {}

        # check if password enabled
        user = values[0]
        password_enabled = values[3]
        if password_enabled == "true":
            password_last_changed = values[5]
            password_diff = (
                current_datetime - datetime.fromisoformat(password_last_changed)
                if current_datetime > datetime.fromisoformat(password_last_changed)
                else datetime.fromisoformat(password_last_changed) - current_datetime
            )
            password_age = password_diff.days

        mfa_enabled = values[7]

        # check if access_key1 enabled
        access_key1_enabled = values[8]
        if access_key1_enabled == "true":
            access_key1_last_changed = values[9]
            access_key1_diff = (
                current_datetime - datetime.fromisoformat(access_key1_last_changed)
                if current_datetime > datetime.fromisoformat(access_key1_last_changed)
                else datetime.fromisoformat(access_key1_last_changed) - current_datetime
            )
            access_key1_age = access_key1_diff.days

        access_key2_enabled = values[13]
        if access_key2_enabled == "true":
            access_key2_last_changed = values[14]
            access_key2_diff = (
                current_datetime - datetime.fromisoformat(access_key2_last_changed)
                if current_datetime > datetime.fromisoformat(access_key2_last_changed)
                else datetime.fromisoformat(access_key2_last_changed) - current_datetime
            )
            access_key2_age = access_key2_diff.days

        if (
            int(password_age) > 90
            or int(access_key1_age) > 90
            or int(access_key2_age) > 90
        ):
            credential_data["User"] = user
            # check MFA Enabled
            credential_data["MFA enabled"] = mfa_enabled
            # check password enable
            credential_data["Password enabled"] = password_enabled
            if password_enabled == "false" and password_age == 0:
                credential_data["Password last changed"] = "N/A"
            else:
                credential_data["Password last changed"] = str(password_age)
            # check accesskey1 last_rotated_date
            credential_data["Access key1 active"] = access_key1_enabled
            if access_key1_enabled == "false" and access_key1_age == 0:
                credential_data["Access key1 last changed"] = "N/A"
            else:
                credential_data["Access key1 last changed"] = str(access_key1_age)
            # check accesskey2 last_rotated_date
            credential_data["Access key2 active"] = access_key2_enabled
            if access_key2_enabled == "false" and access_key2_age == 0:
                credential_data["Access key2 last changed"] = "N/A"
            else:
                credential_data["Access key2 last changed"] = str(access_key2_age)
            credential_data_set.append(credential_data)

    return credential_data_set
