# Cenários Gherkin para um Piloto de Sistema de Padaria usando Guará

## Objetivo

Criar um núcleo reutilizável para padarias que possa ser customizado para diferentes clientes.

Os módulos principais do piloto devem ser:

* Cadastro de produtos
* Controle de estoque
* Vendas no balcão
* Caixa
* Clientes
* Relatórios
* Compras e reposição
* Controle de validade
* Usuários e permissões


# Cadastro de Produtos

```gherkin
Feature: Cadastro de produtos

  Scenario: Cadastrar um novo produto de padaria
    Given que estou na tela de cadastro de produtos
    When informo:
      | nome           | Pão Francês |
      | categoria      | Padaria     |
      | preço          | 0.90        |
      | estoque mínimo | 100         |
    And clico em salvar
    Then o produto deve ser cadastrado com sucesso
```

```gherkin
Scenario: Impedir cadastro de produto duplicado
  Given que já existe um produto chamado "Pão Francês"
  When tento cadastrar outro produto com o mesmo nome
  Then devo ver a mensagem "Produto já cadastrado"
```

```gherkin
Scenario: Alterar preço de um produto
  Given que existe o produto "Bolo de Cenoura"
  When altero o preço para "32.00"
  Then o novo preço deve ser salvo
```


# Controle de Estoque

```gherkin
Feature: Controle de estoque

  Scenario: Dar entrada em estoque
    Given que existe o produto "Leite"
    And o estoque atual é 10
    When registro entrada de 20 unidades
    Then o estoque deve passar para 30
```

```gherkin
Scenario: Dar baixa no estoque após venda
  Given que existe o produto "Pão Francês"
  And o estoque atual é 200
  When realizo a venda de 15 unidades
  Then o estoque deve passar para 185
```

```gherkin
Scenario: Alertar estoque abaixo do mínimo
  Given que o produto "Café" possui estoque mínimo de 10
  And o estoque atual é 8
  When acesso o painel de estoque
  Then o produto deve aparecer como "Estoque Baixo"
```

```gherkin
Scenario: Impedir venda sem estoque suficiente
  Given que o produto "Refrigerante" possui 2 unidades em estoque
  When tento vender 3 unidades
  Then devo ver a mensagem "Estoque insuficiente"
```


# Controle de Validade

```gherkin
Feature: Controle de validade

  Scenario: Registrar lote com data de validade
    Given que existe o produto "Presunto"
    When registro um lote com validade em "2026-05-01"
    Then o lote deve ficar associado ao produto
```

```gherkin
Scenario: Alertar produtos próximos do vencimento
  Given que existe um lote de "Queijo" vencendo em 3 dias
  When acesso o painel de validade
  Then o lote deve aparecer na lista de vencimento próximo
```

```gherkin
Scenario: Impedir venda de produto vencido
  Given que existe um lote de "Iogurte" vencido
  When tento realizar a venda
  Then devo ver a mensagem "Produto vencido"
```


# Venda no Balcão

```gherkin
Feature: Venda no balcão

  Scenario: Realizar venda simples
    Given que existe o produto "Pão Francês"
    When adiciono 10 unidades ao carrinho
    And finalizo a venda
    Then a venda deve ser registrada
    And o estoque deve ser atualizado
```

```gherkin
Scenario: Aplicar desconto na venda
  Given que existe uma venda no valor de 100.00
  When aplico desconto de 10%
  Then o valor final deve ser 90.00
```

```gherkin
Scenario: Cancelar item da venda
  Given que existe uma venda com:
    | item         | quantidade |
    | Refrigerante | 2          |
    | Salgado      | 3          |
  When removo o item "Refrigerante"
  Then a venda deve permanecer apenas com "Salgado"
```

```gherkin
Scenario: Finalizar venda em dinheiro
  Given que a venda totaliza 25.00
  When o cliente paga 30.00 em dinheiro
  Then o troco deve ser 5.00
```

