import os

# Stores the commands into an array and returns.
# rename lex_document
# Look into using split(" ", 3)
def parse_document(doc):
    commands = []
    for line in doc:
        phrases = line.split()
        for i, val in enumerate(phrases):
            if i == 3:
                for index, item in enumerate(phrases[3:len(phrases)]):
                    phrases[2] += " " + item
                    phrases.pop(i)
                break
        commands.append(phrases)
    return commands


# Checks parsed commands for syntax errors.
# Returns a dictionary with any errors.
def check_command_syntax(commands):
    errors = {}

    # Check for correct number of command/variables/arguments.
    for index, command in enumerate(commands):
        if command[0] == "click":
            if len(command) != 2:
                errors[f'{index + 1} - Invalid word count: '] = "Invalid number of words. Should be click (item)."
        elif command[0] == "repeat":
            if(len(command) != 2):
                errors[
                    f'{index + 1} - Invalid word count: '] = f"Invalid argument count. Should be repeat (num repeats)"
        elif command[0] == "end":
            if(len(command) != 1):
                errors[
                    f'{index + 1} - Invalid word count: '] = "Invalid argument count. Should be stop"
        else:
            if len(command) != 3:
                errors[
                    f'{index + 1} - Invalid word count: '] = f"Invalid number of words. Should be {command[0]} (item) (argument). "

        if errors != {}:
            return errors

        # Check that all "variables" are declared.
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

    # Check that repeats have a coresponding end.
    # This check should only run once.

    endsToFind = 0
    for index, command in enumerate(commands):
        if command[0] == "repeat":
            endsToFind += 1
        if command[0] == "end":
            endsToFind -= 1 
    if endsToFind < 0:
        errors['Too many ends. Missing corresponding repeat statements'] = "Make sure you don\'t have any extra end commands."
    elif endsToFind > 0:
        errors['Missing ends. Repeat needs end statement.'] = "Make sure you have a corresponding end with your repeat command."

    return errors



# Format the correct indentation 
# Use * string instead of looping.

def format_indentation(command, indentation_num):
    return "\t" * (indentation_num  // 4) + command;

# Converts the parsed text commands to python code.
def convert_commands(commands):

    selenium_commands = {

        "open": "driver.get({argument})",
        "find": "driver.find_element_by_xpath({argument})",
        "click": ".click()",
        "type": ".send_keys({argument})",
        "wait": "time.sleep({argument})",
        "repeat":"for i in range({argument}):"

    }

    python_commands = []
    current_indentation = 4
    for command in commands:
        if command[0] == "find":
            structured_command = selenium_commands["find"]
            command_with_argument = structured_command.format(argument = repr(command[2])) 
            python_commands.append(format_indentation(f'{command[1]} = {command_with_argument}', current_indentation))

        elif command[0] == "repeat":
            structured_command = selenium_commands["repeat"]
            command_with_argument = structured_command.format(argument = command[1])
            previous_indentation = current_indentation
            current_indentation = current_indentation + 4
            python_commands.append(format_indentation(command_with_argument, previous_indentation))

        elif command[0] == "end":
            current_indentation = current_indentation - 4


        elif command[0] == "click" or command[0] == "type":
            structured_command = selenium_commands[command[0]]
            if len(command) == 3:
                command_with_argument = structured_command.format(argument = repr(command[2]))
            else:
                command_with_argument = structured_command

            python_commands.append(format_indentation(f'{command[1]}{command_with_argument}',current_indentation))

        else:
            structured_command = selenium_commands[command[0]]
            if command[0] == "wait":
                command_with_argument = structured_command.format(argument = command[2])
            else:
                command_with_argument = structured_command.format(argument=repr(command[2]))
            python_commands.append(format_indentation(f'{command_with_argument}',current_indentation))

    return python_commands

# Combine this into write Selenium code.
# Creates a python file based on the user's config.
# Also imports needed modules.
def create_python_script(config, file_name):
        f = open(f'selenium_scripts/{file_name}.py', "x")
        f.write("import time\n")
        f.write("from selenium import webdriver\n")
        f.write("from selenium.webdriver.common.keys import Keys\n")
        f.write("if __name__ == \"__main__\":\n")
        f.write(f"\tdriver_path = \"{config['directory']}\"\n")
        f.write(f"\tdriver = webdriver.Firefox(executable_path=driver_path)\n")
        f.close()


# Writes python commands to a file.
def write_selenium_code(file_name, commands):
    f = open(f'selenium_scripts/{file_name}.py', "a")
    for command in commands:
        f.write(f'{str(command)}\n')

# Creates a selenium script using commands derived from txt file.
# Returns true if success, false if not.
def create_selenium_script(file_name, config):

    # Create the script.
    create_python_script(config, file_name)

    # If anything fails, want to delete the Python script.
    try:
        document = open(f'scripts/{file_name}.txt')

        # Parse the commands.
        commands = parse_document(document)

        # Check for errors.
        errors = check_command_syntax(commands)
        if errors != {}:
            for error in errors:
                print(error, errors[error])
            return False

        # Convert commands to python.
        converted_commands = convert_commands(commands)

        # Write python code to the existing file.
        write_selenium_code(file_name, converted_commands)

        os.system(f"cd ./selenium_scripts && python3 {file_name}.py")

    except Exception as e:
        print("An error occured, deleting file:", file_name)
        os.remove(f'selenium_scripts/{file_name}.py')
        print(e+"\n\n")

        return False



    return True

def run_selenium_script(file_name, config):
        os.remove(f'selenium_scripts/{file_name}.py')
        create_selenium_script(file_name, config)

