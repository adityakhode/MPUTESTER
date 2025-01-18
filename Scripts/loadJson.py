import json
import os

class JsonDataHandler:
    # Path for the temporary file where the data will be saved
    TEMP_FILE_PATH = "/tmp/MPUTestData.json"

    @staticmethod
    def save_data(result1, result2):#save_data(tablename, TcNo, part_no):
        """
        Save the data to a JSON file in the /tmp directory.
        """
        try:
            # Fetch data from the ResultMaster and UnitMaster (assuming they are defined elsewhere)
            #result1 = ResultMaster.getDetails(tablename, TcNo)
            #result2 = UnitMaster.getDetails(part_no)

            # Create a dictionary with the row data
            data = {
                "TcNo"                   : result1[0],
                "TcDate"                 : result1[1],
                "PartNo"                 : result1[2],
                "PartName"               : result1[3],
                "PartyName"              : result1[4],
                "SupplierCode"           : result1[5],
                "BatchNo"                : result1[6],
                "ChallanQuantity"        : result1[7],
                "ChallanNumber"          : result1[8],
                "ChallanDate"            : result1[9],
                "Resistance1Value"       : result1[10],
                "Resistance1Status"      : result1[11],
                "Resistance2Value"       : result1[12],
                "Resistance2Status"      : result1[13],
                "Inductance1Value"       : result1[14],
                "Inductance1Status"      : result1[15],
                "Inductance2Value"       : result1[16],
                "Inductance2Status"      : result1[17],
                "Frequency1Value"        : result1[18],
                "Frequency2Value"        : result1[19],
                "Voltage1NoLoadValue"    : result1[20],
                "Voltage1NoLoadStatus"   : result1[21],
                "Voltage2NoLoadValue"    : result1[22],
                "Voltage2NoLoadStatus"   : result1[23],
                "Voltage1_10kLoadValue"  : result1[24],
                "Voltage1_10kLoadStatus" : result1[25],
                "Voltage2_10kLoadValue"  : result1[26],
                "Voltage2_10kLoadStatus" : result1[27],
                "Voltage1_3k3LoadValue"  : result1[28],
                "Voltage1_3k3LoadStatus" : result1[29],
                "Voltage2_3k3LoadValue"  : result1[30],
                "Voltage2_3k3LoadStatus" : result1[31],

                "Threading"              : result2[0],
                "Lengths"                : result2[1],
                "ThreadingGoNoGo"        : result2[2],
                "NoLockNuts"             : result2[3],
                "NutThickness"           : result2[4],
                "NutFlatAcross"          : result2[5],
                "PinProtrusion"          : result2[6],
                "CabelType"              : result2[7],
                "CableLength"            : result2[8],
                "Connector1"             : result2[9],
                "Connector2"             : result2[10],
                "UpperResistance"        : result2[11],
                "LowerResistance"        : result2[12],
                "UpperVoltage0kLoad"     : result2[13],
                "LowerVoltage0kLoad"     : result2[14],
                "UpperVoltage10kLoad"    : result2[15],
                "LowerVoltage10kLoad"    : result2[16],
                "UpperVoltage3k3Load"    : result2[17],
                "LowerVoltage3k3Load"    : result2[18],
                "UpperInductance"        : result2[19],
                "LowerInductance"        : result2[20],
                "FREQUENCY1"             : result2[21]
            }
            # Save the data dictionary to a JSON file in the /tmp directory
            with open(JsonDataHandler.TEMP_FILE_PATH, "w") as json_file:
                json.dump(data, json_file, indent=4)

            print(f"Data saved successfully to {JsonDataHandler.TEMP_FILE_PATH}")

        except Exception as e:
            print(f"Error saving data: {e}")

    @staticmethod
    def load_data():
        """
        Load data from the saved JSON file and return it as a dictionary.
        """
        try:
            if os.path.exists(JsonDataHandler.TEMP_FILE_PATH):
                with open(JsonDataHandler.TEMP_FILE_PATH, "r") as json_file:
                    data = json.load(json_file)
                    return data
            else:
                print(f"Error: File {JsonDataHandler.TEMP_FILE_PATH} not found.")
                return None

        except Exception as e:
            print(f"Error loading data: {e}")
            return None

    @staticmethod
    def delete_json_file():
        """
        Delete the JSON file from the /tmp directory.
        """
        try:
            if os.path.exists(JsonDataHandler.TEMP_FILE_PATH):
                os.remove(JsonDataHandler.TEMP_FILE_PATH)
                print(f"File {JsonDataHandler.TEMP_FILE_PATH} deleted successfully.")
            else:
                print(f"Error: File {JsonDataHandler.TEMP_FILE_PATH} does not exist.")
        except Exception as e:
            print(f"Error deleting file: {e}")