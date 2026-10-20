from bakery.backend.repository import DB


def get_total_sales():
    return sum(sale.total for sale in DB.list_sales())
