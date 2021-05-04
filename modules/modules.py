
# Stores the commands into an array and returns.
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
                    f'{index + 1} - Invalid word count: '] = f"Invalid argument count. Should be stop"
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
def format_indentation(command, indentation_num):
    for i in range(int(indentation_num /  4)):
        command = "\t" + command
    return command;

# Converts the parsed text commands to python code.
def convert_commands(commands):

    selenium_commands = {

        "open": "driver.get()",
        "find": "driver.find_element_by_xpath()",
        "click": ".click()",
        "type": ".send_keys()",
        "wait": "time.sleep()",
        "repeat":"for i in range():"

    }

    python_commands = []
    current_indentation = 4
    for command in commands:
        if command[0] == "find":
            structured_command = selenium_commands["find"]
            index = structured_command.index(")")
            command_with_argument = structured_command[:index] + "\"" + command[2] + "\"" + structured_command[index:]
            python_commands.append(format_indentation(f'{command[1]} = {command_with_argument}', current_indentation))

        elif command[0] == "repeat":
            structured_command = selenium_commands["repeat"]
            argumentIndex = structured_command.index(")")
            command_with_argument = structured_command[:argumentIndex] + command[1] + structured_command[argumentIndex:]
            previous_indentation = current_indentation
            current_indentation = current_indentation + 4
            python_commands.append(format_indentation(command_with_argument, previous_indentation))

        elif command[0] == "end":
            current_indentation = current_indentation - 4
            python_commands.append(format_indentation("", current_indentation))


        elif command[0] != "open" and command[0] != "wait":
            structured_command = selenium_commands[command[0]]
            index = structured_command.index(")")
            if len(command) == 3:
                command_with_argument = structured_command[:index] + "\"" + command[2] + "\"" + structured_command[
                                                                                                index:]
            else:
                command_with_argument = structured_command

            python_commands.append(format_indentation(f'{command[1]}{command_with_argument}',current_indentation))

        else:
            structured_command = selenium_commands[command[0]]
            index = structured_command.index(")")
            if command[0] == "wait":
                command_with_argument = structured_command[:index] + command[2] + structured_command[
                                                                                  index:]
            else:
                command_with_argument = structured_command[:index] + "\"" + command[2] + "\"" + structured_command[
                                                                                                index:]
            python_commands.append(format_indentation(f'{command_with_argument}',current_indentation))

    return python_commands

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

