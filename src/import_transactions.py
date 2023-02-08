from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
import time 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
from dotenv import load_dotenv
load_dotenv()

# ================== FUNCTIONS ==================

print('=====================')
print(os.environ.get('CHROME_USER_DATA_DIR'))
print('=====================')

def init_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument(r"user-data-dir=" + os.environ.get('CHROME_USER_DATA_DIR'))
    chrome_options.set_capability("browserVersion", "98")
    if os.environ.get('ENV') == 'docker':
        driver = webdriver.Remote(
            "http://chrome:4444/wd/hub", 
            DesiredCapabilities.CHROME,
            options=chrome_options
        )
    else:
        driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://web.moneylover.me/")
    return driver

def wait_for_xpath(xpath, driver):
    return WebDriverWait(driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))

def click_when_clickable(xpath, driver, scrollIntoView=False):
    element = wait_for_xpath(xpath, driver)
    if scrollIntoView:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
    try:
        WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable(element)).click()
    except:
        element.click()

def enter_text(xpath, text, driver):
    element = wait_for_xpath(xpath, driver)
    element.send_keys(text)

def parse_date(cell):
    # check if cell is a timestamp
    if isinstance(cell, datetime):
        return cell.year, cell.strftime("%b"), cell.day
    try:
        date = datetime.strptime(cell, '%d/%m/%Y')
    except:
        date = datetime.strptime(cell, '%d-%b-%Y')
    return date.year, date.strftime("%b"), date.day

def parse_amount(row):
    if 'Change' in row:
        return abs(row['Change'])
    elif float(str(row['Withdraw']).replace(',', '')) > 0:
        return str(row['Withdraw']).replace(',', '')
    else:
        return str(row['Deposit']).replace(',', '')

def login(driver):
    email = wait_for_xpath('//*[@id="input-26"]', driver)
    email.send_keys(os.environ.get('MONEYLOVER_USER_NAME'))
    password = driver.find_element(by=By.XPATH, value='//*[@type="password"]')
    password.send_keys(os.environ.get('MONEYLOVER_PASSWORD'))
    login_button = driver.find_element(by=By.XPATH, value='//*[@id="app-wrap"]/div/div[2]/div/div[2]/div[3]/form/button')
    login_button.click()

# ================== VALIDATION ==================

valid_categories = ['Food & Beverage', 'Restaurants', 'Café', 'Bills & Utilities', 'Phone Bill', 'Water Bill', 'Electricity Bill', 'Gas Bill', 'Television Bill', 'Internet Bill', 'Rentals', 'Transportation', 'Taxi', 'Parking Fees', 'Petrol', 'Maintenance', 'Shopping', 'Clothing', 'Footwear', 'Accessories', 'Electronics', 'Friends & Lover', 'Entertainment', 'Movies', 'Games', 'Travel', 'Health & Fitness', 'Sports', 'Doctor', 'Pharmacy', 'Personal Care', 'Gifts & Donations', 'Marriage', 'Funeral', 'Charity', 'Family', 'Children & Babies', 'Home Improvement', 'Home Services', 'Pets', 'Education', 'Books', 'Investment', 'Business', 'Insurances', 'Fees & Charges', 'Withdrawal', 'Other Expense', 'Award', 'Interest Money', 'Salary', 'Gifts', 'Selling', 'Other Income']
valid_titles = ['Expense', 'Income']
wallets = list(pd.read_excel('data/transactions.xlsx', None).keys())
all_titles = []
all_categories = []
for wallet in wallets:
    df = pd.read_excel('data/transactions.xlsx', sheet_name=wallet)
    categories = df['Category']
    all_titles = all_titles + list(map(lambda x: x.split('|')[0], categories))
    all_categories = all_categories + list(map(lambda x: x.split('|')[1], categories))

unique_titles = list(set(all_titles))
unique_categories = list(set(all_categories))

# check if all titles are present in valid_titles
for title in unique_titles:
    if title not in valid_titles:
        raise Exception('Invalid title: ' + title)

# check if all categories are present in valid_categories
for category in unique_categories:
    if category not in valid_categories:
        raise Exception('Invalid category: ' + category)


# ================== MAIN ==================

# Init driver
driver = init_driver()

# Login
print("Logging in")
login(driver)
print("Logging success")

# # Tabs
# tabs = {
#     "Expense": 2,
#     "Income": 3
# }

# # Read excel
# wallets = list(pd.read_excel('data/transactions.xlsx', None).keys())

# for wallet in wallets:
#     df = pd.read_excel('data/transactions.xlsx', sheet_name=wallet)
#     for idx, row in df.iterrows():

#         tab = row['Category'].split('|')[0]
#         category = row['Category'].split('|')[1]
#         tab_id = tabs[tab]
#         print(wallet + "-" + str(idx))
#         amount = parse_amount(row)
#         year, month, date = parse_date(row['Date'])

#         # Open transaction modal
#         click_when_clickable('//button[.//*[contains(text(), "Add transaction")]]', driver)
        
#         # Click wallet dropdown
#         click_when_clickable('(//*[@title="Wallet"]/div[contains(@class, "search-border")])[2]', driver)
        
#         # Select wallet
#         click_when_clickable('//div[contains(@class, "focus-wallet") and .//*[contains(text(), "' + wallet + '")]]', driver, True)
        
#         # Open category dropdown
#         click_when_clickable('(//*[@title="Category"]/div[contains(@class, "search-border")])[2]', driver)

#         # Select category tab
#         click_when_clickable('//div[contains(@class, "tab-item") and .//*[contains(text(), "' + tab + '")]]', driver)

#         # Select category
#         click_when_clickable('//div[@id="tab-' + str(tab_id) + '"]//div[(contains(@class, "category-item") or contains(@class, "child-category-item")) and .//*[contains(text(), "' + category + '")]]', driver, True)

#         # Open date modal
#         click_when_clickable('(//*[@title="Date"]/div[contains(@class, "search-border")])[2]', driver)

#         # Select date
#         click_when_clickable('//div[contains(@class, "picker-date")]//div[contains(@class, "v-date-picker-title__year")]', driver)
#         time.sleep(1)        
#         click_when_clickable('//ul[contains(@class, "v-date-picker-years")]//li[contains(text(), "' + str(year) + '")]', driver, True) # Year 2023
#         time.sleep(1)        
#         click_when_clickable('//*[text()="' + month + '"]/..', driver, True) # month Jan
#         time.sleep(1)        
#         click_when_clickable('//*[contains(@class, "v-date-picker-table--date")]//*[text()="' + str(date) + '"]/..', driver, True) # date 31
#         time.sleep(1)

#         # Enter amount
#         enter_text('//div[contains(@class, "v-dialog--active")]//div[contains(@class, "amount")]//input', amount, driver)

#         # Enter note
#         enter_text('//div[contains(@class, "v-dialog--active")]//div[contains(@class, "note")]//input', row['Note'], driver)
#         time.sleep(1)

#         # Save transaction
#         click_when_clickable('//div[contains(@class, "v-dialog--active")]//div[contains(@class, "transaction-dialog")]//div[contains(@class, "transaction-action")]//button[contains(@class, "done")]', driver)
#         time.sleep(5)
