import json

FILENAME = "Task_4/config.json"

default_settings = {
    "theme": "light",
    "language": "English",
    "volume": 50,
    "notifications": True
}

try:
    with open(FILENAME, "r") as file:
        config = json.load(file)
        print("System Ready.")
        print("Loaded Settings:", config)

except FileNotFoundError:
    print("Config file not found. Creating default config...")
    with open(FILENAME, "w") as file:
        json.dump(default_settings, file, indent=4)
    print("Default config.json created successfully!")
    print("Default Settings:", default_settings)