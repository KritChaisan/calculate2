def total_sales(orders):
    return sum(order["total"] for order in orders)

def total_orders(orders):
    return len(orders)

def low_stock(products, limit=5):
    return [p for p in products if p["stock"] <= limit]