```gherkin
Scenario: Finalizar venda com múltiplas formas de pagamento
  Given que a venda totaliza 100.00
  When o cliente paga:
    | forma      | valor |
    | Dinheiro   | 40.00 |
    | Cartão     | 60.00 |
  Then a venda deve ser finalizada com sucesso
```


# Caixa

```gherkin
Feature: Caixa

  Scenario: Abrir caixa
    Given que não existe caixa aberto
    When abro o caixa com valor inicial de 200.00
    Then o caixa deve ficar disponível para vendas
```

```gherkin
Scenario: Impedir abrir dois caixas simultaneamente
  Given que já existe um caixa aberto
  When tento abrir outro caixa
  Then devo ver a mensagem "Já existe um caixa aberto"
```

```gherkin
Scenario: Registrar sangria
  Given que existe um caixa aberto
  When retiro 100.00 do caixa
  Then a movimentação deve ser registrada
```

```gherkin
Scenario: Fechar caixa
  Given que existe um caixa aberto
  And o total vendido no dia foi 1500.00
  When fecho o caixa
  Then o sistema deve gerar o resumo do dia
```


# Clientes

```gherkin
Feature: Clientes

  Scenario: Cadastrar cliente
    Given que estou na tela de clientes
    When cadastro:
      | nome      | João da Silva |
      | telefone  | 31999999999   |
    Then o cliente deve ser salvo
```

```gherkin
Scenario: Vincular venda a cliente
  Given que existe o cliente "João da Silva"
  When realizo uma venda para esse cliente
  Then a venda deve ficar associada ao cliente
```

```gherkin
Scenario: Consultar histórico de compras do cliente
  Given que o cliente "João da Silva" possui compras registradas
  When acesso o histórico do cliente
  Then devo visualizar todas as compras realizadas
```


# Compras e Reposição

```gherkin
Feature: Compras e reposição

  Scenario: Gerar sugestão automática de compra
    Given que o produto "Farinha" está abaixo do estoque mínimo
    When acesso o relatório de reposição
    Then o produto deve aparecer como sugestão de compra
```

```gherkin
Scenario: Registrar compra de fornecedor
  Given que existe o fornecedor "Distribuidora Minas"
  When registro uma compra de 50 unidades de "Farinha"
  Then o estoque deve ser atualizado
```


# Relatórios

```gherkin
Feature: Relatórios

  Scenario: Consultar produtos mais vendidos
    Given que existem vendas registradas no mês
    When acesso o relatório de produtos mais vendidos
    Then devo visualizar os produtos ordenados pela quantidade vendida
```

```gherkin
Scenario: Consultar faturamento diário
  Given que existem vendas realizadas hoje
  When acesso o relatório financeiro do dia
  Then devo visualizar o total vendido
```

```gherkin
Scenario: Consultar lucro por produto
  Given que os produtos possuem preço de custo e venda
  When acesso o relatório de lucro
  Then devo visualizar a margem de cada produto
```


# Usuários e Permissões

```gherkin
Feature: Usuários e permissões

  Scenario: Permitir apenas gerente alterar preços
    Given que existe um usuário com perfil "Atendente"
    When tento alterar o preço de um produto
    Then devo ver a mensagem "Acesso negado"
```

```gherkin
Scenario: Permitir gerente fechar caixa
  Given que existe um usuário com perfil "Gerente"
  When o gerente fecha o caixa
  Then o fechamento deve ser realizado com sucesso
```


# Cenários de Customização por Cliente

```gherkin
Scenario: Padaria que vende por peso
  Given que o produto "Pão de Queijo" é vendido por peso
  When informo 0.350 kg
  Then o sistema deve calcular o valor proporcional
```

```gherkin
Scenario: Padaria com entrega
  Given que existe uma venda para entrega
  When informo o endereço do cliente
  Then a venda deve ser marcada como "Entrega"
```

```gherkin
Scenario: Padaria com comanda
  Given que existe uma comanda aberta para a mesa 10
  When adiciono um item na comanda
  Then o item deve ficar pendente até o fechamento
```

```gherkin
Scenario: Padaria com produção própria
  Given que existe a receita do produto "Pão Francês"
  When produzo 100 unidades
  Then os ingredientes devem ser baixados do estoque
```


