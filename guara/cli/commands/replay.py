from guara.transaction import Application


def replay(args):
    driver = getattr(args, "driver", None)
    Application(driver).replay(
        args.file,
        transaction_id=args.id,
        dry_run=args.dry_run,
        resume=args.resume,
    )
