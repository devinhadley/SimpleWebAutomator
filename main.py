import os
import platform
import json
import modules.modules as modules

# Clear command is dependent on OS.
def retrieve_clear_command():
    if platform.system() == "Linux" or platform.system() == "Darwin":
        return "clear"
    else:
        return "cls"


# Creates a config, saves as config.json.
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

# Prints txt scripts in directory.
def show_scripts():
    files = os.listdir("./scripts")
    for val in files:
        print(val)
    print("-----------")


def main():
    CLEAR = retrieve_clear_command()

    # Load configuration if it doesnt exist, make it.
    try:
        config = retrieve_configuration()
    except FileNotFoundError:
        print("Enter driver name. ex: geckodriver")
        driver = input()
        os.system(CLEAR)
        print("Enter the driver directory.")
        driver_directory = input()
        config = create_configuration(driver, driver_directory)

    while True:
        os.system(CLEAR)
        print("v - view scripts")
        print("c - create script")
        print("r - run script")
        print("Welcome, please enter command.")
        user_input = input()

        if user_input == "v":
            os.system(CLEAR)
            show_scripts()
            user_input = input("Please press enter to continue. ")
        elif user_input == "c":
            os.system(CLEAR)
            print("Enter new file name.")
            user_input = input()
            try:
                open(f'scripts/{user_input}.txt', 'x')
            except Exception as e:
                print(e)
                print("Press enter to continue....")
                user_input = input()
        elif user_input == "r":
            os.system(CLEAR)
            show_scripts()
            user_input = input("Please enter script name: ")
            try:
                # Switch to use .access() to see if file is found.
                open(f'selenium_scripts/{user_input}.py', "r")
                modules.run_selenium_script(user_input, config)
                input()

            # If the file is not found.
            except IOError:
                if not modules.create_selenium_script(user_input, config):
                    # If creating the script fails.
                    input('Press any key to continue')

                input()
                continue


if __name__ == '__main__':
    main()
