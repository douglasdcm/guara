from PySide6.QtWidgets import (
    QHeaderView,
    QInputDialog,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from bakery.backend.repository import DB
from bakery.backend.scenarios import scenario_add_stock


class StockPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            [
                "Produto [Product]",
                "Estoque [Stock]",
                "Mínimo [Minimum]",
                "Situação [Status]",
            ]
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        button = QPushButton("Adicionar Estoque [Add stock]")
        button.clicked.connect(self.increase_stock)

        layout.addWidget(self.table)
        layout.addWidget(button)

        self.refresh()

    def refresh(self):
        products = DB.list_products()
        self.table.setRowCount(len(products))

        for row, product in enumerate(products):
            status = "OK"
            if product.stock < product.minimum_stock:
                status = "Estoque baixo [Low stock]"

            self.table.setItem(row, 0, QTableWidgetItem(product.name))
            self.table.setItem(row, 1, QTableWidgetItem(str(product.stock)))
            self.table.setItem(row, 2, QTableWidgetItem(str(product.minimum_stock)))
            self.table.setItem(row, 3, QTableWidgetItem(status))

    def increase_stock(self):
        row = self.table.currentRow()
        if row < 0:
            return

        product_name = self.table.item(row, 0).text()

        quantity, ok = QInputDialog.getDouble(
            self,
            "Adicionar estoque [Add stock]",
            "Quantidade: [Quantity]",
            1,
            0,
            9999,
            2,
        )

        if ok:
            try:
                scenario_add_stock(product_name, quantity)
                self.refresh()
            except Exception as error:  # noqa
                QMessageBox.warning(self, "Erro [Error]", str(error))
