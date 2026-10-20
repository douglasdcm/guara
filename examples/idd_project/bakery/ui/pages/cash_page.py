from PySide6.QtWidgets import (
    QInputDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from bakery.backend.repository import DB
from bakery.backend.scenarios import (
    scenario_close_cash,
    scenario_open_cash,
    scenario_sangria_withdraw_cash,
)


class CashPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.status = QLabel()
        self.status.setStyleSheet("font-size: 18px;")

        self.open_button = QPushButton("Abrir Caixa [Open cash register]")
        self.open_button.clicked.connect(self.open_cash_register)

        self.withdraw_button = QPushButton("Sangria [Cash withdrawal]")
        self.withdraw_button.clicked.connect(self.withdrawal)

        self.close_button = QPushButton("Fechar Caixa [Close cash register]")
        self.close_button.clicked.connect(self.close_cash_register)

        self.layout.addWidget(self.status)
        self.layout.addWidget(self.open_button)
        self.layout.addWidget(self.withdraw_button)
        self.layout.addWidget(self.close_button)

        self.refresh()

    def refresh(self):
        if DB.get_open_cash_register():
            self.status.setText("Caixa aberto [Opened cash register]")
        else:
            self.status.setText("Caixa fechado [Closed cash register]")

    def open_cash_register(self):
        value, ok = QInputDialog.getDouble(
            self,
            "Abrir Caixa [Open cash register]",
            "Valor inicial: [Initial value]",
            200,
            0,
            999999,
            2,
        )

        if ok:
            try:
                scenario_open_cash(value)
                self.refresh()
                QMessageBox.information(
                    self, "Sucesso [Success]", "Caixa aberto [Cash register is open]"
                )
            except Exception as error:  # noqa
                QMessageBox.warning(self, "Erro [Error]", str(error))

    def withdrawal(self):
        value, ok = QInputDialog.getDouble(
            self,
            "Sangria [Withdrawal]",
            "Valor: [Value]",
            0,
            0,
            999999,
            2,
        )

        if ok:
            scenario_sangria_withdraw_cash(value)
            QMessageBox.information(
                self, "Sucesso [Success]", "Sangria registrada [Withdrawal registered]"
            )

    def close_cash_register(self):
        try:
            result = scenario_close_cash(role="Gerente")
            QMessageBox.information(
                self,
                "Fechamento [Closure]",
                f"Total vendido: R$ {result['total_sales']:.2f} [Salles]",
            )
            self.refresh()

        except Exception as error:  # noqa
            QMessageBox.warning(self, "Erro [Error]", str(error))
