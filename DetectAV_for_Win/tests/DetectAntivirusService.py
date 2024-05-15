import winreg

def check_auto_start_services(av_list_file):
    with open(av_list_file, "r") as file:
        av_list_file = [line.strip() for line in file if line.strip()]

        regheve = winreg.HKEY_LOCAL_MACHINE
        regpath = r"SYSTEM\CurrentControlSet\Services"

        try:
            with winreg.OpenKey(regheve, regpath, access=winreg.KEY_READ) as key:
                num_keys = winreg.QueryInfoKey(key)[0]

                for i in range(num_keys):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        if any(av_name in subkey_name for av_name in av_list_file):
                            sub_path = fr"{regpath}\{subkey_name}"
                            with winreg.OpenKey(regheve, sub_path, access=winreg.KEY_READ) as subkey:
                                start_type = winreg.QueryValueEx(subkey, 'Start')[0]
                                if start_type == 2:
                                    found = True # matches not found
                                    print(f"Services {subkey_name} set to run automatically")
                    except FileNotFoundError:
                        continue
        except Exception as e:
            print(f"An error occured: {e}")
        if not found:
            print("No matching AV services found set to auto start.")

## File with AV services identifiers to check
av_list_file = "av_services.txt"
check_auto_start_services(av_list_file)




