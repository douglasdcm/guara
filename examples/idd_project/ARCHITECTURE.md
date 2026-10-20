# Gherkin Scenarios for a Bakery System Pilot using Guará

## Objective

Create a reusable core for bakeries that can be customized for different clients.

The main modules of the pilot should be: 

- Product registration
- Inventory control 
- Counter sales 
- Cash register 
- Customers 
- Reports 
- Purchasing and replenishment
- Expiration control
- Users and permissions 

```gherkin
Product Registration

Feature: Product registration 

Scenario: Register a new bakery product 
Given I am on the product registration screen 
When I enter: 
| name | French Bread | 
| category | Bakery | 
| price| 0.90 | 
| minimum stock| 100| 
And I click save
Then the product should be registered successfully
```

```gherkin
Scenario: Prevent duplicate product registration
Given a product named "French Bread" already exists 
When I try to register another product with the same name 
Then I should see the message "Product already registered"
```

```gherkin
Scenario: Change a product's price
Given the product "Carrot Cake" exists
When I change the price to "32.00"
Then the new price should be saved
```

```gherkin
Inventory Control 


Feature: Inventory control

Scenario: Add stock 
Given the product "Milk" exists 
And the current stock is 10 
When I register an entry of 20 units
Then the stock should become 30 
```

```gherkin
Scenario: Deduct stock after sale 
Given the product "French Bread" exists 
And the current stock is 200
When I sell 15 units
Then the stock should become 185
```

```gherkin
Scenario: Alert when stock is below minimum 
Given the product "Coffee" has a minimum stock of 10
And the current stock is 8
When I access the inventory panel 
Then the product should appear as "Low Stock" 
```

```gherkin
Scenario: Prevent sale without sufficient stock 
Given the product "Soda" has 2 units in stock 
When I try to sell 3 units
Then I should see the message "Insufficient stock"
```

```gherkin
Expiration Control 


Feature: Expiration control 

Scenario: Register a batch with an expiration date
Given the product "Ham" exists
When I register a batch expiring on "2026-05-01"
Then the batch should be associated with the product
```

```gherkin
Scenario: Alert for products nearing expiration 
Given a batch of "Cheese" expires in 3 days 
When I access the expiration panel
Then the batch should appear in the near-expiration list
```

```gherkin
Scenario: Prevent sale of expired product 
Given a batch of "Yogurt" is expired
When I try to make a sale 
Then I should see the message "Expired product" 
```
```gherkin
Counter Sales 


Feature: Counter sales

Scenario: Perform a simple sale 
Given the product "French Bread" exists 
When I add 10 units to the cart 
And I finalize the sale 
Then the sale should be registered
And the stock should be updated 
```

```gherkin
Scenario: Apply discount to a sale
Given a sale totaling 100.00
When I apply a 10% discount 
Then the final value should be 90.00
```

```gherkin
Scenario: Cancel an item from the sale
Given a sale with:
| item | quantity | 
| Soda | 2| 
| Snack| 3| 
When I remove the item "Soda" 
Then the sale should remain with only "Snack" 
```

```gherkin
Scenario: Finalize cash sale
Given the sale totals 25.00 
When the customer pays 30.00 in cash
Then the change should be 5.00
```

```gherkin
Scenario: Finalize sale with multiple payment methods 
Given the sale totals 100.00
When the customer pays: 
| method | value |
| Cash | 40.00 |
| Card | 60.00 |
Then the sale should be finalized successfully
```

```gherkin
Cash Register 


Feature: Cash register

Scenario: Open cash register
Given no cash register is open
When I open the cash register with an initial value of 200.00 
Then the cash register should be available for sales
```

```gherkin
Scenario: Prevent opening two cash registers simultaneously 
Given a cash register is already open 
When I try to open another cash register
Then I should see the message "A cash register is already open" 
```

```gherkin
Scenario: Register a cash withdrawal (sangria)
Given a cash register is open 
When I withdraw 100.00 from the register
Then the transaction should be recorded 
```

```gherkin
Scenario: Close cash register 
Given a cash register is open 
And the total sold for the day was 1500.00
When I close the cash register
Then the system should generate the daily summary 
```

```gherkin
Customers 


Feature: Customers

Scenario: Register a customer 
Given I am on the customers screen
When I register:
| name| John Doe| 
| phone | 31999999999 | 
Then the customer should be saved 
```

