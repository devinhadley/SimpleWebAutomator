class Parser:
    def __init__(self, doc):

        self.document = doc
        self.commands = None

        # Parse commands from document, store as attribute.
        commands = []
        for line in self.document:
            phrases = line.split()
            for i, val in enumerate(phrases):
                if i == 3:
                    for index, item in enumerate(phrases[3:len(phrases)]):
                        phrases[2] += " " + item
                        phrases.pop(i)
                    break
            commands.append(phrases)
        self.commands = commands

    def check_command_syntax(self):

        global valid_variable
        errors = {}

        # Check for correct number of command/variables/arguments.
        for index, command in enumerate(self.commands):
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

                for item in self.commands[:index]:
                    valid_variable = False
                    if command[1] == item[1] and item[0] == "find":
                        valid_variable = True
                        break

                if not valid_variable:
                    errors[
                        f'{index + 1} - Item {command[1]} not found. '] = "Use command find (item) (xpath) before " \
                                                                          "preforming action. "

        return errors
