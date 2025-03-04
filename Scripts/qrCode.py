import os
import qrcode
from Scripts.loadJson import JsonDataHandler

class QrCode:
    @staticmethod
    def create(tcNo):
        """
        Generate a QR code for the given test certificate number (tcNo) and save it in a directory.

        Args:
            tcNo (str): The test certificate number used to create the directory and filename.
        """
        try:
            # Create directory for the test certificate
            os.makedirs(f"testData/{tcNo}", exist_ok=True)

            # Load data from JSON
            data = JsonDataHandler.load_data()

            # Construct the QR code text
            qrText = f"""
            Company Name: Twintech Control System Pvt Ltd
            Resistance of 1st Coil: {data["Resistance1Value"]} and status is {data["Resistance1Status"]}
            Resistance of 2nd Coil: {data["Resistance2Value"]} and status is {data["Resistance2Status"]}
            Inductance of 1st Coil: {data["Inductance1Value"]} and status is {data["Inductance1Status"]}
            Inductance of 2nd Coil: {data["Inductance2Value"]} and status is {data["Inductance2Status"]}
            Voltage of 1st Coil: {data["Voltage1NoLoadValue"]} and status is {data["Voltage1NoLoadStatus"]}
            Voltage of 2nd Coil: {data["Voltage2NoLoadValue"]} and status is {data["Voltage2NoLoadStatus"]}
            Frequency of 1st Coil: {data["Frequency1Value"]} and status is {data["Frequency2Value"]}
            Frequency of 2nd Coil: {data["Frequency1Value"]} and status is {data["Frequency2Value"]}
            """

            # Configure QR code
            qr = qrcode.QRCode(
                version=10,  # Adjust version for data size
                box_size=5,  # Adjust box size for visual appeal
                border=4,    # Border size
            )
            qr.add_data(qrText)
            qr.make(fit=True)

            # Generate and save the QR code image
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(f"testData/{tcNo}/{tcNo}.png")

            print(f"QR code successfully saved at testData/{tcNo}/{tcNo}.png")

        except FileNotFoundError as e:
            print(f"Error: Directory or file not found. {e}")
        except qrcode.exceptions.DataOverflowError as e:
            print(f"Error: Data too large for QR code. {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")