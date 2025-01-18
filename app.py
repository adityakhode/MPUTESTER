from Scripts.loadJson import JsonDataHandler
#from Scripts.createCertificate import Certificate
#from Scripts.qrCode import QrCode
from Scripts.printerConfig import PrinterManagerUnix
from Scripts.databases import UnitMaster, ResultMaster, PartyMaster

class app:
    def __init__(self):
        printerManager = PrinterManagerUnix()
        connected_printers = printerManager.get_connected_printers()
        print("Connected printers:", connected_printers)

        #UnitMaster.addData("refrenceMaterial/unitMaster.xlsx")
        #PartyMaster.addData("refrenceMaterial/partyMaster.xlsx")
        #ResultMaster.createAll()
        #ResultMaster.insert("1234-Twintech", "TC002", "2024-08-18", 1001, "PartA", "PartyX", "S123", "Batch01", 50, "500", "2024-08-15", 0.5, 1.0, 0.6, 1.1, 0.7, 1.2, 0.8, 1.3, 0.9, 1.4, 1.0, 1.5, 1.1, 1.6, 1.2, 1.7, 1.3, 1.8, 1.4, 1.9,12,12)

        result1 = ResultMaster.getDetails("1234-Twintech", "TC002")
        result2 = UnitMaster.getDetails(12345)
        JsonDataHandler.save_data(result1, result2)
        #Certificate(12345)
        #QrCode.create(12345)

app()