'''
File Name: course_link_scraper.py

The Purpose of this file is to scrape the course name, course details, accessible link of the course. In this case, I have built this program to scrape "udemy.com", one of the best leading edtech 
organization in modern education system.

Udemy has more than 350k+ courses (Till July 2023), this program will scrape course name, available URL for the  11 categories and 90+ sub-categories. The purpose of this task is to build a dataset for a project
named "Course Recommendation System".  

Version I have used:

python: 3.8.0
selenium: 4.9.1
undetected-chromedriver: 3.0.0
Google-Chrome-Version: 100.00 ( this version is the best compatible version for web scraping process) 

target_website: udemy.com 

Note: This code had successfully worked till September 2023, later that udemy.com might change the data locator tags and other tools also changed their characteristics. 
'''

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import logging

# Setup logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_driver():
    """Initialize the Selenium WebDriver with undetected-chromedriver."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = uc.Chrome(options=options)
    return driver
	

def get_subcategory_links(driver, category_url):
    """Get subcategory links from a category page."""
    driver.get(category_url)
	
	
   
   try:
        list_finder = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/nav'))
        )
        categories = list_finder.find_element(By.XPATH, './ul')
        all_items = categories.find_elements(By.TAG_NAME, 'a')
        return [tag.get_attribute("href") for tag in all_items]
    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Error finding subcategories: {e}")
        return []
		
	'''
	#pre: the chromedriver will complete the bypassing anti-bot security system and proceed to load the entire body content
	#post: after that this will complete the loading the particular page of a sub-category, for example after loading "development" as main-category, this will load sub-category like programming, hardware, web-development etc. '''
	

def get_page_count(driver):
    """Get the number of pages in a subcategory."""
    try:
        page_ranges = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div/div[6]/div[2]/nav'))
        )
        final_range = page_ranges.find_element(By.XPATH, './span')
        return int(final_range.text)
    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Error finding page count: {e}")
        return 0

def scrape_courses_from_page(driver):
    """Scrape course names and URLs from the current page."""
    try:
        contents_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div/div[6]/div[2]'))
        )
        contents_table_2 = contents_table.find_element(By.XPATH, './div/div[2]')
        anchor_tags = contents_table_2.find_elements(By.TAG_NAME, 'a')

        courses = [{'Course Name': tag.text.split("\n")[0], 'URL': tag.get_attribute("href")} for tag in anchor_tags]
        return courses
    except (NoSuchElementException, TimeoutException) as e:
        logging.error(f"Error scraping courses: {e}")
        return []

	'''pre: after loading the sub-category, this will reach to the first page of each sub-category and load the entire body content
	   post: this will figure out the entire page/tab range of a sub-category that available on udemy.com, some sub-category has 650+ pages, some of less than 100, this will dynamically figure out all ranges and help to load  '''

def process_category_page(category_url):
    """Process all pages of a category and return a list of courses."""
    driver = initialize_driver()
    subcategory_links = get_subcategory_links(driver, category_url)

	'''pre: the charomedriver is looking for links to perform
	post: after accessing to the categor through provided link, it will atart to bypass anti-bot security system and access to the main categoty such as development, life-style, health-and-fitness etc.'''
    
	all_courses = [] #load all acraped data such as course_title, url 
    for subcategory_url in subcategory_links:
        driver.get(subcategory_url)
        page_count = get_page_count(driver)
        
        for page_no in range(1, page_count + 1):
            page_url = f"{subcategory_url}?p={page_no}"
            driver.get(page_url)
            logging.info(f"Processing page {page_no} of {subcategory_url}")
            courses = scrape_courses_from_page(driver)
            all_courses.extend(courses)

			
				'''
				Example: The Complete Full-Stack Web Development Course 2023, https:www.udemy.com/development/web-development/1/The-Complete-Full-Stack-Web-Development-Course-2023
				'''
    driver.quit()
    return all_courses

if __name__ == "__main__":
    category_lists = ["lifestyle", "photography-and-video", "health-and-fitness",
                      "music", "teaching-and-academics", "development", "it-and-software"]
    
	
	#load all categories url 
    for category in category_lists:
        main_url = f"https://www.udemy.com/courses/{category}/"
        logging.info(f"Processing category: {category}")
        all_courses_data = process_category_page(main_url)

		
		#save to csv and logs 
        df = pd.DataFrame(all_courses_data)
        df.to_csv(f'udemy_courses_links_{category}.csv', index=False)
        logging.info(f"Saved {category} data to CSV")
