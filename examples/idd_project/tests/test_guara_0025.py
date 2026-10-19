# from __future__ import annotations

# from types import SimpleNamespace

# import pytest
# from guara import it
# from guara.transaction import Application

# from bakery.backend import transactions
# from bakery.backend.database import engine
# from bakery.backend.models import Base


# @pytest.fixture(scope="function", autouse=True)
# def db():
#     Base.metadata.create_all(bind=engine)
#     yield
#     Base.metadata.drop_all(bind=engine)


# app = Application(driver=SimpleNamespace())


# def test_scenario_list_customers():
#     return (
#         app
#         # .given(preconditons.IsUserLoggedIn)
#         # .and_(preconditons.IsManager)
#         .when(transactions.ListCustomers)
#         .expects(it.IsNotNone)
#         .result
#     )
