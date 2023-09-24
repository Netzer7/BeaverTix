from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

def claimTickets(username, password):
    wd = uc.Chrome()
    
    wd.get("https://osubeavers.evenue.net/myaccount/login?&shopperContext=ST&fromLegacy=1")
    wd.implicitly_wait(2)

    usernameInput = wd.find_element(By.ID, "user_cred")
    passwordInput = wd.find_element(By.ID, "pass_cred")
    signInButton = wd.find_element(By.NAME, "submitForm")

    usernameInput.send_keys(username)
    passwordInput.send_keys(password)
    signInButton.click()

    while(True):
        pass
    

username = input("Enter your student email or ID number: ")
password = input("Enter your password: ")

claimTickets(username, password)