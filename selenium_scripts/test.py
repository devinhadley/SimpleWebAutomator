import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
if __name__ == "__main__":
	driver_path = "/Users/devinhadley/Development/Python/SimpleWebAutomator/geckodriver"
	driver = webdriver.Firefox(executable_path=driver_path)
	driver.get("https://www.google.com/")
	time.sleep(2)
	button = driver.find_element_by_xpath("/html/body/div[1]/div[3]/form/div[2]/div[1]/div[3]/center/input[1]")
	button.click()
	text = driver.find_element_by_xpath("/html/body/div[1]/div[3]/form/div[2]/div[1]/div[3]/center/input[1]")
	for i in range(5):
		text.send_keys("Hello")
	
