import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
if __name__ == "__main__":
	driver_path = "/Users/devinhadley/Development/Python/SimpleWebAutomator/geckodriver"
	driver = webdriver.Firefox(executable_path=driver_path)
	driver.get("https://www.youtube.com/")
	time.sleep(2)
	for i in range(5):
		search = driver.find_element_by_xpath("/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div/div[1]/input")
		button = driver.find_element_by_xpath("/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/button")
		search.send_keys("Hello, world!")
		button.click()
		time.sleep(1)
	
	search.send_keys("Woah, that was sick!")
