orders = []

def create_order(customer, items, total):
    order = {
        "id": len(orders) + 1,
        "customer": customer,
        "items": items,
        "total": total
    }
    orders.append(order)
    return order

def get_all():
    return orders
