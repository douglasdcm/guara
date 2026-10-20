from __future__ import annotations

from datetime import datetime, timedelta, timezone

from bakery.backend.repository import DB
from guara.transaction import IAssertion

# ==========================================================
# ASSERTIONS
# ==========================================================


class IsGreatherThanOrEqualTo(IAssertion):
    def asserts(self, actual, expected):
        return actual >= expected


# ==========================================================
# REPORTS
# ==========================================================


def low_stock_products():
    return [product for product in DB.list_products() if product.stock < product.minimum_stock]


def expiring_batches(days=3):
    limit = datetime.now(tz=timezone.utc).date() + timedelta(days=days)
    return [
        batch
        for batch in DB.list_batches()
        if datetime.now(tz=timezone.utc).date() <= batch.expiration_date <= limit
    ]
