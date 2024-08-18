import pandas as pd
import sqlite3
import os

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
            "UpperVoltage"         FLOAT,
            "LowerVoltage"         FLOAT,
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
        if len(params) != 21:
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
            "UpperVoltage", "LowerVoltage", "UpperInductance", "LowerInductance", "FREQUENCY"
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''

        dropQuery = '''
        DROP TABLE UnitMaster
        '''
        # Execute the SQL command with parameters
        cursor.execute(insert_query, params)

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

    def addData(filename):

        #Reads the data from excel and remove the leading and Traling whiteSpaces
        data = pd.read_excel(filename)
        data.columns = data.columns.str.strip()

        for index, row in data.iterrows():
            PartNo          = row.get('PartNo'         )
            PartName        = row.get('PartName'       )
            SingleDualOp    = row.get('SingleDualOp'   )
            Threading       = row.get('Threading'      )
            Lengths         = row.get('Lengths'        )
            ThreadingGoNoGo = row.get('ThreadingGoNoGo')
            NoLockNuts      = row.get('NoLockNuts'     )
            NutThickness    = row.get('NutThickness'   )
            NutFlatAcross   = row.get('NutFlatAcross'  )
            PinProtrusion   = row.get('PinProtrusion'  )
            CabelType       = row.get('CabelType'      )
            CableLength     = row.get('CableLength'    )
            Connector1      = row.get('Connector1'     )
            Connector2      = row.get('Connector2'     )
            UpperResistance = row.get('UpperResistance')
            LowerResistance = row.get('LowerResistance')
            UpperVoltage    = row.get('UpperVoltage'   )
            LowerVoltage    = row.get('LowerVoltage'   )
            UpperInductance = row.get('UpperInductance')
            LowerInductance = row.get('LowerInductance')
            Frequency       = row.get('FREQUENCY'      )

            UnitMaster.insert(PartNo, PartName, SingleDualOp, Threading, Lengths, ThreadingGoNoGo,NoLockNuts, NutThickness, NutFlatAcross, PinProtrusion, CabelType,CableLength, Connector1, Connector2, UpperResistance, LowerResistance,UpperVoltage, LowerVoltage, UpperInductance, LowerInductance, Frequency)

    def dataAvailable():
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
        if result > 0 :
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

    def getPartNoList():
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

