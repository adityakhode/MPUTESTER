# MPU Tester
- Something about the application.

---
# File Structure
```
MPUTESTER/
       |-- Testdata/                   
                    |--1234-Twintech/
                    |--1235-wintech/
       |-- Databases/
                    |--unitMaster.db
                    |--partyMaster.db
                    |--1234-Twintech.db
                    |--1235-Twintech.db
       |-- Scripts/
                   |--databases.py
                   |--main.py
       | --testCases/
                   |--createDatabase.py
                   |--hardwareTest.py
       app.py 
       .gitignore
       .requirments.txt
       .git/
       README.md   
```

---
# Commands To setup  Env

## 1. Clone the package
```
git clone https://github.com/adityakhode/MPUTESTER.git

cd MPUTESTER  
```
## 2. Make a Virtual environment
```
# Create a Virtual Environment
python3 -m venv MPUTestKitEnv

# Activate the environment.
source MPUTestKitEnv/bin/activate 
```

## 3. Install all Requirments
```
sudo apt-get install libcups2-dev #pycups supporting library for printing
pip install -r requirments.txt
```

## 4. Initilise resource
```
pyside6-rcc frontend/assets.qrc -o frontend/resources.py
```
