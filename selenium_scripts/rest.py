import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
if __name__ == "__main__":
	driver_path = "/Users/devinhadley/Development/Python/SimpleWebAutomator/geckodriver"
	driver = webdriver.Firefox(executable_path=driver_path)
