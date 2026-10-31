from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, \
    QComboBox, QTableView, QCheckBox

from radioscraper.eibi.model import Broadcast
from radioscraper.eibi.parser import language_json_to_dict
from radioscraper.ui.table_model import BroadcastTableModel


def filling_language_combo_box(combo_box: QComboBox) -> None:
    language_data = language_json_to_dict()
    for language in language_data.values():
        combo_box.addItem(language)

class MainWindow(QMainWindow):
    def __init__(self, broadcast: Broadcast) -> None:
        super().__init__()
        self.setWindowTitle("Radio Scraper")
        self.resize(1000, 600)

        self.search = QLineEdit(placeholderText="Station")
        self.search.textChanged.connect(self.show_station_in_status_bar)
        self.search.textChanged.connect(self.set_default_language)

        self.language = QComboBox(placeholderText="Language")
        filling_language_combo_box(self.language)
        self.language.currentIndexChanged.connect(self.show_language_in_status_bar)

        self.irregular = QCheckBox("Show irregular")
        self.irregular.toggled.connect(self.show_toggled_in_status_bar)

        self.model = BroadcastTableModel(broadcast, self)
        self.table = QTableView()
        self.table.setModel(self.model)

        self.filters = QHBoxLayout()
        self.add_widgets_to_filters_box()

        self.root = QVBoxLayout()
        self.root.addLayout(self.filters)
        self.root.addWidget(self.table, stretch=1)

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