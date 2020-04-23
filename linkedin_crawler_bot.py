import imp
import re
import sys
from time import sleep

from parsel import Selector
from selenium import webdriver

imp.reload(sys)



def load_chrome_web_driver(path):
    driver = webdriver.Chrome(path)
    return driver

def phantom_buster(path):
    driver = webdriver.PhantomJS(executable_path=path)
    return driver

def find_element_by_id_name(id, value, driver, sleep_time):
    field_value = driver.find_element_by_id(id)
    field_value.send_keys(value)
    sleep(sleep_time)

def button_click(driver):
    sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
    sign_in_button.click()
    sleep(1.5)

def collect_name(selector):
    name = selector.xpath('//*[starts-with(@class, "inline t-24 t-black t-normal break-words")]/text()').extract_first()
    return name

def collect_companies(selector):
    companies = selector.xpath('//*[starts-with(@class, "pv-entity__secondary-title t-14 t-black t-normal")]/text()').getall()
    return companies

def collect_designations(selector):
    designations = selector.xpath('//li//div//div//a//div//h3[starts-with(@class, "t-16 t-black t-bold")]/text()').getall()
    return designations

def collect_companies_start_end_date(selector):
        
    dates = selector.xpath('//li//div//div//a//div//div//h4[starts-with(@class, "pv-entity__date-range t-14 t-black--light t-normal")]//span/text()').getall()
    dates = [date for date in dates if date != 'Dates Employed']
    dates = [re.sub('–', '-', date) for date in dates]
    return dates

def collect_location(selector):
    location = selector.xpath('//*[starts-with(@class, "t-16 t-black t-normal inline-block")]/text()').extract_first()
    return location
        

def collect_university(selector):
    universities = selector.xpath('//*[starts-with(@class, "pv-entity__school-name t-16 t-black t-bold")]/text()').getall()
    return universities

def collect_studies(selector):
    studies = selector.xpath('//*[starts-with(@class, "pv-entity__comma-item")]/text()').getall()
    return studies
    
def collect_universities_studies_time(selector):
    time = selector.xpath('//*[starts-with(@class, "pv-entity__dates t-14 t-black--light t-normal")]//span//time/text()').getall()
    return time



if __name__=="__main__":

    path = '../../chromedriver_linux64/chromedriver'
    #path = '../phantomjs-2.1.1-linux-x86_64/bin/phantomjs'

    linkedin_username = '' # your username
    linkedin_password = '' # your password

    driver = load_chrome_web_driver(path=path)
    #driver = obj.phantom_buster(path=path)
    driver.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')
    
    find_element_by_id_name(id='username', value=linkedin_username, driver=driver, sleep_time=1.5)
    find_element_by_id_name(id='password', value=linkedin_password, driver=driver, sleep_time=1.5)

    button_click(driver=driver)

    user_acc = '' # user profile account link which you want to crawl
    driver.get(user_acc)
    sleep(3)

    sel = Selector(text=driver.page_source)
    name = collect_name(selector=sel)
    location = collect_location(selector=sel)
    companies = collect_companies(selector=sel)
    designations = collect_designations(selector=sel)
    companies_start_end_date = collect_companies_start_end_date(selector=sel)
    universities = collect_university(selector=sel)
    studies = collect_studies(selector=sel)
    universities_studies_time = collect_universities_studies_time(selector=sel)


    print(name, location)
    print(companies, designations, companies_start_end_date)
    print(universities, studies, universities_studies_time)

    driver.quit()

