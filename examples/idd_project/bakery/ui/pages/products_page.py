from PySide6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from bakery.backend.repository import DB
from bakery.ui.dialogs.product_dialog import ProductDialog


class ProductsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        top = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Buscar produto [Seach product]")
        self.search.textChanged.connect(self.refresh)

        new_button = QPushButton("Novo Produto [New product]")
        self.new_button = new_button
        new_button.clicked.connect(self.create_product)

        top.addWidget(self.search)
        top.addWidget(new_button)

        self.products = QListWidget()

        layout.addLayout(top)
        layout.addWidget(self.products)

        self.refresh()

    def refresh(self):
        self.products.clear()

        text = self.search.text().lower()

        for product in DB.list_products():
            if text and text not in product.name.lower():
                continue

            self.products.addItem(
                f"{product.name} - R$ {product.price:.2f} - Estoque: {product.stock} [Stock]"
            )

    def create_product(self):
        dialog = ProductDialog(self)
        self.dialog = dialog

        if dialog.exec():
            QMessageBox.information(
                self, "Sucesso [Success]", "Produto criado [Created]"
            )
            self.refresh()