# UI

# Sistema Desktop de Padaria usando Python + Guará + PySide6

## Objetivo

Transformar os cenários existentes da CLI em uma aplicação desktop simples, rápida e fácil de usar por uma padaria de bairro.

A prioridade de UX é:

* poucas telas
* botões grandes
* fluxo rápido de venda
* pouco texto
* mensagens claras
* operação possível com mouse ou teclado
* instalação local sem internet


# Estrutura do Projeto

```text
bakery_app/
│
├── bakery/
│   ├── entities.py
│   ├── repository.py
│   ├── transactions.py
│   ├── preconditions.py
│   ├── helpers.py
│   └── exceptions.py
│
├── ui/
│   ├── main_window.py
│   ├── dashboard_page.py
│   ├── products_page.py
│   ├── sales_page.py
│   ├── stock_page.py
│   ├── customers_page.py
│   ├── cash_page.py
│   ├── expiration_page.py
│   ├── dialogs/
│   │   ├── create_product_dialog.py
│   │   ├── sell_dialog.py
│   │   ├── customer_dialog.py
│   │   └── batch_dialog.py
│   └── components/
│       ├── menu_card.py
│       ├── notification.py
│       └── table_widget.py
│
├── app.py
└── requirements.txt
```


# Navegação Principal

A aplicação abre em uma única janela com menu lateral.

```text
+------------------------------------------------+
| Padaria São José                               |
+----------------------+-------------------------+
| Dashboard            |                         |
| Produtos             |     Conteúdo            |
| Estoque              |                         |
| Vendas               |                         |
| Clientes             |                         |
| Caixa                |                         |
| Validade             |                         |
| Relatórios           |                         |
+----------------------+-------------------------+
```


# Tela Inicial (Dashboard)

A primeira tela deve mostrar apenas as informações mais importantes:

* Caixa aberto / fechado
* Quantidade de produtos com estoque baixo
* Produtos próximos do vencimento
* Total vendido hoje
* Atalhos rápidos

Exemplo:

```text
[ Caixa Aberto ]     [ R$ 1.250 vendidos hoje ]

[ 3 produtos com estoque baixo ]
[ 2 produtos vencendo hoje ]

[ Novo Produto ] [ Nova Venda ] [ Abrir Caixa ]
```


# Tela de Produtos

## UX

* Lista de produtos à esquerda
* Campo de busca no topo
* Botão “Novo Produto” destacado
* Ao clicar no produto, abre edição na lateral

Campos:

* Nome
* Categoria
* Preço
* Estoque mínimo
* Vendido por peso

## Exemplo visual

```text
Buscar produto: [____________]

+----------------------------------------------+
| Pão Francês       R$ 0,90     Estoque: 200   |
| Bolo de Cenoura   R$ 32,00    Estoque: 5     |
| Café              R$ 18,00    Estoque: 8     |
+----------------------------------------------+

[ Novo Produto ]
```


# Exemplo de Tela de Cadastro de Produto

```python
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QDoubleSpinBox,
    QCheckBox,
    QMessageBox,
)

from guara.transaction import Application
from bakery import transactions, preconditions
from bakery.entities import User


class CreateProductPage(QWidget):
    def __init__(self):
        super().__init__()

        self.app = Application()

        layout = QVBoxLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Nome do produto")

        self.price = QDoubleSpinBox()
        self.price.setMaximum(9999)
        self.price.setPrefix("R$ ")

        self.minimum_stock = QDoubleSpinBox()
        self.minimum_stock.setMaximum(9999)

        self.by_weight = QCheckBox("Vendido por peso")

        save_button = QPushButton("Salvar Produto")
        save_button.clicked.connect(self.create_product)

        layout.addWidget(QLabel("Nome"))
        layout.addWidget(self.name)
        layout.addWidget(QLabel("Preço"))
        layout.addWidget(self.price)
        layout.addWidget(QLabel("Estoque mínimo"))
        layout.addWidget(self.minimum_stock)
        layout.addWidget(self.by_weight)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def create_product(self):
        try:
            user = User("usuario", "Gerente")

            (
                self.app.given(preconditions.HasManagerAccess, user=user)
                .and_(preconditions.HasNotRegistredProduct, name=self.name.text())
                .execute(
                    transactions.CreateProduct,
                    name=self.name.text(),
                    price=self.price.value(),
                    minimum_stock=self.minimum_stock.value(),
                    sold_by_weight=self.by_weight.isChecked(),
                )
            )

            QMessageBox.information(self, "Sucesso", "Produto criado com sucesso")

        except Exception as error:
            QMessageBox.warning(self, "Erro", str(error))
```