```gherkin
Scenario: Link sale to a customer 
Given the customer "John Doe" exists
When I perform a sale for this customer 
Then the sale should be associated with the customer
```

```gherkin
Scenario: Consult customer purchase history 
Given the customer "John Doe" has registered purchases
When I access the customer's history
Then I should see all purchases made
```

```gherkin

Purchasing and Replenishment


Feature: Purchasing and replenishment 

Scenario: Generate automatic purchase suggestion
Given the product "Flour" is below minimum stock
When I access the replenishment report
Then the product should appear as a purchase suggestion 
```

```gherkin
Scenario: Register purchase from supplier 
Given the supplier "Distribuidora Minas" exists 
When I register a purchase of 50 units of "Flour" 
Then the stock should be updated
```
```gherkin
Reports


Feature: Reports

Scenario: Consult best-selling products 
Given there are sales registered for the month
When I access the best-selling products report
Then I should see the products ordered by quantity sold 
```

```gherkin
Scenario: Consult daily revenue 
Given there are sales made today
When I access the daily financial report
Then I should see the total sold
```

```gherkin
Scenario: Consult profit per product
Given products have cost and sale prices
When I access the profit report 
Then I should see the margin for each product 
```
```gherkin
Users and Permissions 


Feature: Users and permissions

Scenario: Allow only manager to change prices 
Given a user with the "Attendant" profile 
When I try to change a product's price
Then I should see the message "Access denied" 
```

```gherkin
Scenario: Allow manager to close cash register
Given a user with the "Manager" profile 
When the manager closes the cash register 
Then the closing should be performed successfully 
```

```gherkin
Customization Scenarios per Client 


Scenario: Bakery that sells by weight 
Given the product "Cheese Bread" is sold by weight
When I enter 0.350 kg 
Then the system should calculate the proportional value 
```

```gherkin
Scenario: Bakery with delivery
Given a sale for delivery exists
When I enter the customer's address 
Then the sale should be marked as "Delivery"
```

```gherkin
Scenario: Bakery with tabs (comanda)
Given an open tab for table 10
When I add an item to the tab 
Then the item should remain pending until the tab is closed 
```

```gherkin
Scenario: Bakery with in-house production 
Given the recipe for "French Bread" exists
When I produce 100 units
Then the ingredients should be deducted from stock
```

## UI 

Desktop Bakery System using Python + Guará + PySide6

Objective

Transform the existing CLI scenarios into a simple, fast, and easy-to-use desktop application for a neighborhood bakery. 

### UX priority: 

- Few screens 
- Large buttons 
- Fast sales flow 
- Minimal text
- Clear messages
- Operation possible with mouse or keyboard 
- Local installation without internet 

### Project Structure 

```bash
bakery_app/ 
│ 
├── bakery/ 
│ ├── entities.py 
│ ├── repository.py 
│ ├── transactions.py 
│ ├── preconditions.py
│ ├── helpers.py
│ └── exceptions.py 
│ 
├── ui/ 
│ ├── main_window.py
│ ├── dashboard_page.py 
│ ├── products_page.py
│ ├── sales_page.py 
│ ├── stock_page.py 
│ ├── customers_page.py 
│ ├── cash_page.py
│ ├── expiration_page.py
│ ├── dialogs/
│ │ ├── create_product_dialog.py
│ │ ├── sell_dialog.py
│ │ ├── customer_dialog.py
│ │ └── batch_dialog.py 
│ └── components/ 
│ ├── menu_card.py
│ ├── notification.py 
│ └── table_widget.py 
│ 
├── app.py
└── requirements.txt
```

### Main Navigation

The application opens in a single window with a side menu. 

```bash
+------------------------------------------------+
| St. Joseph's Bakery|
+----------------------+-------------------------+
| Dashboard| |
| Products | Content |
| Inventory| |
| Sales| |
| Customers| |
| Cash Register| |
| Expiration | |
| Reports| |
+----------------------+-------------------------+
```

### Initial Screen (Dashboard) 

The first screen should show only the most important information:

- Cash register open/closed 
- Number of products with low stock 
- Products nearing expiration 
- Total sold today
- Quick shortcuts 

Example: 

```bash
[ Cash Register Open ] [ R$ 1,250 sold today ]

[ 3 products with low stock ] 
[ 2 products expiring today ] 

[ New Product ] [ New Sale ] [ Open Cash Register ] 
```

### Products Screen

## UX 

- Product list on the left
- Search field at the top 
- "New Product" button highlighted
- Clicking a product opens editing on the side

