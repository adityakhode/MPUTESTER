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
            Result
            R1: {data["Resistance1Value"]}Ω {data["Resistance1Status"]}
            R2: {data["Resistance2Value"]}Ω {data["Resistance2Status"]}
            I1: {data["Inductance1Value"]}L {data["Inductance1Status"]}
            I2: {data["Inductance2Value"]}L {data["Inductance2Status"]}
            V1: {data["Voltage1NoLoadValue"]}V {data["Voltage1NoLoadStatus"]}
            V2: {data["Voltage2NoLoadValue"]}V {data["Voltage2NoLoadStatus"]}
            F1: {data["Frequency1Value"]}Hz
            F1: {data["Frequency2Value"]}Hz
            """

            # Configure QR code
            qr = qrcode.QRCode(
                version=3,  # Adjust version for data size
                box_size=4,  # Adjust box size for visual appeal
                border=1,    # Border size
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

        return f"testData/{tcNo}/{tcNo}.png"