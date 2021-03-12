class Parser:
    def __init__(self, doc):
        """
        :param doc:
        :type text file
        """
        self.document = doc

    def parse_and_return_commands(self):
        """
        :return: Three dimensional array of command, variable, and argument respectively.

        Text document must end with space.
        """

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
        return commands






    def check_command_syntax(self):
        """

        Verifies there are no syntax errors on the document.
        :return: Dictionary with error data.
        """
        self.document
        return {"Error Type": "Line"}

    # return a list of commands which is then processed by selenium port.
