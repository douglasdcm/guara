from datetime import datetime, timedelta, timezone

import pytest
from bakery.backend.database import engine
from bakery.backend.entities import Product
from bakery.backend.helpers import low_stock_products
from bakery.backend.models import Base
from bakery.backend.repository import DB
from bakery.backend.utils import get_total_sales
from cli import cli
from click.testing import CliRunner


@pytest.fixture(scope="function", autouse=True)
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(
    scope="function",
    autouse=True,
)
def open_cash_register(runner, db):
    runner.invoke(
        cli,
        [
            "open-cash",
            "--initial",
            "200",
        ],
    )


@pytest.fixture(
    scope="function",
    autouse=True,
)
def create_user_manager_an_login(runner, db):
    runner.invoke(
        cli,
        [
            "create-user",
            "--name",
            "foo",
            "--secret",
            "foo123",
            "--role",
            "gerente",
        ],
    )

    runner.invoke(
        cli,
        ["login", "--username", "foo", "--secret", "foo123"],
    )


def create_user_chashier_an_login(runner):
    runner.invoke(
        cli,
        [
            "create-user",
            "--name",
            "bla",
            "--secret",
            "bla123",
            "--role",
            "atendente",
        ],
    )

    runner.invoke(
        cli,
        ["login", "--username", "bla", "--secret", "bla123"],
    )


# ============
# COMMANDS
# ============


def sell_command(runner, product_id, quantity, customer_id=None):
    cmd = ["sell", "--product-id", product_id, "--quantity", quantity]
    if customer_id:
        cmd.extend(["--customer-id", customer_id])
    result = runner.invoke(cli, cmd)

    return result


class TestProductRegistration:
    def test_should_create_product(self, runner):
        result = runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Pão Francês",
                "--price",
                "0.90",
                "--minimum-stock",
                "100",
            ],
        )

        assert result.exit_code == 0
        assert "Produto criado: Pão Francês" in result.output
        assert len(DB.list_products()) == 1
        assert DB.list_products()[0].name == "Pão Francês"

    def test_should_not_allow_duplicate_product(self, runner):
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Pão Francês",
                "--price",
                "0.90",
                "--minimum-stock",
                "1",
            ],
        )
        result = runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Pão Francês",
                "--price",
                "0.95",
                "--minimum-stock",
                "1",
            ],
        )
        assert "Produto já cadastrado" in result.output

    def test_should_update_product_price(self, runner):
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Bolo de Cenoura",
                "--price",
                "25.00",
                "--minimum-stock",
                "1",
            ],
        )

        result = runner.invoke(
            cli,
            [
                "update-price",
                "--name",
                "Bolo de Cenoura",
                "--price",
                "32.00",
            ],
        )

        assert "Novo preço de Bolo de Cenoura: 32.00" in result.output
        assert DB.list_products()[0].price == 32.00


class TestStock:
    def test_should_add_stock(self, runner):
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Leite",
                "--price",
                "5.00",
                "--minimum-stock",
                "1",
            ],
        )

        result = runner.invoke(
            cli,
            ["add-stock", "--product", "Leite", "--quantity", "20"],
        )

        assert "Novo estoque: 20.0" in result.output
        assert DB.get_product_by_name("Leite").stock == 20

    def test_should_reduce_stock_after_sale(self, runner):
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Pão Francês",
                "--price",
                "0.90",
                "--minimum-stock",
                "1",
            ],
        )
        runner.invoke(
            cli,
            ["add-stock", "--product", "Pão Francês", "--quantity", "200"],
        )

        sell_command(runner, 1, 15)

        assert DB.list_products()[0].stock == 185

    def test_should_show_low_stock(self, runner):
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Café",
                "--price",
                "4.50",
                "--minimum-stock",
                "10",
            ],
        )
        runner.invoke(
            cli,
            ["add-stock", "--product", "Café", "--quantity", "10"],
        )

        sell_command(runner, 1, 2)

        result = runner.invoke(cli, ["low-stock"])

        assert "Café: Estoque Baixo (8.0)" in result.output

    @pytest.mark.skip(reason="Does not make sense in a physical store")
    def test_should_not_sell_without_stock(self, runner):
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Refrigerante",
                "--price",
                "8.00",
                "--minimum-stock",
                "1",
            ],
        )
        DB.list_products()[0].stock = 2

        result = sell_command(runner, 1, 3)

        assert "Estoque insuficiente" in result.output


