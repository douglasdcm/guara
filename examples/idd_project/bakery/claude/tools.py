# tools.py


def get_product_info(name):
    # query DB
    return {"name": name, "price": 5.0, "stock": 10}


def check_stock(name, quantity):
    return quantity <= 10


def calculate_total(items, discount=0):
    total = sum(k["p"] * k["q"] for k in items)
    return total * (1 - discount)
