import pandas as pd
import sqlite3
import json
import os


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
        
        try:
            # Execute the SQL command with parameters
            cursor.execute(insert_query, (supplier_code, party_name, party_address))
        except sqlite3.IntegrityError as e:
            print("Record already present PartyMaster. Unique constraint violation.")
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
