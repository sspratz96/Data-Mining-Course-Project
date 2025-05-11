import pandas as pd
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Safari()
driver.set_window_size(1100, 900)

df = pd.DataFrame(columns=['Position', 'Link'])

driver.get('https://www.stepstone.de/jobs/data-engineer')

soup = BeautifulSoup(driver.page_source, features="lxml")
time.sleep(5)

# Accept cookies 
element = driver.find_element(By.CSS_SELECTOR, "#ccmgt_explicit_accept")
element.click()
time.sleep(5)
# Close the stepstone popup
button = driver.find_element(By.CSS_SELECTOR, 'img[src="https://static-assets.qualtrics.com/static/prototype-ui-modules/SharedGraphics/siteintercept/svg-close-btn-black-7.svg"]')
button.click()
time.sleep(5)

# Total page number for DS=15, DE=35
page_number = 35
count_page = 1

# Go to each page and extract all card links
for _ in range(page_number):
    # Get the height of the entire document
    document_height = driver.execute_script("return document.body.scrollHeight;")

    # Calculate the desired scroll position (e.g., 80% before the end)
    scroll_position = int(document_height * 0.73)

    # Scroll to the desired position
    driver.execute_script("window.scrollTo(0, %d);" % scroll_position)
    time.sleep(5)

    # Find job card
    h2_elements = driver.find_elements(By.CSS_SELECTOR, "h2[data-genesis-element='BASE']")

    # Initialize lists to store href and text
    href_list = []
    text_list = []

    # Iterate through each job card
    for h2_element in h2_elements:
        # Extract title from the job card
        text = h2_element.text.strip()

        # Find the card button with link
        button_element = h2_element.find_element(By.TAG_NAME, "a")

        # Extract the link from the card
        href = button_element.get_attribute("href")

        href_list.append(href)
        text_list.append(text)

    new_df = pd.DataFrame({'Position': text_list, 'Link': href_list})
    df = pd.concat([df, new_df], ignore_index=True)
    time.sleep(3)

    # Go to the next page by clicking next button
    count_page+=1
    if(count_page<=page_number):
        # Css selector for DS: res481, DE: res485
        button = driver.find_element(By.CSS_SELECTOR, "#stepstone-pagination-res485 > ul > li:nth-child(9) > a")
        button.click()
        time.sleep(5)

df.to_excel('DE.xlsx', index=False)

driver.quit()