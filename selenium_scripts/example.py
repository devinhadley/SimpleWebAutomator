import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
if __name__ == "__main__":
	driver_path = "/Users/devinhadley/Desktop/geckodriver"
	driver = webdriver.Firefox(executable_path=driver_path)
	for i in range(5):
		driver.get('https://www.google.com/')
		box = driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
		box.send_keys('Hello, World!')
		button = driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]')
		button.click()