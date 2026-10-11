from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from bakery.backend.repository import DB, Repository
from bakery.backend.scenarios import scenario_sell


class SalesPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        top = QHBoxLayout()

        self.product = QComboBox()
        self.refresh()

        self.quantity = QDoubleSpinBox()
        self.quantity.setMaximum(999)
        self.quantity.setValue(1)

        self.discount = QDoubleSpinBox()
        self.discount.setMaximum(100)
        self.discount.setSuffix(" %")

        top.addWidget(QLabel("Produto [Product]"))
        top.addWidget(self.product)
        top.addWidget(QLabel("Quantidade [Quantity]"))
        top.addWidget(self.quantity)

        layout.addLayout(top)

        second = QHBoxLayout()
        second.addWidget(QLabel("Desconto [Discount]"))
        second.addWidget(self.discount)

        self.money = QDoubleSpinBox()
        self.money.setMaximum(100000)
        self.money.setPrefix("R$ ")

        second.addWidget(QLabel("Dinheiro [Money]"))
        second.addWidget(self.money)

        layout.addLayout(second)

        self.summary = QListWidget()
        layout.addWidget(self.summary)

        self.total = QLabel("TOTAL: R$ 0.00")
        self.total.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(self.total)

        finish = QPushButton("Finalizar Venda [Close sale]")
        finish.setMinimumHeight(48)
        finish.clicked.connect(self.sell)
        layout.addWidget(finish)

    def refresh(self):
        self.product.clear()

        for product in DB.list_products():
            self.product.addItem(product.name)

    def sell(self):
        try:
            product = Repository().get_product_by_name(self.product.currentText())
            sale = scenario_sell(
                product_id=product.id,
                quantity=self.quantity.value(),
                customer_id=None,
                delivery=None,
            )

            self.summary.addItem(
                f"{self.product.currentText()} x {self.quantity.value()}"
            )
            self.total.setText(f"TOTAL: R$ {sale.total:.2f}")

            QMessageBox.information(
                self, "Sucesso [Success]", "Venda registrada [Sold]"
            )

        except Exception as error:  # noqa
            QMessageBox.warning(self, "Erro [Error]", str(error))
