import os
import undetected_chromedriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)

# Define the problematic link
problematic_link = "https://www.udemy.com/udemy-business/request-demo-mx/?ref=right-rail&locale=en_US"

# Function to filter out the problematic link from URLs


def filter_problematic_links(urls):
    return [url for url in urls if problematic_link not in url]

# Function to find CSV files in a directory


def find_csv_files(directory):
    csv_files = [filename for filename in os.listdir(
        directory) if filename.endswith('.csv')]
    return csv_files

# Function to get output filename based on input filename


def get_output_filename(input_filename):
    base_name, _ = os.path.splitext(input_filename)
    return f"{base_name}_details.csv"


# Initialize the Chrome driver
driver = undetected_chromedriver.Chrome()
driver.set_window_size(1200, 800)

try:
    current_directory = os.getcwd()
    csv_files = find_csv_files(current_directory)

    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        urls = df['URL'].tolist()
        urls = filter_problematic_links(urls)

        scraped_data = []

        for url in urls:
            driver.get(url)
            time.sleep(3)

            # Add your scraping logic here

            '''Titles & Categories scraping'''
            main_body = driver.find_element(By.XPATH, '/html/body')
            try:
                course_body = main_body.find_element(
                    By.CLASS_NAME, "paid-course-landing-page__container")
            except NoSuchElementException:
                print("Skipping....")
            try:
                course_title = course_body.find_element(By.TAG_NAME, 'h1')
            except:
                print("Skipping")
            try:
                course_label = course_body.find_element(
                    By.XPATH, '/html/body/div[1]/div[2]/div/div/main/div[1]/div/div/div[1]/div')
                labels = [course_label.text.replace("\n", ",")]
            except StaleElementReferenceException:
                print("No label found")
                labels = "Nill"

# ... (other imports and code)

            try:
                '''Click Show more button to expand full data if available'''
                button_class = course_body.find_element(
                    By.CSS_SELECTOR, "#main-content-anchor > div.paid-course-landing-page__body > div > div.component-margin.what-you-will-learn--what-will-you-learn--1nBIT > div > button")
                actions = ActionChains(driver)
                actions.move_to_element(button_class).perform()
                button_class.click()
                time.sleep(10)
            except (NoSuchElementException, StaleElementReferenceException):
                print("No button found")
                button_class = None  # Handle the absence of the button differently if needed

            '''Course description scraping'''
            try:
                descriptions = course_body.find_element(
                    By.CLASS_NAME, "paid-course-landing-page__body")
                course_details = descriptions.find_element(
                    By.CLASS_NAME, "what-you-will-learn--content-spacing--3n5NU")
                details = [course_details.text.replace("\n", ",")]
            except (NoSuchElementException, StaleElementReferenceException):
                print("None")
                descriptions = "Nill"
                details = "Nill"

            scraped_data.append({
                "Course Title": course_title.text,
                "Labels": labels,
                "Details": details
            })
            print(f"\n\n{course_title.text}\n{labels}\n{details}\n\n")

        scraped_df = pd.DataFrame(scraped_data)
        output_filename = get_output_filename(csv_file)
        scraped_df.to_csv(output_filename, index=False)
        print(f"Scraped data saved to '{output_filename}'")

finally:
    # Close the driver after scraping
    driver.quit()