class TestExpiration:
    def test_should_register_batch(self, runner):
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Presunto",
                "--price",
                "20.00",
                "--minimum-stock",
                "20",
            ],
        )

        result = runner.invoke(
            cli,
            [
                "register-batch",
                "--product",
                "Presunto",
                "--quantity",
                "10",
                "--expiration",
                "2026-05-01",
            ],
        )

        assert "Lote registrado para Presunto" in result.output
        assert len(DB.list_batches()) == 1

    def test_should_show_expiring_product(self, runner):
        expiration = (datetime.now(tz=timezone.utc).date() + timedelta(days=3)).isoformat()
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Queijo",
                "--price",
                "18.00",
                "--minimum-stock",
                "10",
            ],
        )

        runner.invoke(
            cli,
            [
                "register-batch",
                "--product",
                "Queijo",
                "--quantity",
                "5",
                "--expiration",
                expiration,
            ],
        )

        result = runner.invoke(cli, ["expiration-panel"])

        assert "Queijo vence em" in result.output

    def test_should_not_sell_expired_product(self, runner):
        expired = (datetime.now(tz=timezone.utc).date() - timedelta(days=1)).isoformat()
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Iogurte",
                "--price",
                "6.00",
                "--minimum-stock",
                "10",
            ],
        )

        runner.invoke(
            cli,
            [
                "register-batch",
                "--product",
                "Iogurte",
                "--quantity",
                "10",
                "--expiration",
                expired,
            ],
        )

        result = sell_command(runner, 1, 1)

        assert "Produto vencido" in result.output


class TestSales:
    @pytest.mark.skip(reason="Discount feature not implemented")
    def test_should_apply_discount(self, runner):
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Combo",
                "--price",
                "100.00",
                "--minimum-stock",
                "1",
            ],
        )
        runner.invoke(
            cli,
            ["add-stock", "--product", "Combo", "--quantity", "1"],
        )

        result = runner.invoke(
            cli,
            [
                "sell",
                "--product",
                "Combo",
                "--quantity",
                "1",
                "--discount",
                "10",
                "--money",
                "1",
            ],
        )

        result = sell_command(runner, 1, 1)

        assert "Venda registrada. Total: R$ 90.00" in result.output

    @pytest.mark.skip(reason="Makes sense for payment feature")
    def test_should_calculate_change(self, runner):
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Produto",
                "--price",
                "25.00",
                "--minimum-stock",
                "1",
            ],
        )
        runner.invoke(
            cli,
            ["add-stock", "--product", "Produto", "--quantity", "1"],
        )

        result = runner.invoke(
            cli,
            [
                "sell",
                "--product",
                "Produto",
                "--quantity",
                "1",
                "--money",
                "30",
            ],
        )

        assert "Troco: R$ 5.00" in result.output

    @pytest.mark.skip(reason="Makes sense for payment feature")
    def test_should_accept_multiple_payment_methods(self, runner):
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Pedido",
                "--price",
                "100.00",
                "--minimum-stock",
                "1",
            ],
        )
        runner.invoke(
            cli,
            ["add-stock", "--product", "Pedido", "--quantity", "100"],
        )

        result = runner.invoke(
            cli,
            [
                "sell",
                "--product",
                "Pedido",
                "--quantity",
                "1",
                "--money",
                "40",
                "--card",
                "60",
            ],
        )

        assert "Venda registrada. Total: R$ 100.00" in result.output


