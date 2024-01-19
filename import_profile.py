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
