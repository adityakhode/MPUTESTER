import os
import sqlite3
import pandas as pd
from netaddr.ip.iana import query


class PartyMaster:
    @staticmethod
    def _get_db_path():
        """Helper method to get the database path."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        databases_dir = os.path.join(base_dir, 'Databases')
        os.makedirs(databases_dir, exist_ok=True)
        return os.path.join(databases_dir, 'partyMaster.db')

    @staticmethod
    def _connect_db():
        """Helper method to connect to the SQLite database."""
        db_path = PartyMaster._get_db_path()
        return sqlite3.connect(db_path)

    @staticmethod
    def create():
        """Create the PartyMaster table if it doesn't exist."""
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "PartyMaster" (
            "SupplierCode"   CHAR PRIMARY KEY,
            "PartyName"     VARCHAR,
            "PartyAddress"  VARCHAR
        );
        '''
        with PartyMaster._connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_query)
            conn.commit()

    @staticmethod
    def insert(supplierCode, partyName, partyAddress):
        """Insert a record into the PartyMaster table."""
        insert_query = '''
        INSERT INTO "PartyMaster" ("SupplierCode", "PartyName", "PartyAddress")
        VALUES (?, ?, ?);
        '''
        try:
            with PartyMaster._connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute(insert_query, (supplierCode, partyName, partyAddress))
                conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Record already present in PartyMaster. Error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Database error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @staticmethod
    def addData(filename):
        """Add data from an Excel file to the PartyMaster table."""
        data = pd.read_excel(filename)
        data.columns = data.columns.str.strip()

        for _, row in data.iterrows():
            supplierCode = row['SupplierCode']
            partyName = row['partyName']
            partyAddress = row['partyAddress']
            PartyMaster.insert(supplierCode, partyName, partyAddress)

    @staticmethod
    def dataAvailable():
        """Check if any data exists in the PartyMaster table."""
        count_query = 'SELECT COUNT(*) FROM PartyMaster;'
        with PartyMaster._connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(count_query)
            result = cursor.fetchone()[0]
            return result > 0

    @staticmethod
    def getSupplierCodeAndNameList():
        """Get a list of supplier codes and names from the PartyMaster table."""
        query = 'SELECT SupplierCode, PartyName FROM PartyMaster;'
        with PartyMaster._connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    @staticmethod
    def getSupplierCodeList():
        """Get a list of supplier codes and names from the PartyMaster table."""
        query = 'SELECT SupplierCode FROM PartyMaster;'
        with PartyMaster._connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [row[0] for row in cursor.fetchall()]

    @staticmethod
    def getPartyList():
        """Get a list of supplier codes and names from the PartyMaster table."""
        query = 'SELECT PartyName FROM PartyMaster;'
        with PartyMaster._connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [row[0] for row in cursor.fetchall()]

    @staticmethod
    def getPartyName(supplierCode):
        query = 'SELECT PartyName FROM PartyMaster WHERE SupplierCode=? LIMIT 1;'
        with PartyMaster._connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (supplierCode,))
            result = cursor.fetchone()
            return result[0] if result else None