
import json
from pathlib import Path


def load_customer_data():

    project_root = Path(__file__).resolve().parent.parent

    file_path = project_root / "test_data" / "customers.json"

    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data


if __name__ == "__main__":

    customer_data = load_customer_data()

    for customer in customer_data["customers"]:
        print(customer["customer_id"], customer["name"])
