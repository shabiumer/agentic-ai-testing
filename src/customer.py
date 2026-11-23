
class Customer:

    def __init__(self, customer_id, name, address):
        self.customer_id = customer_id
        self.name = name
        self.address = address

    def display_details(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "address": self.address
        }
