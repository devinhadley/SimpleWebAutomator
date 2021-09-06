import os
import sys
from PyQt5.QtWidgets import QMessageBox
from io import StringIO


def lex_document(doc: open) -> list:
    """
    Stores the commands into a list and returns.
    """
    commands = []
    for line in doc:
        # Skip empty lines.
        if not line == "\n":
            phrases = line.split()
            for i, val in enumerate(phrases):
                if i == 3:
                    for index, item in enumerate(phrases[3:len(phrases)]):
                        phrases[2] += " " + item
                        phrases.pop(i)
                    break
            commands.append(phrases)
    return commands


def check_command_syntax(commands: list) -> dict:
    """
    Checks parsed commands for syntax errors.
    Returns a dictionary with any errors.
    """
    errors = {}

    # Check for correct number of command/variables/arguments.
    # Check if command is a supported command.
    for index, command in enumerate(commands):
        if command[0] == "click":
            if len(command) != 2:
                errors[
                    f'{index + 1} - Invalid word count: '] = "Invalid number of words. Should be click (item)."
        elif command[0] == "repeat":
            if len(command) != 2:
                errors[
                    f'{index + 1} - Invalid word count: '] = f"Invalid argument count. Should be repeat (num repeats)"
        elif command[0] == "end":
            if len(command) != 1:
                errors[
                    f'{index + 1} - Invalid word count: '] = "Invalid argument count. Should be stop"
        elif command[0] == "find" or command[0] == "type" or command[0] == "open":
            if len(command) != 3:
                errors[
                    f'{index + 1} - Invalid word count: '] = f"Invalid number of words. Should be {command[0]} (item) (argument). "
        else:
            errors[
                f'{index + 1} - Invalid command'] = f" \"{command[0]}\" not recognized."

    if errors != {}:
        return errors

    # Check that all DOM elements are declared.
    for index, command in enumerate(commands):
        if command[0] == "click" or command[0] == "type":
            valid_variable = False
            for item in commands[:index]:
                if item[0] == "find" and command[1] == item[1]:
                    valid_variable = True
                    break

            if not valid_variable:
                errors[
                    f'{index + 1} - Item {command[1]} not found. '] = "Use command find (item) (xpath) before " \
                                                                      "preforming action. "

    # Check that repeats have a corresponding end.
    # This check should only run once.

    ends_to_find = 0
    for index, command in enumerate(commands):
        if command[0] == "repeat":
            ends_to_find += 1
        if command[0] == "end":
            ends_to_find -= 1
    if ends_to_find < 0:
        errors[
            'Too many ends. Missing corresponding repeat statements'] = "Make sure you don\'t have any extra end commands."
    elif ends_to_find > 0:
        errors[
            'Missing ends. Repeat needs end statement.'] = "Make sure you have a corresponding end with your repeat command."

    return errors


