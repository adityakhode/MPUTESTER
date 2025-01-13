from PIL import Image, ImageDraw, ImageFont
import json

def load_from_json():
    with open("data.json", "r") as json_file:
        data = json.load(json_file)
        return data
   
image = Image.open("refrenceMaterial/certificate/certificate.png")
font_path = "./refrenceMaterial/certificate/Helvetica.ttf"
data = load_from_json()

draw = ImageDraw.Draw(image)
text_color = (0, 0, 0)  # Black color for the text
font = ImageFont.truetype(font_path, size=35)  # Adjust the size as needed

# Define a reusable function for placing text
def add_text(position, key, fallback="N/A"):
    text = str(data.get(key, fallback))
    draw.text(position, text, font=font, fill=text_color)

# Fill text fields
add_text((280, 290), "TcNo")
add_text((790, 285), "TcDate") 
add_text((1355, 285), "SupplierCode")
add_text((530, 370), "PartyName")
add_text((380, 450), "PartName")
add_text((1230, 448), "PartNo")
add_text((360, 530), "BatchNo")
add_text((1320, 528), "ChallanQuantity")
add_text((410, 610), "ChallanNo")
add_text((1340, 612), "ChallanDate")

# Threading and dimensions
add_text((380, 700), "Threading")
add_text((1220, 700), "Length")
add_text((650, 775), "ThreadingGoNoGoTest", "YES")
add_text((1410, 770), "NoLockNuts")
add_text((510, 840), "NutThickness")
add_text((1430, 840), "NutFlatAcross")
add_text((470, 910), "PinProtrusion")
add_text((1200, 912), "CabelType")
add_text((430, 1132), "Connector1")
add_text((1330, 1132), "Connector2")

# Resistance values
add_text((520, 1335), "Resistance1Value")
add_text((1420, 1325), "Resistance2Value")

# # Voltage Outputs
add_text((430, 1512), "Voltage1NoLoadValue")
add_text((1335, 1512), "Voltage2NoLoadValue")
add_text((435, 1592), "Voltage1_10kLoadValue")
add_text((1340, 1592), "Voltage2_10kLoadValue")
add_text((435, 1672), "Voltage1_3k3LoadValue")
add_text((1340, 1672), "Voltage2_3k3LoadValue")

# # Frequency values
add_text((390, 1748), "FREQUENCY1")
add_text((1290, 1752), "FREQUENCY1")

# # Inductance
add_text((400, 1825), "Inductance1Value", "NA")
add_text((1300, 1825), "Inductance2Value", "NA")

# # Check and Approval
# add_text((330, 1035), "CheckedBy")
# add_text((1200, 1035), "ApprovedBy")

# Save and show the final certificate
output_path = "certificate_with_text.png"
image.save(output_path)
image.show()

print(f"Certificate with text saved to: {output_path}")
