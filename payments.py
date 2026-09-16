def calculate_subtotal(items):
    return sum(item["price"] * item["quantity"] for item in items)

def calculate_tax(subtotal, rate):
    return subtotal * rate

def calculate_total(subtotal, tax):
    return subtotal + tax
