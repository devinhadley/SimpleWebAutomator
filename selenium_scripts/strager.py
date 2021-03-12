import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
if __name__ == "__main__":
	driver_path = "/home/devinhadley/PycharmProjects/WebAutomator/geckodriver"
	driver = webdriver.Firefox(executable_path=driver_path)
	driver.get("https://www.twitch.tv/strager")
	time.sleep(4)
	chat = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div/div/div/div/section/div/div[5]/div[2]/div[1]/div/div[2]/div/div/div[1]/textarea")
	chat.click()
	time.sleep(1)
	button = driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div/div/div/div[3]/button")
	button.click()
	chat.send_keys("Strager like men?")
