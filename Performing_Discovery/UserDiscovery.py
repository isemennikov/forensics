import os
import wmi


def get_admin_accounts(wmi_service):
    for group in wmi_service.Win32_Group():
        if group.Name == "Administrators":
            users = group.associators(wmi_result_class="Win32_UserAccount")
            return [user.Name for user in users]
    return []


def print_user_info(user, admins):
    print(f"Username: {user.Name}")
    print(f"Administrator: {'Yes' if user.Name in admins else 'No'}")
    print(f"Disabled: {user.Disabled}")
    print(f"Domain: {user.Domain}")
    print(f"Local: {user.LocalAccount}")
    print(f"Password Changeable: {user.PasswordChangeable}")
    print(f"Password Expires: {user.PasswordExpires}")
    print(f"Password Required: {user.PasswordRequired}")
    print("n")


def print_password_policy():
    print("Password Policy:")
    os.system("net accounts")


try:
    wmi_service = wmi.WMI()
    admin_accounts = get_admin_accounts(wmi_service)
    for user_account in wmi_service.Win32_UserAccount():
        print_user_info(user_account, admin_accounts)
    print_password_policy()
except wmi.x_wmi as wmi_exc:
    print(f"WMI exception occurred: {wmi_exc}")
