import os
import json
from modules.modules import Parser, Converter


def create_configuration(driver, driver_directory):
    default_config = {"driver": driver, "directory": driver_directory}
    data = json.dumps(default_config)
    config_file = open("config.json", "w")
    config_file.write(data)
    config_file.close()
    return default_config

def retrieve_configuration():
    with open('config.json') as file:
        return json.load(file)

def show_scripts():
    os.system("clear")
    files = os.listdir("./scripts")
    for val in files:
        print(val)
    print("-----------")

def show_selenium_scripts():
    os.system("clear")
    files = os.listdir("./selenium_scripts")
    for val in files:
        print(val)
    print("-----------")

def main():

    # Load configuration.
    try:
        config = retrieve_configuration()
    except FileNotFoundError:
        print("Enter driver name. ex: geckodriver")
        driver = input()
        os.system("clear")
        print("Enter the driver directory.")
        driver_directory = input()
        config = create_configuration(driver, driver_directory)

    while True:
        os.system("clear")
        print("v - view scripts")
        print("c - create script")
        print("p - parse script")
        print("cs - create selenium script")
        print("r - run selenium script")
        print("Welcome, please enter command.")
        user_input = input()

        if user_input == "v":
            show_scripts()
            user_input = input("Please press enter to continue. ")
        elif user_input == "c":
            os.system("clear")
            print("Enter new file name.")
            user_input = input()
            try:
                file = open(f'scripts/{user_input}.txt', 'x')
            except Exception as e:
                print(e)
                print("Press enter to continue....")
                user_input = input()
        elif user_input == "p":
            show_scripts()
            user_input = input("Enter file name.")
            parsed_document = Parser(open(f'scripts/{user_input}.txt', "r"))
            os.system("clear")
            for val in parsed_document.commands:
                print(val)
            input("Press enter to continue")
        elif user_input == "cs":
            os.system("clear")
            show_scripts()
            user_input = input("Please enter script name: ")
            try:
                file = open(f'scripts/{user_input}.txt', "r")
            except FileNotFoundError:
                os.system("clear")
                print("File not found, press enter to continue.")
                input()
                continue

            os.system("clear")
            parsed_document = Parser(open(f'scripts/{user_input}.txt', "r"))
            errors = parsed_document.check_command_syntax()
            if errors != {}:
                for item in errors:
                    print(item, errors[item])
                input("Press enter to continue.")
                continue
            convert_document = Converter(parsed_document.commands, user_input, config)
            convert_document.create_python_script()
            convert_document.write_selenium_code()
        elif user_input == "r":
            show_scripts()
            user_input = input("Type name of script you wish to run: ")
            parsed_document = Parser(open(f'scripts/{user_input}.txt', "r"))
            errors = parsed_document.check_command_syntax()
            if errors != {}:
                os.system("clear")
                for item in errors:
                    print(item, errors[item])
                input("Press enter to continue.")
                continue
            os.system(f"cd ./selenium_scripts && python3 {user_input}.py")
            input("Press enter to continue....")



if __name__ == '__main__':
    main()
