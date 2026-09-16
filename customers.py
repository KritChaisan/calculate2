customers = []

def add_customer(name, phone):
    customer = {"id": len(customers) + 1, "name": name, "phone": phone}
    customers.append(customer)
    return customer

def get_all():
    return customers
