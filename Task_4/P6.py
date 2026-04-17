import platform
import datetime

FILENAME = "Task_4/sys_log.txt"

def log_system_info():
    os_type    = platform.system()
    timestamp  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = (
        f"OS Type   : {os_type}\n"
        f"Timestamp : {timestamp}\n"
        f"{'------------------------------'}\n"
    )

    with open(FILENAME, "a") as file:
        file.write(log_entry)

    print("System info logged successfully")
    print(log_entry)


def main():
    print("Starting system logger\n")
    log_system_info()


if __name__ == "__main__":
    main()