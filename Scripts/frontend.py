from PySide6.QtWidgets import QWidget, QPushButton, QStackedWidget, QCheckBox, QComboBox, QDateEdit, QLabel, QLineEdit, QFrame, QFileDialog, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QResource, QTimer, QThread, Signal, Qt, QDate
import os
import subprocess
import serial
import shutil
import serial.tools.list_ports
import time
from Scripts.uuidGenerate import generate_7_digit_uuid
from Scripts.unitMaster import UnitMaster
from Scripts.partyMaster import PartyMaster
from Scripts.resultMaster import ResultMaster
from Scripts.loadJson import JsonDataHandler
from Scripts.createCertificate import Certificate
from Scripts.qrCode import QrCode

class MeasurementThread(QThread):
    resistance_updated = Signal(float)
    connection_error = Signal(str)
    measurement_complete = Signal()

    def __init__(self, parent=None):
        super(MeasurementThread, self).__init__(parent)
        self.esp_serial = None
        self.single_measurement = True  # Changed to always do a single measurement

    def set_serial(self, serial_connection):
        self.esp_serial = serial_connection

    def run(self):
        """Take a single measurement and then stop"""
        if self.esp_serial and self.esp_serial.is_open:
            try:
                # Send command to measure resistance
                self.esp_serial.write(b"start\n")

                # Wait for data to be available
                start_time = time.time()
                response_received = False

                while time.time() - start_time < 5:  # 5 seconds timeout
                    if self.esp_serial.in_waiting > 0:
                        response = self.esp_serial.readline().decode('utf-8').strip()
                        print(f"Received from ESP: {response}")

                        try:
                            resistance_value = float(response)
                            self.resistance_updated.emit(resistance_value)
                            response_received = True
                            break
                        except ValueError as e:
                            print(f"Error parsing resistance value: {e}")

                    self.msleep(100)  # Use QThread's sleep method

                if not response_received:
                    print("No valid response received from ESP")

            except Exception as e:
                print(f"Error in measurement thread: {e}")
                self.connection_error.emit(str(e))

            # Signal that measurement is complete
            self.measurement_complete.emit()


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

        # Initialize the measurement thread
        self.measurement_thread = MeasurementThread(self)
        self.measurement_thread.resistance_updated.connect(self.on_resistance_updated)
        self.measurement_thread.connection_error.connect(self.on_connection_error)
        self.measurement_thread.measurement_complete.connect(self.on_measurement_complete)

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
        self.InductanceCalculatedValue = self.ui.findChild(QLabel, "InductanceCalculatedValue")

        self.voltageValue = self.ui.findChild(QLabel, "voltageValue")
        self.resistanceValue = self.ui.findChild(QLabel, "resistanceValue")
        self.inductanceValue = self.ui.findChild(QLabel, "inductanceValue")

        self.voltageStatus = self.ui.findChild(QLabel, "voltageStatus")
        self.resistanceStatus = self.ui.findChild(QLabel, "resistanceStatus")
        self.inductanceStatus = self.ui.findChild(QLabel, "inductanceStatus")

        self.qrCodeLabel = self.ui.findChild(QLabel, "qrCodeLabel")
        self.pdfButton = self.ui.findChild(QPushButton, "pdfButton")

        self.expandedSettingFrame = self.ui.findChild(QFrame, "expandedSettingFrame")
        self.expandedSettingFrame.hide()

        self.set_tc_number(generate_7_digit_uuid())

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

    def find_esp_device(self):
        """Find the ESP device connected via USB."""
        # Common ESP8266/ESP32 USB-to-Serial adapter identifiers
        esp_identifiers = ['CP210x', 'CH340', 'FTDI', 'Silicon Labs', 'Espressif', 'USB-SERIAL']

        available_ports = list(serial.tools.list_ports.comports())

        for port in available_ports:
            port_info = f"{port.device} - {port.description}"
            print(f"Found port: {port_info}")

            # Check if any of the ESP identifiers is in the port description
            for identifier in esp_identifiers:
                if (identifier.lower() in port.description.lower() or
                        (port.manufacturer and identifier.lower() in port.manufacturer.lower())):
                    print(f"ESP device found on port: {port.device}")
                    return port.device

        # If no specific ESP identifier found, try to find any likely candidates
        if available_ports:
            for port in available_ports:
                # For Linux systems, ttyUSB and ttyACM are common for ESP devices
                if 'ttyUSB' in port.device or 'ttyACM' in port.device:
                    print(f"Possible ESP device found on port: {port.device}")
                    return port.device

        print("No ESP device found")
        return None

    def connect_to_esp(self):
        """Connect to the ESP device."""
        self.esp_port = self.find_esp_device()

        if self.esp_port:
            try:
                # Close existing connection if any
                if self.esp_serial and self.esp_serial.is_open:
                    self.esp_serial.close()
                    self.esp_serial = None
                    time.sleep(0.5)  # Brief pause before reconnecting

                # Note: Your ESP code uses 9600 baud rate
                self.esp_serial = serial.Serial(
                    port=self.esp_port,
                    baudrate=9600,
                    timeout=2
                )
                print(f"Connected to ESP on port {self.esp_port}")

                # Give the ESP a moment to stabilize after connection
                time.sleep(1)

                # Clear any pending data
                self.esp_serial.reset_input_buffer()

                return True
            except Exception as e:
                print(f"Error connecting to ESP: {e}")
                self.esp_serial = None
                return False
        else:
            print("No ESP device found to connect")
            return False

    def on_resistance_updated(self, value):
        """Handle resistance value updates from the measurement thread."""
        self.update_resistance_value(value)

    def on_connection_error(self, error_message):
        """Handle connection errors from the measurement thread."""
        print(f"Connection error in thread: {error_message}")
        if "Input/output error" in error_message:
            # Try to reconnect
            QTimer.singleShot(1000, self.try_reconnect)

        # Re-enable the start button in case of error
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.resistanceCalculatedValue.setText("Error: Check connection")

    def on_measurement_complete(self):
        """Handle the completion of a measurement."""
        print("Measurement completed")
        # Re-enable the start button once measurement is complete
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)

    def try_reconnect(self):
        """Attempt to reconnect to the ESP device."""
        if self.connect_to_esp():
            print("Reconnected to ESP device")
            self.resistanceCalculatedValue.setText("Ready for measurement")
        else:
            self.resistanceCalculatedValue.setText("Connection failed")

    def on_start_button_clicked(self):
        """Handle start button click - Take a single measurement."""
        print("Start button clicked - Taking a single measurement")

        # Connect to ESP if not already connected
        if not self.esp_serial or not self.esp_serial.is_open:
            if not self.connect_to_esp():
                self.resistanceCalculatedValue.setText("ESP not connected")
                return

        # Start the measurement thread for a single measurement
        if not self.measurement_thread.isRunning():
            self.measurement_thread.set_serial(self.esp_serial)
            self.measurement_thread.start()

            self.resistanceCalculatedValue.setText("Measuring...")
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(True)

    def on_testNewSensorButton_clicked(self):
        if not self.saveResultCheckBox.isChecked():
            self.delete_directory(f"testData/{self.get_tc_number()}")

        self.set_tc_number(generate_7_digit_uuid())
        self.stacked_widget.setCurrentIndex(1)

    def on_stop_button_clicked(self):
        """Handle stop button click."""
        print("Stop button clicked")

        if self.measurement_thread.isRunning():
            self.measurement_thread.terminate()  # Forcefully terminate since we're doing single measurements
            self.measurement_thread.wait()  # Wait for the thread to finish

        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(True)
        self.resistanceCalculatedValue.setText("Measurement stopped")

    def on_next_button1_clicked(self):
        self.stacked_widget.setCurrentIndex(2)

    def on_next_button2_clicked(self):
        tablename = self.get_supplier_code() + '-' + self.get_partyName()
        print(tablename)
        ResultMaster.insert(tablename, self.get_tc_number(), self.get_date(), self.get_part_number(),
                            self.get_part_name(), self.get_partyName(), self.get_supplier_code(), self.get_batch_number(),
                            self.get_challan_quantity(), self.get_challan_number(), self.get_date(), self.get_resistance_value(),
                            1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        result1 = ResultMaster.getDetails(tablename, self.get_tc_number())
        result2 = UnitMaster.getDetails(self.get_part_number())
        JsonDataHandler.save_data(result1, result2)

        self.pdfPath = Certificate(self.get_tc_number())
        qrPath = QrCode.create(self.get_tc_number())
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

        result1 = ResultMaster.getDetails(tablename, self.get_tc_number())
        result2 = UnitMaster.getDetails(self.get_part_number())
        JsonDataHandler.save_data(result1, result2)

        Certificate(self.get_tc_number())
        QrCode.create(self.get_tc_number())

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

    # Getter Methods
    def get_tc_number(self):
        return self.tcNumberInput.text()

    def get_part_name(self):
        return self.partNameInput.text()

    def get_part_number(self):
        return self.partNumberDropBox.currentText()

    def get_batch_number(self):
        return self.batchNumberInput.text()

    def get_challan_quantity(self):
        return self.challanQuantityInput.text()

    def get_challan_number(self):
        return self.challanNumberInput.text()

    def get_supplier_code(self):
        return self.supplierCodeDropBox.currentText()

    def get_partyName(self):
        return self.nameDropBox.currentText()

    def get_resistance_value(self):
        return self.resistanceCalculatedValue.text()

    def get_date(self):
        return self.tcDateInput.date().toString("dd MM yyyy")

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

    def set_nameDropBox(self, value):
        """Set the dropdown to the specified part number"""
        index = self.nameDropBox.findText(value)
        if index >= 0:  # Value exists in dropdown
            self.nameDropBox.setCurrentIndex(index)
        else:
            print(f"Warning: Part number '{value}' not found in dropdown")

    def update_resistance_value(self, value):
        if self.resistanceCalculatedValue:
            self.resistanceCalculatedValue.setText(f"{value:.2f} Ω")

            min_resistance = 300  # Example threshold
            max_resistance = 2000.0  # Example threshold

            if self.resistanceStatus:
                if min_resistance <= value <= max_resistance:
                    self.resistanceStatus.setText("PASS")
                    self.resistanceStatus.setStyleSheet("color: green; font-weight: bold;")
                else:
                    self.resistanceStatus.setText("FAIL")
                    self.resistanceStatus.setStyleSheet("color: red; font-weight: bold;")

    def show(self):
        """Show the UI."""
        self.ui.show()

    def populate_dropdown(self, combo_box, items):
        combo_box.clear()

        # Add new items from the list
        for item in items:
            combo_box.addItem(str(item))

    def on_partNumber_dropBox_change(self):
        partNumber = self.partNumberDropBox.currentText()
        part_name = UnitMaster.getPartName(partNumber)
        self.set_part_name(part_name)

    def on_supplierCode_dropBox_change(self):
        supplier_code = self.supplierCodeDropBox.currentText()
        party_name = PartyMaster.getPartyName(supplier_code)
        self.set_nameDropBox(party_name)

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
        subprocess.run(["xdg-open", f"./testData/{self.get_tc_number()}/{self.get_tc_number()}.pdf"], check=True)
