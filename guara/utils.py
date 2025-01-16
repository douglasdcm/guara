"""

"""
def get_transaction_info(transaction) -> str:
    module_name = ".".join(transaction.__module__.split(".")[-1:])
    return f"{module_name}.{transaction.__name__}"
