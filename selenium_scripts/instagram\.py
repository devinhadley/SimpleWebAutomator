import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
if __name__ == "__main__":
	driver_path = "/home/devinhadley/Development/Python/SimpleWebAutomator/geckodriver"
	driver = webdriver.Firefox(executable_path=driver_path)
	driver.get("https://www.instagram.com/?hl=en")
	username = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input")
	time.sleep(3)
	username.send_keys("devinhadley")
	password = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input")
	password.send_keys("hadleyd1247")
