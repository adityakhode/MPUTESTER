from os import path, makedirs
from sqlite3 import DatabaseError, connect, IntegrityError
import pandas as pd


class UnitMaster:
    @staticmethod
    def _get_db_path():
        """Helper method to get the database path."""
        base_dir = path.dirname(path.dirname(path.abspath(__file__)))
        databases_dir = path.join(base_dir, 'Databases')
        makedirs(databases_dir, exist_ok=True)
        return path.join(databases_dir, "unitMaster.db")

    @staticmethod
    def _connect_db():
        """Helper method to connect to the SQLite database."""
        db_path = UnitMaster._get_db_path()
        return connect(db_path)

    @staticmethod
    def create() -> None:
        """Create the UnitMaster table if it doesn't exist."""
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "UnitMaster" (
            "PartNo"            INT PRIMARY KEY,
            "PartName"          VARCHAR,
            "SingleDualOp"      SMALLINT,
            "Threading"         VARCHAR,
            "Lengths"           SMALLINT,
            "ThreadingGoNoGo"   CHAR,
            "NoLockNuts"        SMALLINT,
            "NutThickness"      FLOAT,
            "NutFlatAcross"    FLOAT,
            "PinProtrusion"    FLOAT,
            "CabelType"         VARCHAR,
            "CableLength"      SMALLINT,
            "Connector1"        VARCHAR,
            "Connector2"        VARCHAR,
            "UpperResistance"   FLOAT,
            "LowerResistance"   FLOAT,
            "UpperVoltage0kLoad"  FLOAT,
            "LowerVoltage0kLoad"  FLOAT,
            "UpperVoltage10kLoad" FLOAT,
            "LowerVoltage10kLoad" FLOAT,
            "UpperVoltage3k3Load" FLOAT,
            "LowerVoltage3k3Load" FLOAT,
            "UpperInductance"   FLOAT,
            "LowerInductance"   FLOAT,
            "FREQUENCY"        FLOAT
        );
        '''
        with UnitMaster._connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_query)
            conn.commit()

    @staticmethod
    def insert(*params):
        """Insert a record into the UnitMaster table."""
        if len(params) != 25:
            raise ValueError("Expected 25 parameters for the UnitMaster table")

        insert_query = '''
        INSERT INTO "UnitMaster" (
            "PartNo", "PartName", "SingleDualOp", "Threading", "Lengths", "ThreadingGoNoGo",
            "NoLockNuts", "NutThickness", "NutFlatAcross", "PinProtrusion", "CabelType",
            "CableLength", "Connector1", "Connector2", "UpperResistance", "LowerResistance",
            "UpperVoltage0kLoad", "LowerVoltage0kLoad", "UpperVoltage10kLoad", "LowerVoltage10kLoad",
            "UpperVoltage3k3Load", "LowerVoltage3k3Load", "UpperInductance", "LowerInductance", "FREQUENCY"
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''
        try:
            with UnitMaster._connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute(insert_query, params)
                conn.commit()
        except IntegrityError as e:
            print(f"Record already present in UnitMaster. Error: {e}")
        except DatabaseError as e:
            print(f"Database error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @staticmethod
    def addData(filename):
        """Add data from an Excel file to the UnitMaster table."""
        data = pd.read_excel(filename)
        data.columns = data.columns.str.strip()

        for _, row in data.iterrows():
            params = (
                row.get('PartNo'), row.get('PartName'), row.get('SingleDualOp'), row.get('Threading'),
                row.get('Lengths'), row.get('ThreadingGoNoGo'), row.get('NoLockNuts'), row.get('NutThickness'),
                row.get('NutFlatAcross'), row.get('PinProtrusion'), row.get('CabelType'), row.get('CableLength'),
                row.get('Connector1'), row.get('Connector2'), row.get('UpperResistance'), row.get('LowerResistance'),
                row.get('UpperVoltage0kLoad'), row.get('LowerVoltage0kLoad'), row.get('UpperVoltage10kLoad'),
                row.get('LowerVoltage10kLoad'), row.get('UpperVoltage3k3Load'), row.get('LowerVoltage3k3Load'),
                row.get('UpperInductance'), row.get('LowerInductance'), row.get('FREQUENCY')
            )
            UnitMaster.insert(*params)

    @staticmethod
    def dataAvailable():
        """Check if any data exists in the UnitMaster table."""
        count_query = 'SELECT COUNT(*) FROM UnitMaster;'
        with UnitMaster._connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(count_query)
            result = cursor.fetchone()[0]
            return result > 0

    @staticmethod
    def getPartNo(partNo):
        """Check if a part number exists in the UnitMaster table."""
        query = 'SELECT 1 FROM UnitMaster WHERE PartNo = ? LIMIT 1;'
        with UnitMaster._connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (partNo,))
            return cursor.fetchone() is not None

    @staticmethod
    def getPartName(partNo):
        """Get the part name for a given part number."""
        query = 'SELECT PartName FROM UnitMaster WHERE PartNo = ?;'
        with UnitMaster._connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (partNo,))
            result = cursor.fetchone()
            return result[0] if result else None

    @staticmethod
    def getPartNoList():
        """Get a list of all part numbers in the UnitMaster table."""
        query = 'SELECT PartNo FROM UnitMaster;'
        with UnitMaster._connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [row[0] for row in cursor.fetchall()]

    @staticmethod
    def getDetails(partNo):
        """Get details for a given part number."""
        query = '''
        SELECT Threading, Lengths, ThreadingGoNoGo, NoLockNuts, NutThickness, NutFlatAcross, PinProtrusion,
               CabelType, CableLength, Connector1, Connector2, UpperResistance, LowerResistance,
               UpperVoltage0kLoad, LowerVoltage0kLoad, UpperVoltage10kLoad, LowerVoltage10kLoad,
               UpperVoltage3k3Load, LowerVoltage3k3Load, UpperInductance, LowerInductance, FREQUENCY
        FROM UnitMaster WHERE PartNo = ?;
        '''
        with UnitMaster._connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (partNo,))
            result = cursor.fetchone()
            return result if result else "No records found"

    @staticmethod
    def fetch_unit_parameters(part_no):
        # SQL query to fetch the required parameters
        query = """
        SELECT 
            UpperResistance, LowerResistance,
            UpperVoltage0kLoad, LowerVoltage0kLoad,
            UpperVoltage10kLoad, LowerVoltage10kLoad,
            UpperVoltage3k3Load, LowerVoltage3k3Load,
            UpperInductance, LowerInductance, FREQUENCY
        FROM UnitMaster
        WHERE PartNo = ?
        """

        with UnitMaster._connect_db() as conn:
            cursor = conn.cursor()
            # Execute the query
            cursor.execute(query, (part_no,))
            result = cursor.fetchone()


        # Check if result is not None
        if result:
            # Create a dictionary from the result
            keys = [
                "UpperResistance", "LowerResistance",
                "UpperVoltage0kLoad", "LowerVoltage0kLoad",
                "UpperVoltage10kLoad", "LowerVoltage10kLoad",
                "UpperVoltage3k3Load", "LowerVoltage3k3Load",
                "UpperInductance", "LowerInductance", "FREQUENCY"
                    ]
            return dict(zip(keys, result))
        else:
            return None
