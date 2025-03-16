from Scripts.qrCode import QrCode

# Database handling Imports
from Scripts.unitMaster import UnitMaster
from Scripts.partyMaster import PartyMaster
from Scripts.resultMaster import ResultMaster

from Scripts.loadJson import JsonDataHandler

from Scripts.createCertificate import Certificate
from Scripts.printerConfig import PrinterManagerUnix

import os
import sys
from Scripts import ui_untitled

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

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
        ResultMaster.insert("1234-Twintech", "TC002", "2024-08-18", 1001, "PartA", "PartyX", "S123", "Batch01", 50, "500", "2024-08-15", 0.5, 1.0, 0.6, 1.1, 0.7, 1.2, 0.8, 1.3, 0.9, 1.4, 1.0, 1.5, 1.1, 1.6, 1.2, 1.7, 1.3, 1.8, 1.4, 1.9,12,12)
        x = UnitMaster.getPartNoList()
        result1 = ResultMaster.getDetails("1234-Twintech", "TC002")
        result2 = UnitMaster.getDetails(12345)
        JsonDataHandler.save_data(result1, result2)
        Certificate("TC002")
        QrCode.create("TC002")

        # Set the attribute before creating the QApplication instance
        QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

        app = QApplication(sys.argv)
        window = ui_untitled.Ui_MainWindow()
        window.show()
        sys.exit(app.exec())





app()