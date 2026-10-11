from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDoubleSpinBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from bakery.backend.scenarios import scenario_create_product


class ProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Novo Produto [New product]")

        layout = QVBoxLayout(self)

        self.name = QLineEdit()
        self.price = QDoubleSpinBox()
        self.price.setMaximum(10000)
        self.price.setPrefix("R$ ")

        self.minimum_stock = QDoubleSpinBox()
        self.minimum_stock.setMaximum(10000)

        self.by_weight = QCheckBox("Vendido por peso [Sold by weight]")

        save = QPushButton("Salvar [Save]")
        save.clicked.connect(self.save)
        self.save_button = save

        layout.addWidget(QLabel("Nome [Name]"))
        layout.addWidget(self.name)
        layout.addWidget(QLabel("Preço [Price]"))
        layout.addWidget(self.price)
        layout.addWidget(QLabel("Estoque mínimo [Minimu stock]"))
        layout.addWidget(self.minimum_stock)
        layout.addWidget(self.by_weight)
        layout.addWidget(save)

    def save(self):
        try:
            scenario_create_product(
                name=self.name.text(),
                price=self.price.value(),
                minimum_stock=self.minimum_stock.value(),
                weight=self.by_weight.isChecked(),
            )

            self.accept()

        except Exception as error:  # noqa
            QMessageBox.warning(self, "Erro [Error]", str(error))
