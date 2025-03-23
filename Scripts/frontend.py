from PySide6.QtWidgets import QWidget, QPushButton, QStackedWidget, QCheckBox, QComboBox, QDateEdit
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
        # Find the Buttons
        self.unitMasterUploadButton = self.ui.findChild(QPushButton, "unitMasterUploadButton")
        self.partyMasterUploadButton = self.ui.findChild(QPushButton, "partyMasterUploadButton")
        self.generateReportButton = self.ui.findChild(QPushButton, "generateReportButton")
        self.configPrinterButton = self.ui.findChild(QPushButton, "configPrinterButton")
        self.closeAppButton = self.ui.findChild(QPushButton, "closeAppButton")
        self.poweroffButton = self.ui.findChild(QPushButton, "poweroffButton")

        self.nextButton1 = self.ui.findChild(QPushButton, "nextButton1")

        self.startButton = self.ui.findChild(QPushButton, "startButton")
        self.stopButton = self.ui.findChild(QPushButton, "stopButton")
        self.backButton = self.ui.findChild(QPushButton, "backButton")
        self.nextButton2 = self.ui.findChild(QPushButton, "nextButton2")

        self.pdfButton = self.ui.findChild(QPushButton, "pdfButton")
        self.testNewSensorButton = self.ui.findChild(QPushButton, "testNewSensorButton")

        self.saveResublCheckBox = self.ui.findChild(QCheckBox, "saveResublCheckBox")

        self.stacked_widget = self.ui.findChild(QStackedWidget, "stackedWidget")

        self.nameDropBox = self.ui.findChild(QComboBox, "nameDropBox")
        self.partNumberDropBox = self.ui.findChild(QComboBox, "partNumberDropBox")
        self.supplierCodeDropBox = self.ui.findChild(QComboBox, "supplierCodeDropBox")

        self.tcDateInput = self.ui.findChild(QDateEdit, "tcDateInput")

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