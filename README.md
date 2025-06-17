# MPUTester

**MPUTester** is a desktop GUI application built with **PySide6** for testing Magnetic Pickup Units (MPUs) on Ubuntu Linux systems. It provides a modern interface for real-time sensor data acquisition, QR and certificate generation, and database logging.

## 🎥 Demo Video

[![Watch Demo](https://img.youtube.com/vi/Y0fbIhlIZoM/0.jpg)](https://www.youtube.com/watch?v=Y0fbIhlIZoM&list=PLDbTtMby4HbyvxpOV6Lv6e-EuP07iU_90)  
*Click the image above to watch the demo on YouTube*

---

## 🧩 Features

- 🖼️ PySide6-based modern GUI
- 🔌 Serial communication with MPUs using `pyserial`
- 🧾 Certificate generation using Pillow
- 🔳 QR code generation for test metadata
- 🗃️ SQLite-based local database for party/unit/result management
- 🖨️ Certificate printing via Linux CUPS
- 🔧 Modular structure for easy maintenance and scaling

---

## 🖥️ System Requirements

- **Operating System:** Ubuntu 20.04 / 22.04 or later
- **Python Version:** 3.9+
- **Dependencies:**
  - PySide6
  - pyserial
  - Pillow
  - qrcode
  - pycups
  - sqlite3 (builtin)

---

## ⚙️ Installation (Ubuntu)

### Clone or extract the repository
```bash
git clone https://github.com/adityakhode/MPUTESTER.git
cd MPUTESTER
```

### Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies
```bash
sudo apt-get install libcups2-dev #pycups supporting library for printing
pip install -r requirements.txt
```

### Initilise resource
```bash
pyside6-rcc frontend/assets.qrc -o frontend/resources.py
```

## 🚀 Running the Application
```bash
# Make sure your venv is activated
source venv/bin/activate

# Run the application
python app.py
```
## 👤 Author & Contact
- Made with ❤️ by Aditya Khode, Somesh Mutha, Soham Naik
- 📧 Email: khodeaditya7@gmail.com
📍 Reach out for contributions, feedback, or queries!

MPUTester is optimized for Ubuntu-based laptops and Raspberry Pi devices running low-power environments.
