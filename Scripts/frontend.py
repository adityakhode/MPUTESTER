from PySide6.QtWidgets import QWidget, QPushButton, QStackedWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QResource

class FRONTEND(QWidget):
    def __init__(self, ui_file_path, qrc_file_path, parent=None):
        super(FRONTEND, self).__init__(parent)

        # Load the .qrc file at runtime
        if not QResource.registerResource(qrc_file_path):
            print(f"Failed to load resource file: {qrc_file_path}")

        # Load the .ui file
        self.ui = self._load_ui(ui_file_path)

        # Set up widgets and connect signals
        self._setup_widgets()
        self._connect_signals()

    def _load_ui(self, ui_file_path):
        loader = QUiLoader()
        ui_file = QFile(ui_file_path)
        if not ui_file.open(QFile.ReadOnly):
            print(f"Cannot open {ui_file_path}: {ui_file.errorString()}")
            return None
        ui = loader.load(ui_file, self)
        ui_file.close()
        return ui

    def _setup_widgets(self):
        """Connect widgets to class attributes for easy access."""
        # Example: Assuming you have a QLineEdit named 'lineEdit' in your .ui file


        # Find the 'nextButton1' button
        self.nextButton1 = self.ui.findChild(QPushButton, "nextButton1")
        self.nextButton2 = self.ui.findChild(QPushButton, "nextButton2")
        self.stacked_widget = self.ui.findChild(QStackedWidget, "stackedWidget")
        self.stacked_widget.setCurrentIndex(1)

    def _connect_signals(self):
        """Connect button signals to slots."""
        if self.nextButton1:
            self.nextButton1.clicked.connect(self.on_next_button_clicked1)
        if self.nextButton2:
            self.nextButton2.clicked.connect(self.on_next_button_clicked2)

    def on_next_button_clicked1(self):
        """Slot for handling the nextButton1 click event."""
        print("Next button clicked!")
        self.stacked_widget.setCurrentIndex(2)

    def on_next_button_clicked2(self):
        """Slot for handling the nextButton1 click event."""
        print("Next button clicked!")
        self.stacked_widget.setCurrentIndex(3)

    def show(self):
        """Show the UI."""
        self.ui.show()