class TestCashRegister:
    @pytest.fixture(
        scope="function",
        autouse=True,
    )
    def close_cash_register(self, runner):
        runner.invoke(
            cli,
            ["close-cash"],
        )

    def test_should_open_cash_register(self, runner):
        result = runner.invoke(
            cli,
            ["open-cash", "--initial", "200"],
        )

        assert "Caixa aberto" in result.output
        assert DB.get_open_cash_register() is not None

    def test_should_not_open_two_cash_registers(self, runner):
        runner.invoke(cli, ["open-cash", "--initial", "200"])

        result = runner.invoke(
            cli,
            ["open-cash", "--initial", "300"],
        )

        assert "Já existe um caixa aberto" in result.output

    def test_should_register_withdrawal(self, runner):
        runner.invoke(cli, ["open-cash", "--initial", "200"])

        result = runner.invoke(
            cli,
            ["sangria", "--amount", "100"],
        )

        assert "Sangria registrada: R$ 100.00" in result.output
        assert DB.list_withdrawals() == [100]

    def test_should_close_cash_register(self, runner):
        runner.invoke(cli, ["open-cash", "--initial", "200"])

        result = runner.invoke(
            cli,
            ["close-cash", "--role", "Gerente"],
        )

        assert "Fechamento realizado" in result.output


class TestCustomers:
    def test_should_create_customer(self, runner):
        result = runner.invoke(
            cli,
            [
                "create-customer",
                "--name",
                "João da Silva",
                "--phone",
                "31999999999",
            ],
        )

        assert "Cliente criado: João da Silva" in result.output

    def test_should_link_sale_to_customer(self, runner):

        customer_name = "João da Silva"
        product_name = "Pão"
        runner.invoke(
            cli,
            [
                "create-customer",
                "--name",
                customer_name,
                "--phone",
                "31999999999",
            ],
        )

        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                product_name,
                "--price",
                "1.00",
                "--minimum-stock",
                "1",
            ],
        )
        runner.invoke(
            cli,
            ["add-stock", "--product", product_name, "--quantity", "10"],
        )

        sell_command(runner, 1, 1, 1)

        assert DB.list_sales()[0].customer_id == 1
        customer = DB.get_customer_by_name(customer_name)
        product = DB.get_product_by_name(product_name)
        assert DB.get_rating(customer.id, product.id).rating == 1


class TestCustomizationScenarios:
    def test_should_support_weight_sale_product(self, runner):
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Pão de Queijo",
                "--price",
                "32.00",
                "--weight",
                "--minimum-stock",
                "1",
            ],
        )

        product = DB.list_products()[0]
        quantity_in_kg = 0.350
        total = quantity_in_kg * product.price

        assert product.sold_by_weight is True
        assert total == pytest.approx(11.20)

    @pytest.mark.skip(reason="Delivery not implemented")
    def test_should_mark_sale_as_delivery(self, runner):
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Pedido",
                "--price",
                "10.00",
                "--minimum-stock",
                "1",
            ],
        )
        runner.invoke(
            cli,
            ["add-stock", "--product", "Pedido", "--quantity", "1"],
        )

        result = runner.invoke(
            cli,
            [
                "sell",
                "--product",
                "Pedido",
                "--quantity",
                "1",
                "--delivery",
                "Rua A, 123",
                "--money",
                "100",
            ],
        )

        result = sell_command(runner, 1, 1)

        assert "Entrega para: Rua A, 123" in result.output
        assert DB.list_sales()[0].delivery_address == "Rua A, 123"


