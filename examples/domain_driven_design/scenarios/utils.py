# Copyright (C) 2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

import logging

logging.getLogger(__name__)


def run_scenario(func):
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
            return True
        except Exception:
            app = args[0]
            if app:
                app.undo()
            raise

    return inner
