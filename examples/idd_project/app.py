from bakery.ui.main_window import MainWindow
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.showMaximized()

    app.exec()
