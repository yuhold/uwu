import json

def show_status():
    try:
        with open("status.json", "r") as f:
            data = json.load(f)
        print("------ Status ------")
        for key, value in data.items():
            print(f"{key}:")
            for k, v in value.items():
                print(f"  {k}: {v}")
    except FileNotFoundError:
        print("Status file not found.")
    except json.JSONDecodeError:
        print("Status file is invalid.")

if __name__ == "__main__":
     show_status()
