from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium_stealth import stealth
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
import random 

fallSports = ["football, ", "volleyball", "mensSoccer", "womensSoccer"] 

# Scrapes the event calendar to get event information
def getListOfEvents():
    options = uc.ChromeOptions()
    # Adding argument to disable the AutomationControlled flag 
    options.add_argument("--disable-blink-features=AutomationControlled") 

    # # Exclude the collection of enable-automation switches 
    # options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    # # Turn-off userAutomationExtension 
    # options.add_experimental_option("useAutomationExtension", False) 

    wd = uc.Chrome(options=options)

    stealth(wd,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
    
    wd.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
  
    wd.get("https://osubeavers.evenue.net/cgi-bin/ncommerce3/SEGetEventList?linkID=oregonst&timeDateFrom=2023-9-1-00.00.00&timeDateTo=2024-8-31-23.59.59")
    wd.implicitly_wait(2)
  
    eventDays = wd.find_elements(By.XPATH, '//p[@class="calDay"]')
    for day in eventDays:
        print(day.text)
        currentDayEvent = day.find_element(By.XPATH, 'following-sibling::ul')
        eventTitles = currentDayEvent.find_elements(By.CLASS_NAME, 'calEventTitle]')
        print(eventTitles.text)
        
    while(True):
        pass


def claimTickets(username, password):
    with open("valid_proxies.txt", "r") as f:
        proxies = f.read().split("\n")

    proxyAddress = random.choice(proxies)
    options = uc.ChromeOptions()
    options.add_argument('--proxy-server=%s' % proxyAddress)
    wd = uc.Chrome(chrome_options=options)

    stealth(wd,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
    
    wd.get("https://osubeavers.evenue.net/myaccount/login?&shopperContext=ST&fromLegacy=1")
    wd.implicitly_wait(2)

    try:
        usernameInput = WebDriverWait(wd, 600).until(
        EC.presence_of_element_located((By.ID, "user_cred"))
    )
    except:
        wd.quit()
    
    usernameInput = wd.find_element(By.ID, "user_cred")
    passwordInput = wd.find_element(By.ID, "pass_cred")
    signInButton = wd.find_element(By.NAME, "submitForm")

    usernameInput.send_keys(username)
    wd.implicitly_wait(2)
    passwordInput.send_keys(password)
    wd.implicitly_wait(3)
    signInButton.click()
    wd.implicitly_wait(1)

    # Future TODO Redirect to a selected event page instead of only football. 
    wd.get("https://osubeavers.evenue.net/cgi-bin/ncommerce3/SEGetEventList?groupCode=STFB&linkID=oregonst&shopperContext=ST&caller=&appCode=")

    # Find tickets button
    wd.find_element(By.XPATH, "//td[@class='text-right']//button").click()
    wd.implicitly_wait(1)
    # Add to cart button
    wd.find_element(By.ID, "ev_AddToCart").click()
    wd.implicitly_wait(1)

    # Attempt to close popup modal, if one appears
    try :
        wd.find_element(By.XPATH, "//div[@class='div-close-button']//button").click()
    except:
        pass
    # Checkout button
    wd.find_element(By.ID, "checkout").click()

    # Attempt to close popup modal, if one appears
    try :
        wd.find_element(By.XPATH, "//div[@class='modal-header']//button").click()
    except:
        pass
    # Place order button
    wd.find_element("BY.ID", "btn-place-order").click()

    while(True):
        pass
    

username = input("Enter your student email or ID number: ")
password = input("Enter your password: ")

claimTickets(username, password)

#getListOfEvents()