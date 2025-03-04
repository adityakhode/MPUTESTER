from PySide6 import QtUiTools  # For loading .ui files
from PySide6.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        # Load the .ui file using QtUiTools
        self.load_ui('frontend/untitled.ui')

        # Access the QComboBox by its object name
        self.partNoList = self.findChild(QComboBox, "partNoList")  # Replace "comboBox" with the actual object name

        # Access the QLabel by its object name
        self.label = self.findChild(QLabel, "label")

        # Example: Connect the currentIndexChanged signal to a slot
        self.partNoList.currentIndexChanged.connect(self.on_combo_box_changed)

    def load_ui(self, ui_file):
        # Load the .ui file using QtUiTools
        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile(ui_file)
        ui_file.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.setCentralWidget(self.ui)

    # Slot for combo box index changed event
    def on_combo_box_changed(self, index):
        selected_text = self.partNoList.currentText()
        print(f"Selected option: {selected_text} (Index: {index})")
        self.label.setText(selected_text)

    def updateList(self, arr):
        for elements in arr:
            self.partNoList.addItem(str(elements))
