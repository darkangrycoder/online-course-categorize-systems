import undetected_chromedriver
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException


def process_category_page(category_url):
    driver = undetected_chromedriver.Chrome()
    driver.get(category_url)
    time.sleep(5)

    '''Sub-category finder'''
    try:
        list_finder = driver.find_element(
            By.XPATH, '/html/body/div[1]/div[2]/div/nav')
        categories = list_finder.find_element(By.XPATH, './ul')
        all_items = categories.find_elements(By.TAG_NAME, 'a')
        names = [tag.get_attribute("href") for tag in all_items]
    except NoSuchElementException:
        print("Element not found")
        return []

    all_courses = []

    for links in names:
        driver.get(links)
        time.sleep(5)

        '''category page range detector'''
        try:
            page_ranges = driver.find_element(
                By.XPATH, '/html/body/div[1]/div[2]/div/div/div[6]/div[2]/nav')
            final_range = page_ranges.find_element(By.XPATH, './span')
            final_value = int(final_range.text)
        except NoSuchElementException:
            print("Skipping that category")
            continue

        courses = []
        '''proceeding all pages'''

        for page_no in range(1, final_value + 1):
            page_urls = f"{links}?p={page_no}"
            driver.get(page_urls)
            print(f"page no {page_no}")
            time.sleep(5)

            '''course body finder'''
            try:
                contants_table = driver.find_element(
                    By.XPATH, '/html/body/div[1]/div[2]/div/div/div[6]/div[2]')
                contants_table_2 = contants_table.find_element(
                    By.XPATH, './div/div[2]')
                anchor_tags = contants_table_2.find_elements(By.TAG_NAME, 'a')

                '''Fomatting course URLs & titles'''

                for tag in anchor_tags:
                    course_name = tag.text.split("\n")[0]
                    course_url = tag.get_attribute("href")
                    courses.append(
                        {'Course Name': course_name, 'URL': course_url})
                print(f"\npage loaded courses{courses}\n")
            except NoSuchElementException:
                print("No course found.....")

        all_courses.extend(courses)

    driver.quit()
    return all_courses


'''Accessing all main categories'''

if __name__ == "__main__":
    category_lists = ["lifestyle", "photography-and-video", "health-and-fitness",
                      "music", "teaching-and-academics", "development", "it-and-software"]

    for categories in category_lists:
        main_url = f"https://www.udemy.com/courses/{categories}/"
        all_courses_data = process_category_page(main_url)

        ''''Save the files according to category name'''
        df = pd.DataFrame(all_courses_data)
        df.to_csv(f'udemy_courses_links_{categories}.csv', index=False)
