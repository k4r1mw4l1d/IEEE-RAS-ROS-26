FILENAME = "Task_4/log.txt"

def write_log(message):
    with open(FILENAME, "a") as file:
        file.write(message + "\n")

def read_log():
    with open(FILENAME, "r") as file:
        content = file.read()
    print(content)

if __name__ == "__main__":
    write_log("My name is Karim")
    write_log("I love ROS")
    write_log("I hate doing tasks")
    read_log()