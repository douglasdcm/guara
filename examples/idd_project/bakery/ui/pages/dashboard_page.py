from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from bakery.backend.helpers import expiring_batches, low_stock_products
from bakery.backend.repository import DB
from bakery.backend.utils import get_total_sales


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.cash_label = QLabel()
        self.sales_label = QLabel()
        self.low_stock_label = QLabel()
        self.expiration_label = QLabel()

        for label in [
            self.cash_label,
            self.sales_label,
            self.low_stock_label,
            self.expiration_label,
        ]:
            label.setStyleSheet("font-size: 18px; padding: 12px;")
            self.layout.addWidget(label)

        self.refresh()

    def refresh(self):
        if DB.get_open_cash_register():
            self.cash_label.setText("Caixa: Aberto [Opened cash register]")
        else:
            self.cash_label.setText("Caixa: Fechado [Closed cash register]")

        total = get_total_sales()
        self.sales_label.setText(f"Total vendido hoje: R$ {total:.2f} [Sales]")

        self.low_stock_label.setText(
            f"Produtos com estoque baixo: {len(low_stock_products())} [Low stock]"
        )

        self.expiration_label.setText(
            f"Produtos próximos do vencimento: {len(expiring_batches())} [Next expiration]"
        )
