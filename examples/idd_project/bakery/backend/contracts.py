from guara.transaction import AbstractTransaction


class EntityIsNotNone(AbstractTransaction):
    def do(self, **kwargs):
        for k, v in kwargs.items():
            if not v:
                raise RuntimeError(f"Entity '{k}' is None.")
