import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, \
    QComboBox, QTableWidget, QTableView, QCheckBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Radio Scraper")
        self.resize(1000, 600)

        self.search = QLineEdit(placeholderText="Station")
        self.language = QComboBox(placeholderText="Language")
        self.irregular = QCheckBox()

        self.table = QTableView()

        filters = QHBoxLayout()
        filters.addWidget(QLabel("Station: "))
        filters.addWidget(self.search, stretch=1)
        filters.addWidget(QLabel("Language: "))
        filters.addWidget(self.language, stretch=1)
        filters.addWidget(QLabel("Show irregular"))
        filters.addWidget(self.irregular)

        root = QVBoxLayout()
        root.addLayout(filters)
        root.addWidget(self.table)

        central = QWidget()
        central.setLayout(root)
        self.setCentralWidget(central)

        self.statusBar().showMessage("Ready")