Fields:

- Name
- Category
- Price 
- Minimum stock 
- Sold by weight

Visual Example 

```bash
Search product: [____________]

+----------------------------------------------+
| French BreadR$ 0.90 Stock: 200 |
| Carrot Cake R$ 32.00Stock: 5 |
| CoffeeR$ 18.00Stock: 8 |
+----------------------------------------------+

[ New Product ] 
```

Example of Product Registration Screen 


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
self.name.setPlaceholderText("Product name")

self.price = QDoubleSpinBox() 
self.price.setMaximum(9999) 
self.price.setPrefix("R$ ") 

self.minimum_stock = QDoubleSpinBox() 
self.minimum_stock.setMaximum(9999) 

self.by_weight = QCheckBox("Sold by weight")

save_button = QPushButton("Save Product") 
save_button.clicked.connect(self.create_product)

layout.addWidget(QLabel("Name"))
layout.addWidget(self.name) 
layout.addWidget(QLabel("Price")) 
layout.addWidget(self.price)
layout.addWidget(QLabel("Minimum stock")) 
layout.addWidget(self.minimum_stock)
layout.addWidget(self.by_weight)
layout.addWidget(save_button) 

self.setLayout(layout)

def create_product(self): 
try:
user = User("user", "Manager")

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

QMessageBox.information(self, "Success", "Product created successfully")

except Exception as error:
QMessageBox.warning(self, "Error", str(error))
```

### Sales Screen

This is the most important screen in the application.

Recommended UX 

- Large search field
- List of sale items
- Total highlighted in large font 
- Keyboard shortcuts: 
- F2 = finalize
- ESC = cancel 
- F3 = add customer

```bash
Product: [ French Bread_________________ ]
Quantity: [10]

+--------------------------------------+
| Product Qty Value|
| French Bread 10 R$ 9.00|
+--------------------------------------+

Discount: [ 10% ] 

TOTAL: R$ 8.10

Payment:
[ Cash ] [ Card ] [ PIX ] 

[ Finalize Sale ] 
```

### Internal Flow of the Sales Screen 

```python
Application() 
.given(preconditions.HasStock, product_name=product, quantity=quantity) 
.and_(preconditions.IsProductInValidExpirationDate, product_name=product) 
.execute( 
transactions.RegisterSale,
items=[(product, quantity)],
customer_name=customer, 
discount=discount,
payments={
"Cash": cash, 
"Card": card, 
},
delivery=address, 
) 
```

### Inventory Screen

Show simple table: 

```bash
ProductStockMinimumStatus
────────────────────────────────── 
Coffee 810 Low stock 
Bread200100OK
```

The row should be: 

- Red if stock < minimum
- Yellow if near minimum

Button:

- Add Stock 

### Expiration Screen 

Table: 

```bash
ProductQuantityExpires in 
───────────────────────────── 
Cheese 5 3 days 
Ham10Tomorrow 
```

Rows:

- Red: expired
- Yellow: expires in up to 3 days 

### Cash Register Screen

Flow:

1 Open cash register
2 Register withdrawal 
3 Close cash register 

Screen:

```bash
Current Register: Open
Initial Value: R$ 200.00

Total Sold: R$ 1,500.00 

[ Register Withdrawal ] 
[ Close Cash Register ] 
```

### Reports

Reports should be simple and visually clear. 
```bash
Best-Selling Products Report 


1. French Bread - 1200
2. Coffee - 340 
3. Carrot Cake - 180
```

### Financial Report 

```bash
Today:
R$ 1,250.00 

Month:
R$ 21,000.00
```

### Low Stock Report 


- Coffee
- Milk
- Flour 


## Important UX Rules 

1 Never display a stack trace to the user.
2 Every error message must be simple: 
- "Product already registered" 
- "Insufficient stock" 
- "Expired product"
3 Every action must visually confirm success. 
4 The operator must be able to complete a sale in less than 10 seconds. 
5 The system must remain usable on a 1366x768 screen. 
6 Use large font (minimum 12pt).
7 Main buttons must be at least 44px high.

## Visual Style Suggestion

- Background: light gray
- Primary color: dark orange
- Success color: green
- Warning color: yellow 
- Error color: red

```bash
PRIMARY_COLOR = "#C96A00" 
SUCCESS_COLOR = "#2E7D32" 
WARNING_COLOR = "#F9A825" 
ERROR_COLOR = "#C62828"
```