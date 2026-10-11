from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from bakery.ui.pages.cash_page import CashPage
from bakery.ui.pages.dashboard_page import DashboardPage
from bakery.ui.pages.products_page import ProductsPage
from bakery.ui.pages.sales_page import SalesPage
from bakery.ui.pages.stock_page import StockPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Padaria [Bakery system]")
        self.resize(1366, 768)

        root = QWidget()
        self.setCentralWidget(root)

        layout = QHBoxLayout(root)

        menu = QVBoxLayout()
        menu.setSpacing(12)

        title = QLabel("Padaria [Bakery]")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        menu.addWidget(title)

        self.pages = QStackedWidget()

        self.dashboard_page = DashboardPage()
        self.products_page = ProductsPage()
        self.sales_page = SalesPage()
        self.stock_page = StockPage()
        self.cash_page = CashPage()

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.products_page)
        self.pages.addWidget(self.sales_page)
        self.pages.addWidget(self.stock_page)
        self.pages.addWidget(self.cash_page)

        self.buttons = []
        buttons = [
            ("Dashboard", 0),
            ("Produtos [Products]", 1),
            ("Vendas [Salles]", 2),
            ("Estoque [Storage]", 3),
            ("Caixa [Cash register]", 4),
        ]

        for text, index in buttons:
            button = QPushButton(text)
            button.setMinimumHeight(44)
            button.clicked.connect(lambda checked=False, i=index: self.show_page(i))
            menu.addWidget(button)
            self.buttons.append(button)

        menu.addStretch()

        layout.addLayout(menu, 1)
        layout.addWidget(self.pages, 4)

    def show_page(self, index):
        page = self.pages.widget(index)

        if hasattr(page, "refresh"):
            page.refresh()

        self.pages.setCurrentIndex(index)
