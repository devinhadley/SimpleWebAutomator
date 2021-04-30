class Converter:
    def __init__(self, commands, name, config):
        """
        Converts plain text language to selenium commands.
        :param commands - array with command and argument data. Derived from parser class.

        """
        # Adding repeat command. (for i in range)
        # store indentation value in attribute.
        # indent code based on that until end is found.
        
        # New features:
        # clear text areas

        self.selenium_commands = {

            "open": "driver.get()",
            "find": "driver.find_element_by_xpath()",
            "click": ".click()",
            "type": ".send_keys()",
            "wait": "time.sleep()",
            "repeat":"for i in range():"

        }
        self.indentation_value = 4
        self.filename = name
        self.commands = [self.insert_command(command) for command in commands]
        self.config = config


    # Based on the indentation value, format and return the command.
    def format_indentation(self, command, indentation_num = None):
        if(indentation_num == None):
            indentation_num = self.indentation_value
        for i in range(int(indentation_num /  4)):
            command = "\t" + command

        return command;

    def insert_command(self, command):
        if command[0] == "find":
            structured_command = self.selenium_commands["find"]
            index = structured_command.index(")")
            command_with_argument = structured_command[:index] + "\"" + command[2] + "\"" + structured_command[index:]
            return self.format_indentation(f'{command[1]} = {command_with_argument}')

        elif command[0] == "repeat":
            structured_command = self.selenium_commands["repeat"]
            argumentIndex = structured_command.index(")")
            command_with_argument = structured_command[:argumentIndex] + command[1] + structured_command[argumentIndex:]
            previous_indentation = self.indentation_value
            self.indentation_value = self.indentation_value + 4
            return(self.format_indentation(command_with_argument, previous_indentation))

        elif command[0] == "end":
            self.indentation_value = self.indentation_value - 4
            return self.format_indentation("")


        elif command[0] != "open" and command[0] != "wait":
            structured_command = self.selenium_commands[command[0]]
            index = structured_command.index(")")
            if len(command) == 3:
                command_with_argument = structured_command[:index] + "\"" + command[2] + "\"" + structured_command[
                                                                                                index:]
            else:
                command_with_argument = structured_command

            return self.format_indentation(f'{command[1]}{command_with_argument}')

        else:
            structured_command = self.selenium_commands[command[0]]
            index = structured_command.index(")")
            if command[0] == "wait":
                command_with_argument = structured_command[:index] + command[2] + structured_command[
                                                                                  index:]
            else:
                command_with_argument = structured_command[:index] + "\"" + command[2] + "\"" + structured_command[
                                                                                                index:]
            return self.format_indentation(f'{command_with_argument}')

    def create_python_script(self):
        print(self.config)
        f = open(f'selenium_scripts/{self.filename}.py', "x")
        f.write("import time\n")
        f.write("from selenium import webdriver\n")
        f.write("from selenium.webdriver.common.keys import Keys\n")
        f.write("if __name__ == \"__main__\":\n")
        f.write(f"\tdriver_path = \"{self.config['directory']}\"\n")
        f.write(f"\tdriver = webdriver.Firefox(executable_path=driver_path)\n")
        f.close()

    def write_selenium_code(self):
        f = open(f'selenium_scripts/{self.filename}.py', "a")
        for command in self.commands:
            f.write(f'{str(command)}\n')