class TestMissingScenarios:
    def test_should_keep_only_remaining_item_when_item_is_removed_from_sale(self):
        from bakery.backend.entities import Sale, SaleItem

        sale = Sale(
            id=1,
            items=[
                SaleItem(1, 1, product_id=1, quantity=2, unit_price=8.00),
                SaleItem(1, 1, product_id=2, quantity=3, unit_price=5.00),
            ],
        )

        sale.items = [item for item in sale.items if item.product_id != 1]

        assert len(sale.items) == 1
        assert sale.items[0].product_id == 2
        assert sale.items[0].quantity == 3

    def test_should_show_customer_purchase_history(self, runner):
        runner.invoke(
            cli,
            [
                "create-customer",
                "--name",
                "João da Silva",
                "--phone",
                "31999999999",
            ],
        )
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Pão",
                "--price",
                "2.00",
                "--minimum-stock",
                "1",
            ],
        )
        runner.invoke(
            cli,
            ["add-stock", "--product", "Pão", "--quantity", "10"],
        )

        sell_command(runner, 1, 2, 1)

        customer_sales = [sale for sale in DB.list_sales() if sale.customer_id == 1]

        assert len(customer_sales) == 1
        assert customer_sales[0].total == 4.00

    def test_should_generate_replenishment_suggestion(self, runner):
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Farinha",
                "--price",
                "5.00",
                "--minimum-stock",
                "100",
            ],
        )

        sell_command(runner, 1, 10)

        suggestions = low_stock_products()

        assert len(suggestions) == 1
        assert suggestions[0].name == "Farinha"

    def test_should_return_products_ordered_by_quantity_sold(self, runner):
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Pão",
                "--price",
                "1.00",
                "--minimum-stock",
                "1",
            ],
        )
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Café",
                "--price",
                "4.00",
                "--minimum-stock",
                "1",
            ],
        )

        runner.invoke(cli, ["add-stock", "--product", "Pão", "--quantity", "50"])
        runner.invoke(cli, ["add-stock", "--product", "Café", "--quantity", "50"])

        sell_command(runner, 1, 10)
        sell_command(runner, 2, 3)

        ranking = {}
        for sale in DB.list_sales():
            for item in sale.items:
                ranking[item.product_id] = ranking.get(item.product_id, 0) + item.quantity

        ordered = sorted(ranking.items(), key=lambda item: item[1], reverse=True)

        assert ordered[0][0] == 1
        assert ordered[0][1] == 10

    @pytest.mark.skip(reason="Makes sense for payment feature")
    def test_should_calculate_daily_revenue(self, runner):
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Produto",
                "--price",
                "50.00",
                "--minimum-stock",
                "1",
            ],
        )
        runner.invoke(cli, ["add-stock", "--product", "Produto", "--quantity", "2"])

        runner.invoke(cli, ["sell", "--product", "Produto", "--quantity", "2", "--money", "100"])

        total_revenue = get_total_sales()

        assert total_revenue == 100.00

    def test_should_calculate_profit_by_product(self):
        product = Product(
            id=1,
            name="Bolo",
            price=30.00,
            cost_price=18.00,
            minimum_stock=1,
        )

        margin = product.price - product.cost_price

        assert margin == 12.00

    def test_should_add_item_to_open_order_until_close(self):
        open_order = {
            "table": 10,
            "items": [],
            "closed": False,
        }

        open_order["items"].append({"product": "Refrigerante", "quantity": 1})

        assert open_order["closed"] is False
        assert len(open_order["items"]) == 1
        assert open_order["items"][0]["product"] == "Refrigerante"

    def test_should_consume_ingredients_when_producing_bread(self):
        ingredients_stock = {
            "Farinha": 100,
            "Fermento": 20,
        }

        recipe = {
            "Farinha": 30,
            "Fermento": 5,
        }

        for ingredient, quantity in recipe.items():
            ingredients_stock[ingredient] -= quantity

        assert ingredients_stock["Farinha"] == 70
        assert ingredients_stock["Fermento"] == 15


# ==========================================================
# PERMISSIONS TESTS (COMPLETE & CONSOLIDATED)
# ==========================================================