def format_indentation(command: str, indentation_num: int) -> str:
    """
    Formats the command to use the correct indentation. 
    """
    return "\t" * (indentation_num // 4) + command


def convert_commands(commands: list) -> dict:
    """
    Converts the lexed text commands to python code.
    """
    selenium_commands = {

        "open": "driver.get({argument})",
        "find": """WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, {argument}))
    )""",
        "click": ".click()",
        "type": ".send_keys({argument})",
        "wait": "time.sleep({argument})",
        "repeat": "for i in range({argument}):"

    }

    python_commands = []
    current_indentation = 0
    for command in commands:
        if command[0] == "find":
            structured_command = selenium_commands["find"]
            command_with_argument = structured_command.format(
                argument=repr(command[2]))
            python_commands.append(format_indentation(
                f'{command[1]} = {command_with_argument}', current_indentation))

        elif command[0] == "repeat":
            structured_command = selenium_commands["repeat"]
            command_with_argument = structured_command.format(
                argument=command[1])
            previous_indentation = current_indentation
            current_indentation = current_indentation + 4
            python_commands.append(format_indentation(
                command_with_argument, previous_indentation))

        elif command[0] == "end":
            current_indentation = current_indentation - 4

        elif command[0] == "click" or command[0] == "type":
            structured_command = selenium_commands[command[0]]
            if len(command) == 3:
                command_with_argument = structured_command.format(
                    argument=repr(command[2]))
            else:
                command_with_argument = structured_command

            python_commands.append(format_indentation(
                f'{command[1]}{command_with_argument}', current_indentation))

        else:
            structured_command = selenium_commands[command[0]]
            if command[0] == "wait":
                command_with_argument = structured_command.format(
                    argument=command[2])
            else:
                command_with_argument = structured_command.format(
                    argument=repr(command[2]))
            python_commands.append(format_indentation(
                f'{command_with_argument}', current_indentation))

    return python_commands


def create_python_script(config: dict, file_name: str) -> bool:
    """
    Creates a python file based on the user's config.
    Also imports needed modules.
    Returns false if the driver is not supported.
    """
    with open(f'selenium_scripts/{file_name}.py', "x") as f:
        if "geckodriver" in config['driver'].lower():
            driver_assignment = "driver = webdriver.Firefox(executable_path=PATH)\n"
        elif "chromedriver" in config['driver'].lower():
            driver_assignment = "driver = webdriver.Chrome(executable_path=PATH)\n"
        else:
            return False
        f.write("import time\n")
        f.write("from selenium import webdriver\n")
        f.write("from selenium.webdriver.common.keys import Keys\n")
        f.write(f"from selenium.webdriver.common.by import By\n")
        f.write(f"from selenium.webdriver.support.ui import WebDriverWait\n")
        f.write(f"from selenium.webdriver.support import expected_conditions as EC\n")
        f.write(f"PATH = \"{config['directory']}\"\n")
        f.write(driver_assignment)

        f.close()
        return True


def write_selenium_code(file_name: str, commands: dict) -> None:
    """
    Writes python commands to a file.
    """
    with open(f'selenium_scripts/{file_name}.py', "a") as f:
        for command in commands:
            f.write(f'{str(command)}\n')


def create_selenium_script(file_name: str, config: dict) -> bool:
    """
    Creates a selenium script using commands derived from txt file.
    Returns true if success, false if not.
    """
    # Create the script.
    if not create_python_script(config, file_name):
        print("Driver is not supported or incorrect driver name.")
        print("Please ensure the driver name specified in the config is correct.")
        return False

    # If anything fails, want to delete the Python script.
    try:
        document = open(f'scripts/{file_name}.txt')

        # Parse the commands.
        commands = lex_document(document)

        # Check for errors.
        errors = check_command_syntax(commands)
        if errors != {}:
            formatted_errors = ""
            for error in errors:
                formatted_errors += error + " "
                formatted_errors += errors[error] + "\n"
            error_dialogue = QMessageBox()
            error_dialogue.setWindowTitle("Syntax Error")
            error_dialogue.setText(formatted_errors)
            error_dialogue.exec_()
            return True

        # Convert commands to python.
        converted_commands = convert_commands(commands)

        # Write python code to the existing file.
        write_selenium_code(file_name, converted_commands)

        # Redirect the console output to display in UI.
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        exec(open(f"./selenium_scripts/{file_name}.py").read(), globals())
        sys.stdout = old_stdout

        error_dialogue = QMessageBox()
        if redirected_output.getvalue() == "":
            error_dialogue.setText("Selenium reported no issues!")
        else:
            error_dialogue.setText(redirected_output.getvalue())

        error_dialogue.exec_()

    except Exception as e:

        error_dialogue = QMessageBox()
        error_dialogue.setWindowTitle("Program Error")
        error_dialogue.setText(str(e))
        error_dialogue.exec_()
        os.remove(f'selenium_scripts/{file_name}.py')
        print(e)

        return False

    return True


def run_selenium_script(file_name: str, config: dict) -> None:
    os.remove(f'selenium_scripts/{file_name}.py')
    create_selenium_script(file_name, config)
