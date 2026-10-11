from __future__ import annotations

import click
from bakery.backend.exceptions import BusinessError
from bakery.backend.helpers import expiring_batches, low_stock_products
from bakery.backend.repository import DB
from bakery.backend.scenarios import (
    scenario_add_stock,
    scenario_close_cash,
    scenario_create_customer,
    scenario_create_product,
    scenario_create_user,
    scenario_list_customers,
    scenario_list_products,
    scenario_list_sales,
    scenario_list_users,
    scenario_login_user,
    scenario_open_cash,
    scenario_recommend_products,
    scenario_register_batch,
    scenario_sangria_withdraw_cash,
    scenario_sell,
    scenario_update_price,
)
from bakery.claude.cli_orchestrator import handle_user_input

from guara import LOGGER

# ==========================================================
# CLICK CLI
# ==========================================================


@click.group()
def cli():
    """Sistema de Padaria usando Guará. [Bakry system]"""


@cli.command()
@click.option("--username", required=True)
@click.option("--secret", required=True)
def login(username, secret):
    try:
        user = scenario_login_user(username, secret)
        click.echo(f"Logado como {user.name} ({user.role})")
    except BusinessError as e:
        click.echo(str(e))


@cli.command()
@click.option("--name", required=True)
@click.option("--secret", required=True)
@click.option("--role", default="Atendente")
def create_user(name, secret, role):
    try:
        scenario_create_user(name, secret, role)
        click.echo(f"Usuário criado: {name}")
    except BusinessError as error:
        click.echo(str(error))


@cli.command()
@click.option("--name", required=True)
@click.option("--price", type=float, required=True)
@click.option("--minimum-stock", type=float, required=True)
@click.option("--weight", is_flag=True)
def create_product(name, price, minimum_stock, weight):
    try:
        scenario_create_product(name, price, minimum_stock, weight)
        click.echo(f"Produto criado: {name}")
    except BusinessError as error:
        click.echo(str(error))


@cli.command()
@click.option("--name", required=True)
@click.option("--price", type=float, required=True)
def update_price(name, price):
    try:
        scenario_update_price(name, price)
        click.echo(f"Novo preço de {name}: {price:.2f}")
    except BusinessError as error:
        click.echo(str(error))


@cli.command()
@click.option("--product", required=True)
@click.option("--quantity", type=float, required=True)
def add_stock(product, quantity):
    try:
        stock = scenario_add_stock(product, quantity)
        click.echo(f"Novo estoque: {stock}")
    except BusinessError as error:
        click.echo(str(error))


@cli.command()
@click.option("--name", required=True)
@click.option("--phone", required=True)
def create_customer(name, phone):
    scenario_create_customer(name, phone)
    click.echo(f"Cliente criado: {name}")


@cli.command()
@click.option("--product-id", required=True)
@click.option("--quantity", type=float, required=True)
@click.option("--customer-id")
@click.option("--delivery")
def sell(product_id, quantity, customer_id, delivery):
    try:
        sale = scenario_sell(product_id, quantity, customer_id, delivery)
        click.echo(f"Venda registrada. Total: R$ {sale.total:.2f}")
        if delivery:
            click.echo(f"Entrega para: {delivery}")
    except BusinessError as error:
        click.echo(str(error))


@cli.command()
@click.option("--sale-id", type=int, required=True)
@click.option("--money", type=int)
@click.option("--card", type=int)
def pay(sale_id, money, card):
    sale = DB.get_sale_by_id(sale_id)
    if money > sale.total:
        click.echo(f"Troco: R$ {money - sale.total:.2f}")


@cli.command()
@click.option("--product-id", type=int, required=True)
@click.option("--customer-id", type=int, required=True)
def recommend(product_id, customer_id):
    try:
        recommendation = scenario_recommend_products(customer_id, product_id)
        LOGGER.info(f"Gostaria de levar {recommendation}?")
    except BusinessError as error:
        click.echo(str(error))


@cli.command()
@click.option("--initial", type=float, required=True)
def open_cash(initial):
    try:
        scenario_open_cash(initial)
        click.echo("Caixa aberto")
    except BusinessError as error:
        click.echo(str(error))


@cli.command()
@click.option("--amount", type=float, required=True)
def sangria(amount):
    scenario_sangria_withdraw_cash(amount)
    click.echo(f"Sangria registrada: R$ {amount:.2f}")


@cli.command()
@click.option("--role", default="Gerente")
def close_cash(role):
    try:
        result = scenario_close_cash(role)

        click.echo(
            f"Fechamento realizado. Total vendido: R$ {result['total_sales']:.2f}"
        )
    except BusinessError as error:
        click.echo(str(error))


@cli.command()
def low_stock():
    for product in low_stock_products():
        click.echo(f"{product.name}: Estoque Baixo ({product.stock})")


@cli.command()
def expiration_panel():
    for batch in expiring_batches():
        product = DB.get_product_by_id(batch.product_id)
        click.echo(f"{product.name} vence em {batch.expiration_date.isoformat()}")


@cli.command()
@click.option("--product", required=True)
@click.option("--quantity", type=float, required=True)
@click.option("--expiration", required=True)
def register_batch(product, quantity, expiration):
    scenario_register_batch(product, quantity, expiration)
    click.echo(f"Lote registrado para {product} com validade {expiration}")


# LISTS


@cli.command()
def list_products():
    products = scenario_list_products()
    click.echo("Produto")
    for product in products:
        click.echo(f"{product}")


@cli.command()
def list_users():
    users = scenario_list_users()
    click.echo("Nome | Função")
    for user in users:
        click.echo(f"{user}")


@cli.command()
def list_customers():
    customers = scenario_list_customers()
    click.echo("Nome | CPF")
    for customer in customers:
        click.echo(f"{customer}")


@cli.command()
def list_sales():
    sales = scenario_list_sales()
    click.echo("Vendas")
    for sale in sales:
        click.echo(f"{sale}")


cli.add_command(handle_user_input, "claude")

if __name__ == "__main__":
    cli()
