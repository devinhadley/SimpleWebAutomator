class Converter:
    def __init__(self, commands, name, config):
        """
        Converts plain text language to selenium commands.
        :param commands - array with command and argument data. Derived from parser class.

        """
        self.selenium_commands = {

            "open": "driver.get()",
            "find": "driver.find_element_by_xpath()",
            "click": ".click()",
            "type": ".send_keys()",
            "wait": "time.sleep()"

        }
        self.filename = name
        self.commands = [self.insert_command(command) for command in commands]
        self.config = config

    def insert_command(self, command):
        if command[0] == "find":
            structured_command = self.selenium_commands["find"]
            index = structured_command.index(")")
            command_with_argument = structured_command[:index] + "\"" + command[2] + "\"" + structured_command[index:]
            return f'\t{command[1]} = {command_with_argument}'

        elif command[0] != "open" and command[0] != "wait":
            structured_command = self.selenium_commands[command[0]]
            index = structured_command.index(")")
            if len(command) == 3:
                command_with_argument = structured_command[:index] + "\"" + command[2] + "\"" + structured_command[index:]
            else:
                command_with_argument = structured_command

            return f'\t{command[1]}{command_with_argument}'
        else:
            structured_command = self.selenium_commands[command[0]]
            index = structured_command.index(")")
            if command[0] == "wait":
                command_with_argument = structured_command[:index] + command[2] + structured_command[
                                                                                                index:]
            else:
                command_with_argument = structured_command[:index] + "\"" + command[2] + "\"" + structured_command[index:]
            return f'\t{command_with_argument}'

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
