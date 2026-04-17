import json

FILENAME = "Task_4/inventory.json"

def save_inventory(data):
    try:
        with open(FILENAME, "w") as file:
            json.dump(data, file, indent=4)
        print("Inventory saved successfully!")
    except Exception as e:
        print(f"Error saving inventory: {e}")


def load_inventory():
    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)
            print("Inventory loaded successfully!")
            return data
    except FileNotFoundError:
        print("No inventory file found. Starting with empty inventory.")
        return {}


def display_inventory(inventory):
    if not inventory:
        print("Inventory is empty.")
    else:
        print("\n--- Current Inventory ---")
        for item, quantity in inventory.items():
            print(f"  {item}: {quantity} units")
        print("-------------------------")


inventory = load_inventory()
display_inventory(inventory)
save_inventory(inventory)

print("\nReloading inventory from file...")
loaded = load_inventory()
display_inventory(loaded)