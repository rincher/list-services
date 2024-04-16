from datetime import datetime, timezone


def fetch_and_format_role_data(session):
    iam_client = session.client("iam")
    response = iam_client.list_roles()
    role_data_set = []
    today = datetime.now(tz=timezone.utc)

    for role_list in response.get("Roles"):
        role_data = {}
        role_path = role_list.get("Path")
        role_name = role_list.get("RoleName")
        role_arn = role_list.get("Arn")

        created_time = today - role_list.get("CreateDate")
        created_days = str(created_time.days)

        #
        role_response = iam_client.get_role(RoleName=role_name)
        role_principal = (
            role_response.get("Role")
            .get("AssumeRolePolicyDocument")
            .get("Statement")[0]
            .get("Principal")
        )
        try:
            last_used_days = "Never"
            last_used = today - role_response.get("Role").get("RoleLastUsed").get(
                "LastUsedDate"
            )
            last_used_days = str(last_used.days)
        except Exception:
            continue

        role_max_session = role_response.get("Role").get("MaxSessionDuration")

        role_data["RoleName"] = role_name
        role_data["Path"] = role_path
        role_data["Trusted Entity"] = role_principal
        role_data["Creation Time"] = created_days
        role_data["Arn"] = role_arn
        role_data["Last Activity"] = last_used_days
        role_data["Max Cli/api session"] = role_max_session
        role_data_set.append(role_data)
    return role_data_set
