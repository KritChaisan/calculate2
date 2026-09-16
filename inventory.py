def reduce_stock(product, quantity):
    if product["stock"] < quantity:
        return False
    product["stock"] -= quantity
    return True

def add_stock(product, quantity):
    product["stock"] += quantity
