import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, \
    QComboBox, QTableWidget, QTableView, QCheckBox


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Radio Scraper")
        self.resize(1000, 600)

        self.search = QLineEdit(placeholderText="Station")
        self.search.textChanged.connect(self.show_station_in_status_bar)
        self.search.textChanged.connect(self.set_default_language)

        self.language = QComboBox(placeholderText="Language")
        self.language.addItem("English")
        self.language.addItem("French")
        self.language.currentIndexChanged.connect(self.show_language_in_status_bar)

        self.irregular = QCheckBox("Show irregular")
        self.irregular.toggled.connect(self.show_toggled_in_status_bar)

        self.table = QTableView()

        self.filters = QHBoxLayout()
        self.add_widgets_to_filters_box()

        self.root = QVBoxLayout()
        self.root.addLayout(self.filters)
        self.root.addWidget(self.table)

        central = QWidget()
        central.setLayout(self.root)
        self.setCentralWidget(central)

        self.statusBar().showMessage("Ready")


    def add_widgets_to_filters_box(self) -> None:
        self.filters.addWidget(QLabel("Station: "))
        self.filters.addWidget(self.search, stretch=1)
        self.filters.addWidget(QLabel("Language: "))
        self.filters.addWidget(self.language, stretch=1)
        self.filters.addWidget(self.irregular)


    def show_station_in_status_bar(self, text: str) -> None:
        self.statusBar().showMessage(text)

    def show_language_in_status_bar(self, index: int) -> None:
        language = self.language.currentText()
        self.statusBar().showMessage(str(language))

    def show_toggled_in_status_bar(self, toggled: bool) -> None:
        self.statusBar().showMessage(str(toggled))

    def set_default_language(self) -> None:
        self.language.setCurrentText("English")