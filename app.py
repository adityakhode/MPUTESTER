# Database handling Imports
from Scripts.unitMaster import UnitMaster
from Scripts.partyMaster import PartyMaster
from Scripts.resultMaster import ResultMaster
from Scripts.printerConfig import PrinterManagerUnix

import sys
from PySide6.QtCore import Qt
import frontend.resources
from PySide6.QtWidgets import QApplication
from Scripts.frontend import FRONTEND
from PySide6.QtWidgets import QMessageBox, QPushButton

class app:
    def __init__(self):
        # Force Wayland backend
        #os.environ["QT_QPA_PLATFORM"] = "wayland"
        QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
        app = QApplication(sys.argv)

        UnitMaster.create()
        PartyMaster.create()

        # Paths to the .ui and .qrc files
        ui_file_path = "frontend/v1.ui"
        qrc_file_path = "frontend/assets.qrc"

        # Create the FRONTEND instance
        frontend = FRONTEND(ui_file_path, qrc_file_path)
        frontend.show()

        if not (UnitMaster.dataAvailable() and PartyMaster.dataAvailable()):
            if not UnitMaster.dataAvailable():
                if self.show_upload_instructions("Unit Master"):
                    frontend.on_unit_master_upload_clicked()
                else:
                    frontend.on_close_app_clicked()

            if not PartyMaster.dataAvailable():
                if self.show_upload_instructions("Party Master"):
                    frontend.on_party_master_upload_clicked()
                else:
                    frontend.on_close_app_clicked()
                frontend.on_close_app_clicked()

        #printerManager = PrinterManagerUnix()
        #connected_printers = printerManager.get_connected_printers()
        #print("Connected printers:", connected_printers)

        ResultMaster.createAll()

        sys.exit(app.exec())


    def show_upload_instructions(self, dbName, parent=None):
        """Show file upload instructions with action buttons"""
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("File Upload Required")
        # Main message with formatting
        msg.setText("<b>Please upload the required file</b>")
        msg.setInformativeText(
            "To continue, you need to upload:\n\n"
            f"• An {dbName} Excel file (.xlsx or .xls)\n"
            "• With properly formatted data\n\n"
            "Click 'Upload' to select your file."
        )

        # Custom buttons
        upload_btn = QPushButton("Upload File")
        cancel_btn = QPushButton("Cancel")

        msg.addButton(upload_btn, QMessageBox.AcceptRole)
        msg.addButton(cancel_btn, QMessageBox.RejectRole)

        msg.setDefaultButton(upload_btn)

        # Show dialog and get response
        response = msg.exec()

        if msg.clickedButton() == upload_btn:
            return True  # Proceed with upload
        return False  # User cancelled

app()
