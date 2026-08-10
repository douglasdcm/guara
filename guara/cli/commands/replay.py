from guara.transaction import Application


def replay(args):
    driver = getattr(args, "driver", None)
    Application(driver).replay(
        args.file,
        transaction_id=args.id,
        resume=args.resume,
    )