# Tela de Venda

Esta é a tela mais importante da aplicação.

## UX recomendado

* Campo de busca grande
* Lista de itens da venda
* Total destacado em fonte grande
* Atalhos de teclado:

  * F2 = finalizar
  * ESC = cancelar
  * F3 = adicionar cliente

```text
Produto: [ Pão Francês_________________ ]
Quantidade: [10]

+--------------------------------------+
| Produto         Qtde      Valor      |
| Pão Francês      10       R$ 9,00    |
+--------------------------------------+

Desconto: [ 10% ]

TOTAL: R$ 8,10

Pagamento:
[ Dinheiro ] [ Cartão ] [ PIX ]

[ Finalizar Venda ]
```


# Fluxo Interno da Tela de Venda

```python
Application()
    .given(preconditions.HasStock, product_name=produto, quantity=quantidade)
    .and_(preconditions.IsProductInValidExpirationDate, product_name=produto)
    .execute(
        transactions.RegisterSale,
        items=[(produto, quantidade)],
        customer_name=cliente,
        discount=desconto,
        payments={
            "Dinheiro": dinheiro,
            "Cartão": cartao,
        },
        delivery=endereco,
    )
```


# Tela de Estoque

Mostrar tabela simples:

| Produto | Estoque | Mínimo | Situação      |
| ------- | ------- | ------ | ------------- |
| Café    | 8       | 10     | Estoque baixo |
| Pão     | 200     | 100    | OK            |

A linha deve ficar:

* vermelha se estoque < mínimo
* amarela se próximo do mínimo

Botão:

* Adicionar Estoque


# Tela de Validade

Tabela:

| Produto  | Quantidade | Vence em |
| -------- | ---------- | -------- |
| Queijo   | 5          | 3 dias   |
| Presunto | 10         | Amanhã   |

Linhas:

* vermelha: vencido
* amarela: vence em até 3 dias


# Tela de Caixa

Fluxo:

1. Abrir caixa
2. Registrar sangria
3. Fechar caixa

Tela:

```text
Caixa Atual: Aberto
Valor Inicial: R$ 200,00

Total Vendido: R$ 1.500,00

[ Registrar Sangria ]
[ Fechar Caixa ]
```


# Relatórios

Os relatórios devem ser simples e visualmente claros.

## Relatório de Produtos Mais Vendidos

```text
1. Pão Francês - 1200
2. Café - 340
3. Bolo de Cenoura - 180
```

## Relatório Financeiro

```text
Hoje:
R$ 1.250,00

Mês:
R$ 21.000,00
```

## Relatório de Estoque Baixo

```text
- Café
- Leite
- Farinha
```


# Regras de UX importantes

1. Nunca exibir stack trace para o usuário.
2. Toda mensagem de erro deve ser simples:

   * “Produto já cadastrado”
   * “Estoque insuficiente”
   * “Produto vencido”
3. Toda ação deve confirmar visualmente o sucesso.
4. O operador deve conseguir concluir uma venda em menos de 10 segundos.
5. O sistema deve continuar utilizável em tela 1366x768.
6. Usar fonte grande (mínimo 12pt).
7. Botões principais devem ter no mínimo 44px de altura.


# Sugestão de Estilo Visual

* Fundo: cinza claro
* Cor principal: laranja escuro
* Cor de sucesso: verde
* Cor de alerta: amarelo
* Cor de erro: vermelho

