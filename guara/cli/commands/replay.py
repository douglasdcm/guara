import importlib
from guara.transaction import Application


def load_driver(path: str):
    try:
        module_name, factory_name = path.split(":", 1)
    except ValueError as exc:
        raise ValueError(
            "Driver must use the format 'module:function'. "
            "Example: drivers:create_driver"
        ) from exc

    module = importlib.import_module(module_name)

    try:
        factory = getattr(module, factory_name)
    except AttributeError as exc:
        raise ValueError(
            f"Driver factory '{factory_name}' was not found "
            f"in module '{module_name}'."
        ) from exc

    return factory()

def replay(args):
    driver = load_driver(args.driver) if args.driver else None

    Application(driver).replay(
        args.file,
        transaction_id=args.id,
        resume=args.resume,
    )
