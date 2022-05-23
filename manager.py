import re
from selenium import webdriver
def get_phone_numbers(url):
    driver = webdriver.Chrome()
    driver.get(url)
    res = driver.page_source
    dota = res
    phone = re.findall("[\+\d]?(\d{2,3}[-\.\s]??\d{2,3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})", dota)
    res = " ,".join(phone)
    driver.close()
    return(phone)

