import sqlite3
import os
from Scripts.partyMaster import PartyMaster


class ResultMaster:
    @staticmethod
    def _get_db_path():
        """Helper method to get the database path."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        databases_dir = os.path.join(base_dir, 'Databases')
        os.makedirs(databases_dir, exist_ok=True)
        return os.path.join(databases_dir, "resultMaster.db")

    @staticmethod
    def _connect_db():
        """Helper method to connect to the SQLite database."""
        db_path = ResultMaster._get_db_path()
        return sqlite3.connect(db_path)

    @staticmethod
    def create(tableName):
        """Create a table with the given name if it doesn't exist."""
        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS "{tableName}" (
            "TcNo"                  VARCHAR PRIMARY KEY,
            "TcDate"                VARCHAR,
            "PartNo"                INTEGER,
            "PartName"              CHAR,
            "PartyName"             VARCHAR,
            "SupplierCode"          CHAR,
            "BatchNo"               CHAR,
            "ChallanQuantity"       SMALLINT,
            "ChallanNumber"         INTEGER,
            "ChallanDate"           DATE,
            "Resistance1Value"      FLOAT,
            "Resistance1Status"     FLOAT,
            "Resistance2Value"      FLOAT,
            "Resistance2Status"     FLOAT,
            "Inductance1Value"      FLOAT,
            "Inductance1Status"     FLOAT,
            "Inductance2Value"      FLOAT,
            "Inductance2Status"     FLOAT,
            "Frequency1Value"       FLOAT,
            "Frequency2Value"       FLOAT,
            "Voltage1NoLoadValue"   FLOAT,
            "Voltage1NoLoadStatus" FLOAT,
            "Voltage2NoLoadValue"   FLOAT,
            "Voltage2NoLoadStatus" FLOAT,
            "Voltage1-10kLoadValue" FLOAT,
            "Voltage1-10kLoadStatus" FLOAT,
            "Voltage2-10kLoadValue" FLOAT,
            "Voltage2-10kLoadStatus" FLOAT,
            "Voltage1-3k3LoadValue" FLOAT,
            "Voltage1-3k3LoadStatus" FLOAT,
            "Voltage2-3k3LoadValue" FLOAT,
            "Voltage2-3k3LoadStatus" FLOAT
        );
        '''
        with ResultMaster._connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_query)
            conn.commit()

    @staticmethod
    def insert(tableName, *params):
        """Insert a record into the specified table."""
        if len(params) != 32:
            raise ValueError("Expected 32 parameters for the Result Master table")

        insert_query = f'''
        INSERT INTO "{tableName}" (
            "TcNo", "TcDate", "PartNo", "PartName", "PartyName", "SupplierCode", "BatchNo",
            "ChallanQuantity", "ChallanNumber", "ChallanDate", "Resistance1Value", "Resistance1Status",
            "Resistance2Value", "Resistance2Status", "Inductance1Value", "Inductance1Status",
            "Inductance2Value", "Inductance2Status", "Frequency1Value", "Frequency2Value",
            "Voltage1NoLoadValue", "Voltage1NoLoadStatus", "Voltage2NoLoadValue", "Voltage2NoLoadStatus",
            "Voltage1-10kLoadValue", "Voltage1-10kLoadStatus", "Voltage2-10kLoadValue", "Voltage2-10kLoadStatus",
            "Voltage1-3k3LoadValue", "Voltage1-3k3LoadStatus", "Voltage2-3k3LoadValue", "Voltage2-3k3LoadStatus"
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''
        try:
            with ResultMaster._connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute(insert_query, params)
                conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Record already present in {tableName}. Error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Database error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @staticmethod
    def getDetails(tableName, tcNo):
        """Get details for a given TcNo from the specified table."""
        query = f'SELECT * FROM "{tableName}" WHERE "TcNo" = ?;'
        with ResultMaster._connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (tcNo,))
            result = cursor.fetchone()
            return result if result else "No records found"

    @staticmethod
    def createAll():
        """Create tables for all suppliers if PartyMaster data is available."""
        if PartyMaster.dataAvailable():
            suppliers = PartyMaster.getSupplierCodeAndNameList()
            for supplierCode, partyName in suppliers:
                tableName = f"{supplierCode}-{partyName}"
                ResultMaster.create(tableName)

    @staticmethod
    def printDetails(row):
        """Print details of a row in a readable format."""
        if not row:
            print("No data to print.")
            return

        details = {
            "TcNo"                   : row[0],
            "TcDate"                 : row[1],
            "PartNo"                 : row[2],
            "PartName"               : row[3],
            "PartyName"              : row[4],
            "SupplierCode"           : row[5],
            "BatchNo"                : row[6],
            "ChallanQuantity"        : row[7],
            "ChallanDate"            : row[8],
            "Resistance1Value"       : row[9],
            "Resistance1Status"      : row[10],
            "Resistance2Value"       : row[11],
            "Resistance2Status"      : row[12],
            "Inductance1Value"       : row[13],
            "Inductance1Status"      : row[14],
            "Inductance2Value"       : row[15],
            "Inductance2Status"      : row[16],
            "Frequency1Value"        : row[17],
            "Frequency2Value"        : row[18],
            "Voltage1NoLoadValue"    : row[19],
            "Voltage1NoLoadStatus"   : row[20],
            "Voltage2NoLoadValue"    : row[21],
            "Voltage2NoLoadStatus"   : row[22],
            "Voltage1_10kLoadValue"  : row[23],
            "Voltage1_10kLoadStatus" : row[24],
            "Voltage2_10kLoadValue"  : row[25],
            "Voltage2_10kLoadStatus" : row[26],
            "Voltage1_3k3LoadValue"  : row[27],
            "Voltage1_3k3LoadStatus" : row[28],
            "Voltage2_3k3LoadValue"  : row[29],
            "Voltage2_3k3LoadStatus" : row[30],
        }

        for key, value in details.items():
            print(f"{key}: {value}")

    @staticmethod
    def getTableList():
        query = r"SELECT NAME FROM SQLITE_MASTER WHERE TYPE = 'TABLE';"

        with ResultMaster._connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [row[0] for row in cursor.fetchall()]

    @staticmethod
    def getTcNoList(tableName):
        query = f"SELECT * FROM {tableName} WHERE TcNo IS NOT NULL;"

        with ResultMaster._connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [row[0] for row in cursor.fetchall()]