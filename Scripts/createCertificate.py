from PIL import Image, ImageDraw, ImageFont
import json


class Certificate:
    def __init__(self, output_path = "certificate_with_text.png"):
        self.image = Image.open("refrenceMaterial/certificate/certificate.png")
        font_path = "./refrenceMaterial/certificate/Helvetica.ttf"
        self.text_color = (0, 0, 0)  # Black color for the text
        self.font = ImageFont.truetype(font_path, size=35)  # Adjust the size as needed
        self.draw = ImageDraw.Draw(self.image)
        self.output_path = output_path
        self.data = self.load_from_json()
        self.fill_details()
        self.data = []

    def fill_details(self):
        # Fill text fields
        self.add_text((280, 290), "TcNo")
        self.add_text((790, 285), "TcDate") 
        self.add_text((1355, 285), "SupplierCode")
        self.add_text((530, 370), "PartyName")
        self.add_text((380, 450), "PartName")
        self.add_text((1230, 448), "PartNo")
        self.add_text((360, 530), "BatchNo")
        self.add_text((1320, 528), "ChallanQuantity")
        self.add_text((410, 610), "ChallanNo")
        self.add_text((1340, 612), "ChallanDate")

        # Threading and dimensions
        self.add_text((380, 700), "Threading")
        self.add_text((1220, 700), "Length")
        self.add_text((650, 775), "ThreadingGoNoGoTest", "YES")
        self.add_text((1410, 770), "NoLockNuts")
        self.add_text((510, 840), "NutThickness")
        self.add_text((1430, 840), "NutFlatAcross")
        self.add_text((470, 910), "PinProtrusion")
        self.add_text((1200, 912), "CabelType")
        self.add_text((430, 1132), "Connector1")
        self.add_text((1330, 1132), "Connector2")

        # Resistance values
        self.add_text((520, 1335), "Resistance1Value")
        self.add_text((1420, 1325), "Resistance2Value")

        # # Voltage Outputs
        self.add_text((430, 1512), "Voltage1NoLoadValue")
        self.add_text((1335, 1512), "Voltage2NoLoadValue")
        self.add_text((435, 1592), "Voltage1_10kLoadValue")
        self.add_text((1340, 1592), "Voltage2_10kLoadValue")
        self.add_text((435, 1672), "Voltage1_3k3LoadValue")
        self.add_text((1340, 1672), "Voltage2_3k3LoadValue")

        # # Frequency values
        self.add_text((390, 1748), "FREQUENCY1")
        self.add_text((1290, 1752), "FREQUENCY1")

        # # Inductance
        self.add_text((400, 1825), "Inductance1Value", "NA")
        self.add_text((1300, 1825), "Inductance2Value", "NA")

        # # Check and Approval
        # self.add_text((330, 1035), "CheckedBy")
        # self.add_text((1200, 1035), "ApprovedBy")

        # Save and show the final certificate
        
        self.image.save(self.output_path)
        #self.image.show()

        print(f"Certificate with text saved to: {self.output_path}")

    def load_from_json(self):
        with open("data.json", "r") as json_file:
            data = json.load(json_file)
            return data

    # Define a reusable function for placing text
    def add_text(self,position, key, fallback="N/A"):
        text = str(self.data.get(key, fallback))
        self.draw.text(position, text, font=self.font, fill=self.text_color)




