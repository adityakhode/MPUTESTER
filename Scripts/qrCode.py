import qrcode
from loadJson import JsonDataHandler
import os

class QrCode:

    # Function Name : makeQr
    # input         : list to paramater to be displayed on qr see from database function "get_result_by_tcno"  and testCertificate Number
    # Output        : void
    # Logic         : make custom qr code using library
    # example       : makeQr(list , tc number)
    def create(tc_no):

        #makes testdata/testCertificate number directory
        os.makedirs(f"testData/{tc_no}", exist_ok=True)
        data = JsonDataHandler.load_data()
        #qrcode text string
        image_url = f"""Company Name : Twintech Control System Pvt Ltd
        Resistance of 1st Coil {data["Resistance1Value"]   } and status is {data["Resistance1Status"]   }
        Resistance of 2nd Coil {data["Resistance2Value"]   } and status is {data["Resistance2Status"]   }
        Inductance of 1st Coil {data["Inductance1Value"]   } and status is {data["Inductance1Status"]   }
        Inductance of 2nd Coil {data["Inductance2Value"]   } and status is {data["Inductance2Status"]   }
        Voltage    of 1st Coil {data["Voltage1NoLoadValue"]} and status is {data["Voltage1NoLoadStatus"]}
        Voltage    of 2nd Coil {data["Voltage2NoLoadValue"]} and status is {data["Voltage2NoLoadStatus"]}
        frequency  of 1st Coil {data["Frequency1Value"]    } and status is {data["Frequency2Value"]     }
        frequency  of 2nd Coil {data["Frequency1Value"]    } and status is {data["Frequency2Value"]     }
        """

        # Create a QR code with desired settings
        qr = qrcode.QRCode(
            version=10,  # Adjust version for data size
            box_size=5,  # Adjust box size for visual appeal
            border=4  
        )
        qr.add_data(image_url)
        qr.make(fit=True)

        # Create an image with default colors
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image
        img.save(f"testData/{tc_no}/{tc_no}.png")

