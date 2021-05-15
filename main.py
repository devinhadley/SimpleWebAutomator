import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from user_interface.ui import Ui_mainWindow
from user_interface.directory import Ui_Directory
import json
import os
import modules.modules as modules
import threading

# Main user interface.
class Main(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.update_dropdown_selections()
        # Check number of scripts in scripts directory.
        if len([item for item in os.listdir('scripts') if item[0] != "."]) > 0:
            self.update_code_editor_text()

        # Signals
        self.comboBox.currentTextChanged.connect(self.on_combobox_changed)
        self.pushButton.clicked.connect(self.on_button_press)
        
        self.current_script_name = os.path.splitext(self.comboBox.currentText())[0]


    def update_dropdown_selections(self):
        for item in os.listdir("scripts"):
            # Prevent adding meta data.
            if item[0] != ".":
                self.comboBox.addItem(item)

    def update_code_editor_text(self):
        if self.comboBox.currentText() != None:
            with open('scripts/'+self.comboBox.currentText()) as file:
                self.plainTextEdit.setPlainText(file.read())
            # Set current script to the script name (not including file extension).
            self.current_script_name = os.path.splitext(self.comboBox.currentText())[0]

    def on_combobox_changed(self):
        self.update_code_editor_text()

    def retrieve_configuration(self):
        with open('config.json') as file:
            return json.load(file)

    def on_button_press(self):
            # Updates the file with the editor content.
            with open('scripts/'+self.current_script_name+'.txt', "w") as file:
                file.write(self.plainTextEdit.toPlainText())
            self.run_selenium_script()

    def run_selenium_script(self):
            # Fetch file name, then remove extension.
            try:
                os.remove(f'selenium_scripts/{self.current_script_name}.py')
            except FileNotFoundError:
                pass

            config = self.retrieve_configuration()

            modules.create_selenium_script(self.current_script_name, config)


# Directory specification pop up window.
class Directory(QtWidgets.QWidget, Ui_Directory):
    def __init__(self, parent = None):
        super(Directory, self).__init__(parent)
        self.setupUi(self)
        # Make it so only directory selection can be clicked.
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.pushButton.clicked.connect(self.create_configuration)

    def create_configuration(self):
        default_config = {"driver": self.find_driver_name(), "directory": self.lineEdit.text()}
        data = json.dumps(default_config)
        config_file = open("config.json", "w")
        config_file.write(data)
        config_file.close()
        # Close the window after saving.
        self.close()
        return default_config

    def find_driver_name(self):
        # Gets the directory path from UI.
        driver_directory = self.lineEdit.text()
        driver_name = ""

        for char in driver_directory[::-1]:
            if char != "/" and char != "\\":
                driver_name += char
            else:
                return driver_name[::-1]


if __name__ == '__main__':

    # Ensure needed directories are present. Creaes them if not.
    if not os.path.isdir("scripts"):
        os.mkdir("scripts")

    if not os.path.isdir("selenium_scripts"):
        os.mkdir("selenium_scripts")

    app = QtWidgets.QApplication(sys.argv)
    main = Main()

    # First check for config, display pop up if doesnt exist.
    try:
        config = main.retrieve_configuration()
    except FileNotFoundError:
        dir_window = Directory()
        dir_window.show()

    main.show()
    sys.exit(app.exec_())
