from PySide6.QtWidgets import (QWidget, QPushButton, QStackedWidget,
                               QCheckBox, QComboBox, QDateEdit, QLabel,
                               QLineEdit, QFrame, QFileDialog, QMessageBox)
from PySide6.QtCore import QFile, QResource, Qt, QDate
from Scripts.uuidGenerate import generate_7_digit_uuid
from Scripts.createCertificate import Certificate
from Scripts.resultMaster import ResultMaster
from Scripts.loadJson import JsonDataHandler
from Scripts.partyMaster import PartyMaster
from Scripts.unitMaster import UnitMaster
from Scripts.hardware import ESPHardware
from PySide6.QtUiTools import QUiLoader
from Scripts.qrCode import QrCode
import subprocess
import shutil
import time
import os

class FRONTEND(QWidget):
    def __init__(self, ui_file_path, qrc_file_path, parent=None):
        super(FRONTEND, self).__init__(parent)

        # Load the .qrc file at runtime
        if not QResource.registerResource(qrc_file_path):
            print(f"Failed to load resource file: {qrc_file_path}")

        # Load the .ui file
        self.ui = self._load_ui(ui_file_path)

        # ESP serial connection variables
        self.esp_serial = None
        self.esp_port = None

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
        self.tcDateInput.setDate(QDate.currentDate())

        self.tcNumberInput = self.ui.findChild(QLineEdit, "tcNumberInput")
        self.partNameInput = self.ui.findChild(QLineEdit, "partNameInput")
        self.batchNumberInput = self.ui.findChild(QLineEdit, "batchNumberInput")
        self.challanQuantityInput = self.ui.findChild(QLineEdit, "challanQuantityInput")
        self.challanNumberInput = self.ui.findChild(QLineEdit, "challanNumberInput")

        self.voltageCalculatedValue = self.ui.findChild(QLabel, "voltageCalculatedValue")
        self.resistanceCalculatedValue = self.ui.findChild(QLabel, "resistanceCalculatedValue")
        self.frequencyCalculatedValue = self.ui.findChild(QLabel, "frequencyCalculatedValue")

        self.voltageValue = self.ui.findChild(QLabel, "voltageValue")
        self.resistanceValue = self.ui.findChild(QLabel, "resistanceValue")
        self.frequencyValue = self.ui.findChild(QLabel, "frequencyValue")

        self.voltageStatus = self.ui.findChild(QLabel, "voltageStatus")
        self.resistanceStatus = self.ui.findChild(QLabel, "resistanceStatus")
        self.inductanceStatus = self.ui.findChild(QLabel, "inductanceStatus")

        self.qrCodeLabel = self.ui.findChild(QLabel, "qrCodeLabel")
        self.pdfButton = self.ui.findChild(QPushButton, "pdfButton")

        self.expandedSettingFrame = self.ui.findChild(QFrame, "expandedSettingFrame")
        self.expandedSettingFrame.hide()

        self.setter(self.tcNumberInput, generate_7_digit_uuid())

        self.populate_dropdown(self.partNumberDropBox, UnitMaster.getPartNoList())
        self.populate_dropdown(self.supplierCodeDropBox, PartyMaster.getSupplierCodeList())
        self.populate_dropdown(self.nameDropBox, PartyMaster.getPartyList())


        # Set up initial state
        self.stacked_widget.setCurrentIndex(1)
        if self.resistanceCalculatedValue:
            self.resistanceCalculatedValue.setText("Ready for measurement")
        if self.stopButton:
            self.stopButton.setEnabled(False)

    def _connect_signals(self):
        """Connect button signals to slots."""
        if self.nextButton1:
            self.nextButton1.clicked.connect(self.on_next_button1_clicked)
        if self.nextButton2:
            self.nextButton2.clicked.connect(self.on_next_button2_clicked)
        if self.backButton:
            self.backButton.clicked.connect(self.on_back_button_clicked)
        if self.startButton:
            self.startButton.clicked.connect(self.on_start_button_clicked)
        if self.stopButton:
            self.stopButton.clicked.connect(self.on_stop_button_clicked)
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
        if self.testNewSensorButton:
            self.testNewSensorButton.clicked.connect(self.on_testNewSensorButton_clicked)
        if self.pdfButton:
            self.pdfButton.clicked.connect(self.pdf_open)
        self.partNumberDropBox.currentIndexChanged.connect(self.on_partNumber_dropBox_change)
        self.supplierCodeDropBox.currentIndexChanged.connect(self.on_supplierCode_dropBox_change)
        self.nameDropBox.currentIndexChanged.connect(self.on_partyName_dropBox_change)

    def on_testNewSensorButton_clicked(self):
        if not self.saveResultCheckBox.isChecked():
            self.delete_directory(f"testData/{self.getter(self.tcNumberInput)}")

        self.setter(self.tcNumberInput, generate_7_digit_uuid())

        self.stacked_widget.setCurrentIndex(1)

    def on_stop_button_clicked(self):
        """Handle stop button click."""
        print("Stop button clicked")

        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(True)
        self.resistanceCalculatedValue.setText("Measurement stopped")

    def on_next_button1_clicked(self):
        self.paramater_dictionary = UnitMaster.fetch_unit_parameters(int(self.getDropBox(self.partNumberDropBox)))

        self.setter(self.resistanceValue,
                    f'Resistance: {self.paramater_dictionary["LowerResistance"]} - {self.paramater_dictionary["UpperResistance"]}Ω')
        self.setter(self.voltageValue,
                    f'Voltage: {self.paramater_dictionary["LowerVoltage0kLoad"]} - {self.paramater_dictionary["UpperVoltage0kLoad"]}V')
        self.setter(self.frequencyValue,
                    f'Frequency: {self.paramater_dictionary["FREQUENCY"]} - {self.paramater_dictionary["FREQUENCY"]}Hz')
        self.stacked_widget.setCurrentIndex(2)

    def status(self):
        resistance = self.getter(self.resistanceCalculatedValue)

    def on_next_button2_clicked(self):
        print(self.getter(self.resistanceCalculatedValue))
        tablename = self.getDropBox(self.supplierCodeDropBox) + '-' + self.get_partyName()
        data = {
            "TcNo": self.getter(self.tcNumberInput),
            "TcDate": self.get_date(),
            "PartNo": self.getDropBox(self.partNumberDropBox),
            "PartName": self.getter(self.partNameInput),
            "PartyName": self.get_partyName(),
            "SupplierCode": self.getDropBox(self.supplierCodeDropBox),
            "BatchNo": self.getter(self.batchNumberInput),
            "ChallanQuantity": self.getter(self.challanQuantityInput),
            "ChallanNumber": self.getter(self.challanNumberInput),
            "ChallanDate": self.get_date(),
            # Electrical parameters - using real values where available
            "Resistance1Value": self.getter(self.resistanceCalculatedValue),
            "Resistance1Status": "N.A",
            # Dummy values for unused measurements
            "Resistance2Value": "N.A",
            "Resistance2Status": "N.A",
            "Inductance1Value": "N.A",
            "Inductance1Status": "N.A",
            "Inductance2Value": "N.A",
            "Inductance2Status": "N.A",
            "Frequency1Value": self.getter(self.frequencyCalculatedValue),
            "Frequency2Value": "N.A",
            "Voltage1NoLoadValue": self.getter(self.voltageCalculatedValue),
            "Voltage1NoLoadStatus": 0,
            "Voltage2NoLoadValue": "N.A",
            "Voltage2NoLoadStatus": "N.A",
            "Voltage1-10kLoadValue": "N.A",
            "Voltage1-10kLoadStatus": "N.A",
            "Voltage2-10kLoadValue": "N.A",
            "Voltage2-10kLoadStatus": "N.A",
            "Voltage1-3k3LoadValue": "N.A",
            "Voltage1-3k3LoadStatus": "N.A",
            "Voltage2-3k3LoadValue": "N.A",
            "Voltage2-3k3LoadStatus": "N.A"
        }
        values = []
        for field in data:
            if field in data:
                values.append(data[field])
        ResultMaster.insert(tablename, *values)

        result1 = ResultMaster.getDetails(tablename, self.getter(self.tcNumberInput))
        result2 = UnitMaster.getDetails(self.getDropBox(self.partNumberDropBox))
        JsonDataHandler.save_data(result1, result2)

        self.pdfPath = Certificate(self.getter(self.tcNumberInput))
        qrPath = QrCode.create(self.getter(self.tcNumberInput))
        self.set_qr_code_image(qrPath)

        self.stacked_widget.setCurrentIndex(3)

    def on_back_button_clicked(self):
        self.stacked_widget.setCurrentIndex(1)

    def on_unit_master_upload_clicked(self):
        """Handle unit master upload button click with proper error handling"""
        try:
            # Get file path from user
            path = self.selectFile()
            if not path:  # User cancelled file selection
                return

            # Confirm upload with user
            confirm = QMessageBox.question(
                self,
                "Confirm Upload",
                f"Are you sure you want to upload data from:\n{path}?",
                QMessageBox.Yes | QMessageBox.No
            )

            if confirm != QMessageBox.Yes:
                return  # User cancelled

            # Attempt to add data
            os.remove("Databases/unitMaster.db")
            UnitMaster.create()
            UnitMaster.addData(path)

            # Show success message
            QMessageBox.information(
                self,
                "Success",
                "Unit master data uploaded successfully!"
            )

        except PermissionError:
            QMessageBox.critical(
                self,
                "Error",
                "Permission denied. Please check file access rights."
            )
        except Exception as e:
            # Log the actual error for debugging
            print(f"Upload error: {str(e)}")

            QMessageBox.critical(
                self,
                "Upload Failed",
                f"Failed to upload unit master data:\n{str(e)}"
            )

    def on_party_master_upload_clicked(self):
        """Handle unit master upload button click with proper error handling"""
        try:
            # Get file path from user
            path = self.selectFile()
            if not path:  # User cancelled file selection
                return

            # Confirm upload with user
            confirm = QMessageBox.question(
                self,
                "Confirm Upload",
                f"Are you sure you want to upload data from:\n{path}?",
                QMessageBox.Yes | QMessageBox.No
            )

            if confirm != QMessageBox.Yes:
                return  # User cancelled

            # Attempt to add data
            os.remove("Databases/partyMaster.db")
            PartyMaster.create()
            PartyMaster.addData(path)

            # Show success message
            QMessageBox.information(
                self,
                "Success",
                "Party master data uploaded successfully!"
            )

        except PermissionError:
            QMessageBox.critical(
                self,
                "Error",
                "Permission denied. Please check file access rights."
            )
        except Exception as e:
            # Log the actual error for debugging
            print(f"Upload error: {str(e)}")

            QMessageBox.critical(
                self,
                "Upload Failed",
                f"Failed to upload unit master data:\n{str(e)}"
            )

    def on_config_printer_clicked(self):
        pass

    def on_generate_report_clicked(self):
        tableList = ResultMaster.getTableList()
        tablename = "1234-Twintech"
        tcNoList = ResultMaster.getTcNoList(tablename)

        result1 = ResultMaster.getDetails(tablename, self.getter(self.tcNumberInput))
        result2 = UnitMaster.getDetails(self.getDropBox(self.partNumberDropBox))
        JsonDataHandler.save_data(result1, result2)

        Certificate(self.getter(self.tcNumberInput))
        QrCode.create(self.getter(self.tcNumberInput))

    # Getter Methods
    def getter(self, name):
        return name.text()

    def getDropBox(self, name):
        return name.currentText()

    def get_partyName(self):
        return self.nameDropBox.currentText()

    def get_date(self):
        return self.tcDateInput.date().toString("dd MM yyyy")

    # Setter Methods
    def setter(self, name, value):
        name.setText(value)

    def set_DropBox(self, name, value):
        """Set the dropdown to the specified part number"""
        index = name.findText(value)
        if index >= 0:  # Value exists in dropdown
            name.setCurrentIndex(index)
        else:
            print(f"Warning: Part number '{value}' not found in dropdown")

    def show(self):
        """Show the UI."""
        self.ui.show()

    def on_start_button_clicked(self):
        esp = ESPHardware()
        #Wait a moment for connection
        time.sleep(2)

        # Get resistance
        print("\nGetting resistance measurement...")
        resistance = esp.get_resistance()
        self.setter(self.resistanceCalculatedValue, str(resistance))
        print(f"Resistance: {resistance} ohms")

        if self.show_confirmation_dialog("Press Continue to calculate more param"):
            # Get voltage
            print("\nGetting voltage measurement...")
            voltage = esp.get_voltage()
            self.setter(self.voltageCalculatedValue, str(voltage))
            print(f"Voltage: {voltage} V")

             # Get frequency
            print("\nGetting frequency measurement...")
            frequency = esp.get_frequency()
            self.setter(self.frequencyCalculatedValue, str(frequency))
            print(f"Frequency: {frequency} Hz")

    def populate_dropdown(self, combo_box, items):
        combo_box.clear()

        # Add new items from the list
        for item in items:
            combo_box.addItem(str(item))

    def on_partNumber_dropBox_change(self):
        partNumber = self.partNumberDropBox.currentText()
        part_name = UnitMaster.getPartName(partNumber)
        self.setter(self.partNameInput, part_name)

    def on_partyName_dropBox_change(self):
        partyName = self.nameDropBox.currentText()
        supplier_code = PartyMaster.getsupplierCode(partyName)
        self.set_DropBox(self.supplierCodeDropBox, supplier_code)

    def on_supplierCode_dropBox_change(self):
        supplier_code = self.supplierCodeDropBox.currentText()
        party_name = PartyMaster.getPartyName(supplier_code)
        self.set_DropBox(self.nameDropBox, party_name)

    def selectFile(parent=None):
        """
        Open a file dialog to select an Excel file.

        Args:
            parent (QWidget, optional): Parent widget for the file dialog

        Returns:
            str: Path of the selected Excel file, or None if canceled

        Note:
            Requires QApplication to exist before calling
        """
        file_path, _ = QFileDialog.getOpenFileName(
            parent,
            "Select Excel File",
            "",
            "Excel Files (*.xlsx *.xls);;All Files (*)"
        )
        return file_path if file_path else None

    def delete_directory(self, directory_path):
        """
        Deletes a directory and all its contents

        Args:
            directory_path (str): Path to the directory to be deleted
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            if os.path.exists(directory_path):
                shutil.rmtree(directory_path)
                print(f"Successfully deleted directory: {directory_path}")
                return True
            else:
                print(f"Directory does not exist: {directory_path}")
                return False
        except Exception as e:
            print(f"Error deleting directory {directory_path}: {e}")
            return False

    def show_confirmation_dialog(self, message, title="Confirmation"):
        """
        Show a confirmation dialog with Yes/No buttons.

        Args:
            message (str): The message to display
            title (str): The window title (default: "Confirmation")

        Returns:
            bool: True if Yes clicked, False if No clicked
        """
        # Create the message box
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)

        # Set the window flags to ensure it stays on top
        msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint)

        # Execute the message box and return the result
        result = msg_box.exec()
        return result == QMessageBox.Yes

    def set_qr_code_image(self, new_image_path: str) -> bool:
        """
        Updates the image of qrCodeLabel by modifying its stylesheet.
        The image will respect the min-width/min-height set in the stylesheet.

        Args:
            new_image_path (str): Path to the new image file (PNG, JPG, SVG, etc.)

        Returns:
            bool: True if successful, False if failed
        """
        try:
            # Verify the image exists first
            if not os.path.exists(new_image_path):
                print(f"Error: Image not found at {new_image_path}")
                return False

            # Update the stylesheet with the new image URL
            self.qrCodeLabel.setStyleSheet(f"""
                QLabel {{
                    image: url({new_image_path});
                    min-width: 20%;
                    min-height: 20%;
                }}
            """)

            return True
        except Exception as e:
            print(f"Error updating QR code image: {e}")
            return False

    def pdf_open(self):
        subprocess.run(["xdg-open", f"./testData/{self.getter(self.tcNumberInput)}/{self.getter(self.tcNumberInput)}.pdf"], check=True)

    def on_poweroff_clicked(self):
        if self.show_confirmation_dialog("Are you sure you want to power off the system?"):
            os.system("poweroff")

    def on_close_app_clicked(self):
        if self.show_confirmation_dialog("Are you sure you want to close the application?"):
            self.cleanup_resources()
            self.close()

    def cleanup_resources(self):
        """Clean up resources before exiting."""
        # Stop the measurement thread
        if hasattr(self, 'measurement_thread') and self.measurement_thread.isRunning():
            print("Stopping measurement thread...")
            self.measurement_thread.terminate()
            self.measurement_thread.wait()

        # Close the serial connection
        if self.esp_serial and self.esp_serial.is_open:
            print("Closing serial connection...")
            try:
                self.esp_serial.close()
            except Exception as e:
                print(f"Error closing serial connection: {e}")
