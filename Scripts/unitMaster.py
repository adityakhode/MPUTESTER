import os
import sqlite3
import pandas as pd

class UnitMaster:

    def create():
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        databases_dir = os.path.join(base_dir, 'Databases')
        os.makedirs(databases_dir, exist_ok=True)
        db_path = os.path.join(databases_dir, "unitMaster.db")

        # Connect to the SQLite database (creates the file if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # SQL command to create the UnitMaster table
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "UnitMaster" (
            "PartNo"     INT PRIMARY KEY,
            "PartName"           VARCHAR,
            "SingleDualOp"      SMALLINT,
            "Threading"          VARCHAR,
            "Lengths"           SMALLINT,
            "ThreadingGoNoGo"       CHAR,
            "NoLockNuts"        SMALLINT,
            "NutThickness"         FLOAT,
            "NutFlatAcross"        FLOAT,
            "PinProtrusion"        FLOAT,
            "CabelType"          VARCHAR,
            "CableLength"       SMALLINT,
            "Connector1"         VARCHAR,
            "Connector2"         VARCHAR,
            "UpperResistance"      FLOAT,
            "LowerResistance"      FLOAT,
            "UpperVoltage0kLoad"   FLOAT,
            "LowerVoltage0kLoad"   FLOAT,
            "UpperVoltage10kLoad"  FLOAT,
            "LowerVoltage10kLoad"  FLOAT,
            "UpperVoltage3k3Load"  FLOAT,
            "LowerVoltage3k3Load"  FLOAT,
            "UpperInductance"      FLOAT,
            "LowerInductance"      FLOAT,
            "FREQUENCY"            FLOAT
        );
        '''

        # Execute the SQL command
        cursor.execute(create_table_query)

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

    def insert(*params):

        UnitMaster.create()

        # Ensure the correct number of parameters
        if len(params) != 25:
            raise ValueError("Expected 21 parameters for the UnitMaster table")

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        databases_dir = os.path.join(base_dir, 'Databases')
        os.makedirs(databases_dir, exist_ok=True)
        db_path = os.path.join(databases_dir, "unitMaster.db")

        # Connect to the SQLite database (creates the file if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # SQL command to insert data into the UnitMaster table
        insert_query = '''
        INSERT INTO "UnitMaster" (
            "PartNo", "PartName", "SingleDualOp", "Threading", "Lengths", "ThreadingGoNoGo",
            "NoLockNuts", "NutThickness", "NutFlatAcross", "PinProtrusion", "CabelType",
            "CableLength", "Connector1", "Connector2", "UpperResistance", "LowerResistance",
            "UpperVoltage0kLoad", "LowerVoltage0kLoad", "UpperVoltage10kLoad", "LowerVoltage10kLoad", UpperVoltage3k3Load, "LowerVoltage3k3Load", "UpperInductance", "LowerInductance", "FREQUENCY"
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''

        dropQuery = '''
        DROP TABLE UnitMaster
        '''
        try:
            # Execute the SQL command with parameters
            cursor.execute(insert_query, params)
        except sqlite3.IntegrityError as e:
            print("Record already present in unitMaster. Unique constraint violation.")
            print(f"Error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Database error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            # Commit the transaction and close the connection
            conn.commit()
            conn.close()

    def addData(filename):

        # Reads the data from excel and remove the leading and Trailing whiteSpaces
        data = pd.read_excel(filename)
        data.columns = data.columns.str.strip()

        for index, row in data.iterrows():
            PartNo = row.get('PartNo')
            PartName = row.get('PartName')
            SingleDualOp = row.get('SingleDualOp')
            Threading = row.get('Threading')
            Lengths = row.get('Lengths')
            ThreadingGoNoGo = row.get('ThreadingGoNoGo')
            NoLockNuts = row.get('NoLockNuts')
            NutThickness = row.get('NutThickness')
            NutFlatAcross = row.get('NutFlatAcross')
            PinProtrusion = row.get('PinProtrusion')
            CabelType = row.get('CabelType')
            CableLength = row.get('CableLength')
            Connector1 = row.get('Connector1')
            Connector2 = row.get('Connector2')
            UpperResistance = row.get('UpperResistance')
            LowerResistance = row.get('LowerResistance')
            UpperVoltage0kLoad = row.get('UpperVoltage0kLoad')
            LowerVoltage0kLoad = row.get('LowerVoltage0kLoad')
            UpperVoltage10kLoad = row.get('UpperVoltage10kLoad')
            LowerVoltage10kLoad = row.get('LowerVoltage10kLoad')
            UpperVoltage3k3Load = row.get('UpperVoltage3k3Load')
            LowerVoltage3k3Load = row.get('LowerVoltage3k3Load')
            UpperInductance = row.get('UpperInductance')
            LowerInductance = row.get('LowerInductance')
            Frequency = row.get('FREQUENCY')

            UnitMaster.insert(PartNo, PartName, SingleDualOp, Threading, Lengths, ThreadingGoNoGo, NoLockNuts,
                              NutThickness, NutFlatAcross, PinProtrusion, CabelType, CableLength, Connector1,
                              Connector2, UpperResistance, LowerResistance, UpperVoltage0kLoad, LowerVoltage0kLoad,
                              UpperVoltage10kLoad, LowerVoltage10kLoad, UpperVoltage3k3Load, LowerVoltage3k3Load,
                              UpperInductance, LowerInductance, Frequency)

    def dataAvailable(self):
        UnitMaster.create()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        databases_dir = os.path.join(base_dir, 'Databases')
        os.makedirs(databases_dir, exist_ok=True)
        db_path = os.path.join(databases_dir, "unitMaster.db")

        # Connect to the SQLite database (creates the file if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        countQuery = '''
        SELECT COUNT(*) FROM unitMaster;
        '''

        cursor.execute(countQuery)
        result = cursor.fetchone()[0]

        conn.commit()
        conn.close()
        if result > 0:
            return True
        else:
            return False

    def getPartNo(part_no):
        UnitMaster.create()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        databases_dir = os.path.join(base_dir, 'Databases')
        os.makedirs(databases_dir, exist_ok=True)
        db_path = os.path.join(databases_dir, "unitMaster.db")

        # Connect to the SQLite database (creates the file if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Prepare the SQL query to check if the PartNo exists
        query = '''
        SELECT 1 FROM UnitMaster WHERE PartNo = ? LIMIT 1;
        '''

        # Execute the query with the provided part_no
        cursor.execute(query, (part_no,))
        result = cursor.fetchone()

        # Close the database connection
        conn.close()
        # Return True if a row is found, otherwise False
        return result is not None

    def getPartName(part_no):
        UnitMaster.create()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        databases_dir = os.path.join(base_dir, 'Databases')
        os.makedirs(databases_dir, exist_ok=True)
        db_path = os.path.join(databases_dir, "unitMaster.db")

        # Connect to the SQLite database (creates the file if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Prepare the SQL query to check if the PartNo exists
        query = '''
        SELECT PartName FROM UnitMaster WHERE PartNo = ?;
        '''

        # Execute the query with the provided part_no
        cursor.execute(query, (part_no,))
        result = cursor.fetchone()[0]

        # Close the database connection
        conn.close()
        # Return True if a row is found, otherwise False
        return result

    def getPartNoList(self):
        UnitMaster.create()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        databases_dir = os.path.join(base_dir, 'Databases')
        os.makedirs(databases_dir, exist_ok=True)
        db_path = os.path.join(databases_dir, "unitMaster.db")

        # Connect to the SQLite database (creates the file if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Prepare the SQL query to check if the PartNo exists
        query = '''
        SELECT PartNo FROM UnitMaster;
        '''

        # Execute the query with the provided part_no
        cursor.execute(query)
        result = cursor.fetchall()

        # Close the database connection
        conn.close()
        # Return True if a row is found, otherwise False
        return result

    def getDetails(TcNo):
        # Define the SQL command to select data based on TcNo
        select_query = '''
        SELECT Threading, Lengths, ThreadingGoNoGo, NoLockNuts, NutThickness, NutFlatAcross, PinProtrusion, CabelType, CableLength, Connector1, Connector2, UpperResistance, LowerResistance, UpperVoltage0kLoad, LowerVoltage0kLoad, UpperVoltage10kLoad, LowerVoltage10kLoad, UpperVoltage3k3Load, LowerVoltage3k3Load, UpperInductance, LowerInductance, FREQUENCY FROM UnitMaster WHERE PartNo = ?;
        '''

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        databases_dir = os.path.join(base_dir, 'Databases')
        os.makedirs(databases_dir, exist_ok=True)
        db_path = os.path.join(databases_dir, "unitMaster.db")

        # Connect to the SQLite database (creates the file if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            # Execute the SQL command with the parameter
            cursor.execute(select_query, (TcNo,))

            # Fetch all matching rows
            results = cursor.fetchall()

            # If no rows are found, return an empty list or appropriate message
            if not results:
                return "No records found"

            return results[0]
        except sqlite3.Error as e:
            # Handle any SQLite errors
            return f"An error occurred: {e}"
        finally:
            # Close the database connection
            conn.close()