class PartyMaster:

    def create():
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        databases_dir = os.path.join(base_dir, 'Databases')
        os.makedirs(databases_dir, exist_ok=True)
        db_path = os.path.join(databases_dir, 'partyMaster.db')

        # Connect to the SQLite database (creates the file if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # SQL command to create the Party Master table
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "PartyMaster" (
            "SupplierCode"   CHAR PRIMARY KEY,
            "PartyName"               VARCHAR,
            "PartyAddress"            VARCHAR
        );
        '''
        
        # Execute the SQL command
        cursor.execute(create_table_query)
        
        # Commit the transaction and close the connection
        conn.commit()
        conn.close()
    
    def insert(supplier_code, party_name, party_address):

        PartyMaster.create()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        databases_dir = os.path.join(base_dir, 'Databases')
        os.makedirs(databases_dir, exist_ok=True)
        db_path = os.path.join(databases_dir, 'partyMaster.db')

        # Connect to the SQLite database (creates the file if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # SQL command to insert data into the Party Master table
        insert_query = '''
        INSERT INTO "PartyMaster" ( "SupplierCode", "PartyName", "PartyAddress" )
        VALUES (?, ?, ?);
        '''
        
        # Execute the SQL command with parameters

        cursor.execute(insert_query, (supplier_code, party_name, party_address))
        conn.commit()
        conn.close()

    def addData(filename):
        #Reads the data from excel and remove the leading and Traling whiteSpaces
        data = pd.read_excel(filename)
        data.columns = data.columns.str.strip()

        for index, row in data.iterrows():
            supplierCode = row['SupplierCode']
            partyName    = row['partyName'   ]
            partyAddress = row['partyAddress']
            PartyMaster.insert(supplierCode, partyName, partyAddress)

    def dataAvailable():
        PartyMaster.create()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        databases_dir = os.path.join(base_dir, 'Databases')
        os.makedirs(databases_dir, exist_ok=True)
        db_path = os.path.join(databases_dir, 'partyMaster.db')

        # Connect to the SQLite database (creates the file if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        countQuery = '''
        SELECT COUNT(*) FROM partyMaster;
        '''

        cursor.execute(countQuery)
        result = cursor.fetchone()[0]

        conn.commit()
        conn.close()
        if result > 0 :
            return True
        else:
            return False

    def getSupplierCodeAndNameList():
        PartyMaster.create()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        databases_dir = os.path.join(base_dir, 'Databases')
        os.makedirs(databases_dir, exist_ok=True)
        db_path = os.path.join(databases_dir, 'partyMaster.db')

        # Connect to the SQLite database (creates the file if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Prepare the SQL query to check if the PartNo exists
        query = '''
        SELECT supplierCode, Partyname FROM PartyMaster;
        '''
        
        # Execute the query with the provided part_no
        cursor.execute(query)
        result = cursor.fetchall()
        
        # Close the database connection
        conn.close()
        # Return True if a row is found, otherwise False
        return result

class resultMaster:
    def create(tablename):
        # Define the SQL command to create the table with the given name
        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS "{tablename}" (
            "TcNo"      VARCHAR PRIMARY KEY,
            "TcDate"                VARCHAR,
            "PartNo"                INTEGER,
            "PartName"              CHAR,
            "PartyName"             VARCHAR,
            "SupplierCode"          CHAR,
            "BatchNo"               CHAR,
            "ChallanQuantity"       SMALLINT,
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
            "Voltage1NoLoadStatus"  FLOAT,
            "Voltage2NoLoadValue"   FLOAT,
            "Voltage2NoLoadStatus"  FLOAT,
            "Voltage1-10kLoadValue" FLOAT,
            "Voltage1-10kLoadStatus"FLOAT,
            "Voltage2-10kLoadValue" FLOAT,
            "Voltage2-10kLoadStatus"FLOAT,
            "Voltage1-3k3LoadValue" FLOAT,
            "Voltage1-3k3LoadStatus"FLOAT,
            "Voltage2-3k3LoadValue" FLOAT,
            "Voltage2-3k3Loadstatus"FLOAT
        );
        '''
        filename = tablename + ".db"
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        databases_dir = os.path.join(base_dir, 'Databases')
        os.makedirs(databases_dir, exist_ok=True)
        db_path = os.path.join(databases_dir,filename)

        # Connect to the SQLite database (creates the file if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Execute the SQL command to create the table
        cursor.execute(create_table_query)

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

    def insert(tablename, *params):
        # Ensure the correct number of parameters
        if len(params) != 31:
            print(len(params))
            raise ValueError("Expected 31 parameters for the Result Master table")
    
        # Define the SQL command to insert data into the table with the given name
        insert_query = f'''
        INSERT INTO "{tablename}" (
            "TcNo", "TcDate", "PartNo", "PartName", "PartyName", "SupplierCode", "BatchNo",
            "ChallanQuantity", "ChallanDate", "Resistance1Value", "Resistance1Status",
            "Resistance2Value", "Resistance2Status", "Inductance1Value", "Inductance1Status",
            "Inductance2Value", "Inductance2Status", "Frequency1Value", "Frequency2Value",
            "Voltage1NoLoadValue", "Voltage1NoLoadStatus", "Voltage2NoLoadValue", "Voltage2NoLoadStatus",
            "Voltage1-10kLoadValue", "Voltage1-10kLoadStatus", "Voltage2-10kLoadValue", "Voltage2-10kLoadStatus",
            "Voltage1-3k3LoadValue", "Voltage1-3k3LoadStatus", "Voltage2-3k3LoadValue", "Voltage2-3k3Loadstatus"
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''
        filename = tablename + ".db"
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        databases_dir = os.path.join(base_dir, 'Databases')
        os.makedirs(databases_dir, exist_ok=True)
        db_path = os.path.join(databases_dir,filename)

        # Connect to the SQLite database (creates the file if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
    
        # Execute the SQL command with parameters
        cursor.execute(insert_query, params)
        
        # Commit the transaction and close the connection
        conn.commit()
        conn.close()
    
    def getDetails(tablename, TcNo):

        # Define the SQL command to select data based on TcNo
        select_query = f'SELECT * FROM "{tablename}" WHERE "TcNo" = ?;'
        
        filename = tablename + ".db"
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        databases_dir = os.path.join(base_dir, 'Databases')
        os.makedirs(databases_dir, exist_ok=True)
        db_path = os.path.join(databases_dir,filename)

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
            
            return results
        except sqlite3.Error as e:
            # Handle any SQLite errors
            return f"An error occurred: {e}"
        finally:
            # Close the database connection
            conn.close()

    def createAll():

        if (PartyMaster.dataAvailable()):
            result = PartyMaster.getSupplierCodeAndNameList()
            for row in result:
                tableName = row[0] + "-" + row[1]
                resultMaster.create(tableName)

    def printDetails(row):
        TcNo = row[0]
        TcDate = row[1]
        PartNo = row[2]
        PartName = row[3]
        PartyName = row[4]
        SupplierCode = row[5]
        BatchNo = row[6]
        ChallanQuantity = row[7]
        ChallanDate = row[8]
        Resistance1Value = row[9]
        Resistance1Status = row[10]
        Resistance2Value = row[11]
        Resistance2Status = row[12]
        Inductance1Value = row[13]
        Inductance1Status = row[14]
        Inductance2Value = row[15]
        Inductance2Status = row[16]
        Frequency1Value = row[17]
        Frequency2Value = row[18]
        Voltage1NoLoadValue = row[19]
        Voltage1NoLoadStatus = row[20]
        Voltage2NoLoadValue = row[21]
        Voltage2NoLoadStatus = row[22]
        Voltage1_10kLoadValue = row[23]
        Voltage1_10kLoadStatus = row[24]
        Voltage2_10kLoadValue = row[25]
        Voltage2_10kLoadStatus = row[26]
        Voltage1_3k3LoadValue = row[27]
        Voltage1_3k3LoadStatus = row[28]
        Voltage2_3k3LoadValue = row[29]
        Voltage2_3k3LoadStatus = row[30]
    
        # Print the values
        print(f"TcNo: {TcNo}")
        print(f"TcDate: {TcDate}")
        print(f"PartNo: {PartNo}")
        print(f"PartName: {PartName}")
        print(f"PartyName: {PartyName}")
        print(f"SupplierCode: {SupplierCode}")
        print(f"BatchNo: {BatchNo}")
        print(f"ChallanQuantity: {ChallanQuantity}")
        print(f"ChallanDate: {ChallanDate}")
        print(f"Resistance1Value: {Resistance1Value}")
        print(f"Resistance1Status: {Resistance1Status}")
        print(f"Resistance2Value: {Resistance2Value}")
        print(f"Resistance2Status: {Resistance2Status}")
        print(f"Inductance1Value: {Inductance1Value}")
        print(f"Inductance1Status: {Inductance1Status}")
        print(f"Inductance2Value: {Inductance2Value}")
        print(f"Inductance2Status: {Inductance2Status}")
        print(f"Frequency1Value: {Frequency1Value}")
        print(f"Frequency2Value: {Frequency2Value}")
        print(f"Voltage1NoLoadValue: {Voltage1NoLoadValue}")
        print(f"Voltage1NoLoadStatus: {Voltage1NoLoadStatus}")
        print(f"Voltage2NoLoadValue: {Voltage2NoLoadValue}")
        print(f"Voltage2NoLoadStatus: {Voltage2NoLoadStatus}")
        print(f"Voltage1_10kLoadValue: {Voltage1_10kLoadValue}")
        print(f"Voltage1_10kLoadStatus: {Voltage1_10kLoadStatus}")
        print(f"Voltage2_10kLoadValue: {Voltage2_10kLoadValue}")
        print(f"Voltage2_10kLoadStatus: {Voltage2_10kLoadStatus}")
        print(f"Voltage1_3k3LoadValue: {Voltage1_3k3LoadValue}")
        print(f"Voltage1_3k3LoadStatus: {Voltage1_3k3LoadStatus}")
        print(f"Voltage2_3k3LoadValue: {Voltage2_3k3LoadValue}")
        print(f"Voltage2_3k3LoadStatus: {Voltage2_3k3LoadStatus}")
    