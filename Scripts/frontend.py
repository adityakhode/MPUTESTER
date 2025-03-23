from PySide6.QtWidgets import QWidget, QPushButton, QStackedWidget, QCheckBox, QComboBox, QDateEdit, QLabel, QLineEdit, QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QResource
import os

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

        self.saveResultCheckBox = self.ui.findChild(QCheckBox, "saveResultCheckBox")

        self.stacked_widget = self.ui.findChild(QStackedWidget, "stackedWidget")

        self.nameDropBox = self.ui.findChild(QComboBox, "nameDropBox")
        self.partNumberDropBox = self.ui.findChild(QComboBox, "partNumberDropBox")
        self.supplierCodeDropBox = self.ui.findChild(QComboBox, "supplierCodeDropBox")

        self.tcDateInput = self.ui.findChild(QDateEdit, "tcDateInput")

        self.tcNumberInput = self.ui.findChild(QLineEdit, "tcNumberInput")
        self.partNameInput = self.ui.findChild(QLineEdit, "partNameInput")
        self.batchNumberInput = self.ui.findChild(QLineEdit, "batchNumberInput")
        self.challanQuantityInput = self.ui.findChild(QLineEdit, "challanQuantityInput")
        self.challanNumberInput = self.ui.findChild(QLineEdit, "challanNumberInput")


        self.voltageCalculatedValue = self.ui.findChild(QLabel, "voltageCalculatedValue")
        self.resistanceCalculatedValue = self.ui.findChild(QLabel, "resistanceCalculatedValue")
        self.InductanceCalculatedValue = self.ui.findChild(QLabel, "InductanceCalculatedValue")

        self.voltageValue = self.ui.findChild(QLabel, "voltageValue")
        self.resistanceValue = self.ui.findChild(QLabel, "resistanceValue")
        self.inductanceValue = self.ui.findChild(QLabel, "inductanceValue")

        self.voltageStatus = self.ui.findChild(QLabel, "voltageStatus")
        self.resistanceStatus = self.ui.findChild(QLabel, "resistanceStatus")
        self.inductanceStatus = self.ui.findChild(QLabel, "inductanceStatus")

        self.stacked_widget.setCurrentIndex(1)



    def _connect_signals(self):
        """Connect button signals to slots."""
        if self.nextButton1:
            self.nextButton1.clicked.connect(self.on_next_button1_clicked)
        if self.nextButton2:
            self.nextButton2.clicked.connect(self.on_next_button2_clicked)
        if self.backButton:
            self.backButton.clicked.connect(self.on_back_button_clicked)
        if self.startButton:
            pass
        if self.stopButton:
            pass
        if self.unitMasterUploadButton:
            self.unitMasterUploadButton.clicked.connect(self.on_unit_master_upload_clicked)
        if self.partyMasterUploadButton:
            self.partyMasterUploadButton.clicked.connect(self.on_party_master_upload_clicked)
        if self.generateReportButton:
            self.generateReportButton.clicked.connect(self.on_generate_report_clicked)
        if self.configPrinterButton:
           self.configPrinterButton.clicked.connect(self.on_config_printer_clicked)
        if self.closeAppButton:
            self.closeAppButton.clicked.connect(self.on_close_app_clicked)
        if self.poweroffButton:
            self.poweroffButton.clicked.connect(self.on_poweroff_clicked)


    def on_next_button1_clicked(self):
        """Slot for handling the nextButton1 click event."""
        print("Next button clicked!")
        self.stacked_widget.setCurrentIndex(2)

    def on_next_button2_clicked(self):
        """Slot for handling the nextButton1 click event."""
        print("Next button clicked!")
        self.stacked_widget.setCurrentIndex(3)

    def on_back_button_clicked(self):
        """Slot for handling the nextButton1 click event."""
        print("Back button clicked!")
        self.stacked_widget.setCurrentIndex(1)

    def on_unit_master_upload_clicked(self):
        pass
    def on_party_master_upload_clicked(self):
        pass
    def on_config_printer_clicked(self):
        pass
    def on_generate_report_clicked(self):
        pass
    def on_poweroff_clicked(self):
        os.system("poweroff")
    def on_close_app_clicked(self):
        self.close()

        # Getter Methods
    def get_tc_number(self):
        return self.tcNumberInput.text()

    def get_part_name(self):
        return self.partNameInput.text()

    def get_batch_number(self):
        return self.batchNumberInput.text()

    def get_challan_quantity(self):
        return self.challanQuantityInput.text()

    def get_challan_number(self):
        return self.challanNumberInput.text()

        # Setter Methods
    def set_tc_number(self, value):
        self.tcNumberInput.setText(value)

    def set_part_name(self, value):
        self.partNameInput.setText(value)

    def set_batch_number(self, value):
        self.batchNumberInput.setText(value)

    def set_challan_quantity(self, value):
        self.challanQuantityInput.setText(value)

    def set_challan_number(self, value):
        self.challanNumberInput.setText(value)

    def show(self):
        """Show the UI."""
        self.ui.show()