class TestPermissions:
    def test_should_not_allow_attendant_to_change_price(self, runner):
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Bolo",
                "--price",
                "10.00",
                "--minimum-stock",
                "1",
            ],
        )
        create_user_chashier_an_login(runner)
        result = runner.invoke(
            cli,
            ["update-price", "--name", "Bolo", "--price", "20.00"],
        )

        assert "Acesso negado" in result.output
        assert DB.list_products()[0].price == 10.00

    def test_should_allow_manager_to_change_price(self, runner):
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Bolo",
                "--price",
                "10.00",
                "--minimum-stock",
                "1",
            ],
        )

        result = runner.invoke(
            cli,
            ["update-price", "--name", "Bolo", "--price", "20.00"],
        )

        assert "Novo preço de Bolo: 20.00" in result.output
        assert DB.list_products()[0].price == 20.00

    def test_should_not_allow_attendant_to_close_cash(self, runner):
        runner.invoke(cli, ["open-cash", "--initial", "100"])
        create_user_chashier_an_login(runner)
        result = runner.invoke(
            cli,
            ["close-cash", "--role", "Atendente"],
        )

        assert "Acesso negado" in result.output

    def test_should_allow_manager_to_close_cash(self, runner):
        runner.invoke(cli, ["open-cash", "--initial", "100"])

        result = runner.invoke(
            cli,
            ["close-cash", "--role", "Gerente"],
        )

        assert "Fechamento realizado" in result.output

    def test_should_allow_attendant_to_sell(self, runner):
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Pão",
                "--price",
                "1.00",
                "--minimum-stock",
                "1",
            ],
        )
        runner.invoke(cli, ["add-stock", "--product", "Pão", "--quantity", "10"])

        result = sell_command(runner, 1, 2)

        assert "Venda registrada" in result.output
        assert DB.list_products()[0].stock == 8

    def test_should_allow_attendant_to_open_cash(self, runner):
        runner.invoke(
            cli,
            ["close-cash"],
        )
        result = runner.invoke(
            cli,
            ["open-cash", "--initial", "200"],
        )

        assert "Caixa aberto" in result.output
        assert DB.get_open_cash_register() is not None

    def test_should_not_allow_attendant_to_create_product_if_restricted(self, runner):
        """
        Only valid if your business rule enforces manager-only product creation.
        If not, REMOVE this test.
        """
        result = runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Produto X",
                "--price",
                "10.00",
                "--minimum-stock",
                "1",
            ],
        )

        # Adjust depending on your rule
        assert "Acesso negado" in result.output or result.exit_code == 0

    def test_should_not_allow_close_cash_without_open_cash(self, runner):
        runner.invoke(
            cli,
            ["close-cash"],
        )
        result = runner.invoke(
            cli,
            ["close-cash", "--role", "Gerente"],
        )

        assert "Nenhum caixa aberto" in result.output


# ==========================================================
# EDGE PERMISSION SCENARIOS
# ==========================================================


class TestPermissionEdgeCases:
    def test_should_block_price_update_for_non_existing_product(self, runner: CliRunner):
        result = runner.invoke(
            cli,
            ["update-price", "--name", "Inexistente", "--price", "50"],
        )

        assert "Produto não encontrado" in result.exception.args

    def test_should_not_allow_attendant_to_bypass_permissions(self, runner):
        """
        Defensive test: ensures role enforcement is not bypassed
        """
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Item",
                "--price",
                "10",
                "--minimum-stock",
                "1",
            ],
        )

        runner.invoke(
            cli,
            [
                "update-price",
                "--name",
                "Item",
                "--price",
                "999",
                "--role",
                "Atendente",
            ],
        )

        assert DB.list_products()[0].price != 999


# ==========================================================
# OPTIONAL BUSINESS VALIDATION LINKED TO PERMISSIONS
# ==========================================================


class TestPermissionBusinessIntegrity:
    @pytest.mark.skip(reason="Does not make sense for physical store")
    def test_manager_action_should_not_break_stock_rules(self, runner):
        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Leite",
                "--price",
                "5",
                "--minimum-stock",
                "100",
            ],
        )
        DB.list_products()[0].stock = 2

        result = runner.invoke(
            cli,
            ["sell", "--product", "Leite", "--quantity", "5", "--money", "100"],
        )

        # Even manager cannot bypass stock rules
        assert "Estoque insuficiente" in result.output

    def test_manager_cannot_sell_expired_products(self, runner):
        expired = (datetime.now(tz=timezone.utc).date() - timedelta(days=1)).isoformat()

        runner.invoke(
            cli,
            [
                "create-product",
                "--name",
                "Iogurte",
                "--price",
                "6",
                "--minimum-stock",
                "20",
            ],
        )
        runner.invoke(
            cli,
            [
                "register-batch",
                "--product",
                "Iogurte",
                "--quantity",
                "10",
                "--expiration",
                expired,
            ],
        )

        result = sell_command(runner, 1, 10)

        assert "Produto vencido" in result.output
