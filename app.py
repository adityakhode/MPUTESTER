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

class app:
    def __init__(self):
        # Force Wayland backend
        #os.environ["QT_QPA_PLATFORM"] = "wayland"

        UnitMaster.create()
        PartyMaster.create()
        #
        printerManager = PrinterManagerUnix()
        connected_printers = printerManager.get_connected_printers()
        print("Connected printers:", connected_printers)
        #
        UnitMaster.addData("refrenceMaterial/unitMaster.xlsx")
        PartyMaster.addData("refrenceMaterial/partyMaster.xlsx")
        ResultMaster.createAll()

        QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
        app = QApplication(sys.argv)

        # Paths to the .ui and .qrc files
        ui_file_path = "frontend/v1.ui"
        qrc_file_path = "frontend/assets.qrc"

        # Create the FRONTEND instance
        frontend = FRONTEND(ui_file_path, qrc_file_path)
        frontend.show()

        sys.exit(app.exec())

app()