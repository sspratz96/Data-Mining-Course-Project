import pandas as pd

from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

driver = webdriver.Safari()

# Load the Excel file containing links
df_link = pd.read_excel('unscrapable_links.xlsx')

# Define CSS selectors for job elements
selectors = {
    'Job': 'span.job-ad-display-4vegif',
    'Company': 'li.at-listing__list-icons_company-name.job-ad-display-62o8fr',
    'Location': 'li.at-listing__list-icons_location.map-trigger.job-ad-display-62o8fr',
    'Contract type': 'li.at-listing__list-icons_contract-type.job-ad-display-62o8fr',
    'Work type': 'li.at-listing__list-icons_work-type.job-ad-display-62o8fr',
    'Date': 'li.at-listing__list-icons_date.job-ad-display-zoyosf',
    'About company': 'div.at-section-text-introduction.job-ad-display-cl9qsc',
    'Job description': 'div.at-section-text-description.job-ad-display-cl9qsc',
    'Requirements': 'div.at-section-text-profile.job-ad-display-cl9qsc',
    'Benefits': 'div.at-section-text-benefits.job-ad-display-cl9qsc'
}

# Function to find an element by CSS selector or return a placeholder if not found
def find_element_or_placeholder(selector):
    try:
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        return element.text.strip()
    except:
        return '________________________'

# Function to scrape elements from a URL
def scrape_elements(url):
    try:
        driver.get(url)
    except TimeoutException:
        print(f"TimeoutException: Couldn't open the page for URL: {url}. Moving to the next URL.")
        return None
    
    # Accept cookies if present
    try:
        accept_button = driver.find_element(By.ID, "ccmgt_explicit_accept")
        accept_button.click()
    except NoSuchElementException:
        pass
    
    # Check if the job element is present on the page (for identification of page error)
    if not driver.find_elements(By.CSS_SELECTOR, selectors['Job']):
        print(f"No job information found on the page for URL: {url}. Moving to the next URL.")
        return None

    # Find and collect job elements
    soup = BeautifulSoup(driver.page_source, features="lxml")
    data = {}
    for key, selector in selectors.items():
        data[key] = find_element_or_placeholder(selector)
    
    return data

total_data = []
run_again = []

# Go to links and scrape pages
for count, link in enumerate(df_link['Link'], start=1):
    scraped_data = {'Language': 'English', 'Card number': count}
    
    try:
        scraped_data.update(scrape_elements(link))
        scraped_data['Link'] = link
        total_data.append(scraped_data)
    except:
        # Put placeholders into empty rows for all columns except 'Link' and 'Card number'
        placeholder_data = {'Language': 'English', 'Card number': count, 'Link': link}
        for key in selectors.keys():
            if key not in ['Link', 'Card number']:
                placeholder_data[key] = '________________________'
        total_data.append(placeholder_data)
        print(f"__________{count}_________")
        run_again.append(count)
        continue

driver.quit()

# Convert the list of dictionaries into a DataFrame
total_df = pd.DataFrame(total_data)
total_df['Date of extraction'] = date.today().strftime("%Y-%m-%d")

# Save the DataFrame to an Excel file
total_df.to_excel('scraped_again_2.xlsx', index=False)

# Print indices of unscraped pages
print(run_again)