```python
PRIMARY_COLOR = "#C96A00"
SUCCESS_COLOR = "#2E7D32"
WARNING_COLOR = "#F9A825"
ERROR_COLOR = "#C62828"
BACKGROUND = "#F5F5F5"
```


# Inicialização da Aplicação

```python
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


if __name__ == "__main__":
    qt = QApplication([])

    window = MainWindow()
    window.showMaximized()

    qt.exec()
```


# Próximo Passo Recomendado

Implementar primeiro apenas 4 telas:

1. Produtos
2. Vendas
3. Estoque
4. Caixa

Com isso já é possível fazer um piloto utilizável em uma padaria real.

Depois adicionar:

* clientes
* validade
* relatórios
* comanda
* produção própria
* licenciamento por cliente


Recommendation

sqlite3 bakery.db ".read /home/douglas/repo/padaria/bakery/plugins/recomendation/data-demo.sql"

Plan
- save data to vector database (faiss)
    - which data is important to vectorize?
    - it is expensive
- before complete the sales get recomendations (raw)
- build the prompt to LLM
- validate the prompt manually in chatgpt
- feed LLM
- validate LLM output using rules
- fallback



Feature: Access control based on user roles
  In order to protect critical operations
  As a system
  I want to restrict actions based on user roles (Cashier and Manager)


  # ==========================================================
  # MANAGER PERMISSIONS
  # ==========================================================

  Scenario: Manager creates a new product
    Given a user with role "Gerente"
    And the product "Pão Francês" is not registered
    When the user creates a product with name "Pão Francês" and price 0.90
    Then the product should be successfully created

  Scenario: Manager updates product price
    Given a user with role "Gerente"
    And a product "Bolo" with price 20.00 exists
    When the user updates the price to 32.00
    Then the product price should be updated to 32.00

  Scenario: Manager closes the cash register
    Given a user with role "Gerente"
    And the cash register is open
    When the user closes the cash register
    Then the cash register should be closed


  # ==========================================================
  # CASHIER (ATENDENTE) RESTRICTIONS
  # ==========================================================

  Scenario: Cashier tries to create a product
    Given a user with role "Atendente"
    When the user tries to create a product "Pão Francês"
    Then the operation should be denied
    And an "Acesso negado" message should be shown

  Scenario: Cashier tries to update product price
    Given a user with role "Atendente"
    And a product "Bolo" with price 20.00 exists
    When the user tries to update the price to 30.00
    Then the operation should be denied
    And an "Acesso negado" message should be shown

  Scenario: Cashier tries to close cash register
    Given a user with role "Atendente"
    And the cash register is open
    When the user tries to close the cash register
    Then the operation should be denied
    And an "Acesso negado" message should be shown


  # ==========================================================
  # SHARED PERMISSIONS
  # ==========================================================

  Scenario Outline: User registers a sale
    Given a user with role "<role>"
    And a product "Pão" with price 1.00 and stock 10
    When the user sells 2 units of "Pão"
    Then the sale should be registered
    And the stock should be reduced to 8

    Examples:
      | role       |
      | Gerente    |
      | Atendente  |

  Scenario Outline: User opens cash register
    Given a user with role "<role>"
    And there is no open cash register
    When the user opens the cash register with initial value 200
    Then the cash register should be opened

    Examples:
      | role       |
      | Gerente    |
      | Atendente  |

  Scenario Outline: User adds stock to product
    Given a user with role "<role>"
    And a product "Leite" exists
    When the user adds 20 units to stock
    Then the product stock should be 20

    Examples:
      | role       |
      | Gerente    |
      | Atendente  |


  # ==========================================================
  # SECURITY / EDGE CASES
  # ==========================================================

  Scenario: User cannot escalate privileges
    Given a user with role "Atendente"
    When the user attempts to perform a manager-only action
    Then the operation should be denied

  Scenario: System validates role before executing restricted actions
    Given a restricted operation
    When a user without permission executes it
    Then the system must block the execution


create database
# run once
from bakery.backend.database import engine
from bakery.backend.models import Base

Base.metadata.create_all(bind=engine)