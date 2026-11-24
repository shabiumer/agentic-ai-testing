from src.database import get_customer_bills

records = get_customer_bills("C1001")

for record in records:
    print(record)