import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date

from selenium import webdriver # for bot
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


class bot_jobteaser:
    def __init__(self):
        # link Data Engineer
        linkDE = 'https://www.jobteaser.com/en/job-offers?locale=en&q=Data+Engineer&abroad_only=false&location=Germany&page=1'

        # Data Analyst
        linkDA = 'https://www.jobteaser.com/en/job-offers?locale=en&q=Data+Analyst&abroad_only=false&location=Germany&page=1'

        links_to_bot = {'Data Engineer':linkDE, 
                        'Data Analyst':linkDA
                       }

        total_df = pd.DataFrame(columns = ['date_of_extraction','websource','search_job','title', 'company', 
                                           'location', 'duration','date_of_posting','reference','other_info',
                                           'compagination'
                                          ])

        for key in links_to_bot:
            print(f'Starting with : {key}')
            data_link = self.requests_jobteaser(key = key, url = links_to_bot[key])
            total_df = pd.concat(objs = [total_df, data_link], ignore_index = True)
            
        prefix = date.today().strftime('%Y%m%d')
        total_df.to_excel(f"{prefix}_job_listings_jobteaser.xlsx")
        
        
    def requests_jobteaser(self, key, url):
        # Important headers to make this requests instance work
        headers = {
            'Origin':'https://www.jobteaser.com',
            'Referer':'https://www.jobteaser.com/',
            'Sec-Ch-Ua':'"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }

        i = 1
        data = []
        while True:
            response = requests.get(url, headers = headers)
            if response:
                soup = BeautifulSoup(response.content, 'html.parser')
                job_listings = soup.find('ul',class_='Results_main__fyiWs')

                for job in job_listings:
                    company_name = job.find('p', class_='text_jds-Text__15y8h').text
                    card_title = job.find('a', class_='link_jds-Link__IVm1_').text
                    link = job.find('a', class_='link_jds-Link__IVm1_').get('href')
                    all_spans = job.find_all('span', class_='text_jds-Text__15y8h')
                    duration = all_spans[0].text
                    location = all_spans[1].text
                    if job.find('span', class_ = 'sk-Badge_label__f1crk') is None:
                        posting_time = job.find('time', class_ = 'text_jds-Text__15y8h').text
                    else:
                        posting_time = job.find('span', class_ = 'sk-Badge_label__f1crk').text

                    data.append({'date_of_extraction':str(date.today()),
                                 'websource': 'JobTeaser',
                                 'search_job': key,
                                 'title': card_title, 
                                 'company': company_name, 
                                 'location': location,
                                 'duration': duration,
                                 'date_of_posting':posting_time,
                                 'other_info':'--',
                                 'reference': 'https://www.jobteaser.com'+link,
                                 'compagination': i
                                })

                print(f'It. {i} is done!')
                time.sleep(3)
                # print(soup.find('button', attrs={'disabled': True}))
                next_page = soup.find('button', attrs={'disabled': True})
                # print(next_page == None)
                # print(i, next_page)
                if (next_page == None) | ((next_page != None) & (i == 1)):
                    print('Proceeding with next link:')
                    i += 1
                    url = f'https://www.jobteaser.com/en/job-offers?locale=en&q=Data+Engineer&abroad_only=false&location=Germany&page={i}'
                    print(url)
                    time.sleep(3)
                else:
                    print('Ran out of pages!')
                    break
            else:
                print(f'Request not working at it. {i}')
                break

        df = pd.DataFrame(data)
        return df
    
    
    
class bot_stellen:
    def __init__(self):
        
        # link Data Engineer
        linkDE = 'https://www.stellenanzeigen.de/suche/?fulltext=Data+Engineer&locationId=C-DE'

        # Data Analyst
        linkDA = 'https://www.stellenanzeigen.de/suche/?fulltext=Data+Analyst&locationId=C-DE'

        links_to_bot = {'Data Engineer':linkDE, 
                        'Data Analyst':linkDA
                       }

        total_df = pd.DataFrame(columns = ['date_of_extraction','websource','search_job','title', 'company', 
                                           'location', 'duration','date_of_posting','reference','other_info',
                                           'compagination'
                                          ])

        for key in links_to_bot:
            data_link = self.requests_stellen(key = key, url = links_to_bot[key])
            total_df = pd.concat(objs = [total_df, data_link], ignore_index = True)
            
        prefix = date.today().strftime('%Y%m%d')
        total_df.to_excel(f"{prefix}_job_listings_stellenanzeigen.xlsx")

    def requests_stellen(self, key, url):

        headers = {
            'Sec-Ch-Ua':'"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }

        response = requests.get(url)
        if response:
            soup = BeautifulSoup(response.content, 'html.parser')
            job_listings = soup.find('div',class_='sc-69fa95f4-0 eYDOmr')

            data = []

            for job in job_listings:   
                card_title = job.find('a', class_ = 'sc-e7795f3a-14').get('title')
                company_name = job.find('p', class_='sc-e7795f3a-7').text
                link = job.find('a', class_ = 'sc-e7795f3a-14').get('href')
                posting_time = job.find('p', class_ = 'sc-e7795f3a-9 eJFpjF').text
                location = job.find('span', class_ = 'sc-e7795f3a-17 htiqgX').text

                data.append({'date_of_extraction':str(date.today()),
                             'websource': 'stellenanzeigen.de',
                             'search_job': key,
                             'title': card_title, 
                             'company': company_name, 
                             'location': location,
                             'duration': '--',
                             'date_of_posting':posting_time,
                             'other_info':'--',
                             'reference': 'https://www.stellenanzeigen.de'+link,
                             'compagination': '--'
                            })

            df = pd.DataFrame(data)

            return df
        
        
        
class bot_indeed:
    def __init__(self):
        # link Data Engineer
        linkDE = 'https://de.indeed.com/jobs?q=Data%20Engineer&l=Deutschland&&start=10'

        # Data Analyst
        linkDA = 'https://de.indeed.com/jobs?q=Data%20Analyst&l=Deutschland&&start=10'

        links_to_bot = {'Data Engineer':linkDE, 
                        'Data Analyst':linkDA
                       }

        total_df = pd.DataFrame(columns = ['date_of_extraction','websource','search_job','title', 'company', 
                                           'location', 'duration','date_of_posting','reference','other_info',
                                           'compagination'
                                          ])

        for key in links_to_bot:
            data_link = self.scrape_indeed(key = key, url = links_to_bot[key])
            total_df = pd.concat(objs = [total_df, data_link], ignore_index = True)
             
        prefix = date.today().strftime('%Y%m%d')
        total_df.to_excel(f"{prefix}_job_listings_indeed.xlsx")
        
        
    def scrape_indeed(self, key, url):
        service = Service()
        options = webdriver.ChromeOptions()

    #     options.add_argument("--headless")
        options.add_argument("--disable-gpu")

        options.add_argument('disable-infobars')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-blink-features')
        options.add_argument('--profile-directory=Default')
        options.add_argument('--disable-plugins-discovery')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches',['enable-automation'])
        options.add_experimental_option('useAutomationExtension',False)

        browser = webdriver.Chrome(service = service, options = options)
        browser.get(url)
        time.sleep(2)

        data = []
        max_pages = 9
        for j in range(2, max_pages + 2):
            job_listings = browser.find_elements(By.CSS_SELECTOR, '.resultContent')
            total_i = len(job_listings)
            for i, job in enumerate(job_listings):
                link_element = job.find_element(By.CSS_SELECTOR, 'h2.jobTitle a[href]')
                link = link_element.get_attribute('href')
                # Extract the job title
                title_element = job.find_element(By.CSS_SELECTOR, 'h2.jobTitle span[title]')
                title = title_element.text

                # Extract other info
    #             other_info_element = job.find_element(By.CSS_SELECTOR, 'div.jobMetaDataGroup [data-testid="attribute_snippet_testid"]')
    #             other_info = other_info_element.text
    #             print(other_info)
                # Extract the company name
                company_element = job.find_element(By.CSS_SELECTOR, 'div.company_location [data-testid="company-name"]')
                company = company_element.text

                # Extract the location
                location_element = job.find_element(By.CSS_SELECTOR, 'div.company_location [data-testid="text-location"]')
                location = location_element.text

                state_date_element = browser.find_element(By.CSS_SELECTOR, 'span[data-testid="myJobsStateDate"]')
                date_of_posting = state_date_element.text

                data.append({'date_of_extraction':str(date.today()),
                             'websource': 'indeed',
                             'search_job':key,
                             'title': title, 
                             'company': company, 
                             'location': location, 
                             'duration':'--',
                             'date_of_posting': date_of_posting,
                             'reference':link,
                             'other_info':'--',
                             'compagination' : j
                            })
                print(f'{i} of {total_i}')
            next_page_button = browser.find_element(By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"]')
            browser.execute_script("arguments[0].click();", next_page_button)
            print('Changing page')
            time.sleep(5)
            unchanged_web = True
            while unchanged_web:
                current_url = str(browser.current_url)
                print(f'&start={j}0')
                if f'&start={j}0' in current_url:
                    unchanged_web = False
                else:
                    time.sleep(3)

        browser.close()
        df = pd.DataFrame(data)

        return df
    
    
class bot_workwise:
    def __init__(self):
        # link Data Engineer
        linkDE = 'https://www.workwise.io/jobsuche?search_id=140401002&page=1&id=16124'

        # Data Analyst
        linkDA = 'https://www.workwise.io/jobsuche?search_id=140401238&page=1&id=88454'

        links_to_bot = {'Data Engineer':linkDE, 
                        'Data Analyst':linkDA
                       }

        total_df = pd.DataFrame(columns = ['date_of_extraction','websource','search_job','title', 'company', 
                                           'location', 'duration','date_of_posting','reference','other_info',
                                           'compagination'
                                          ])

        for key in links_to_bot:
            data_link = self.selenium_workwise(key = key, url = links_to_bot[key])
            total_df = pd.concat(objs = [total_df, data_link], ignore_index = True)    
            
        prefix = date.today().strftime('%Y%m%d')
        total_df.to_excel(f"{prefix}_job_listings_workwise.xlsx")
        
    def selenium_workwise(self, key, url):
        service = Service()
        options = webdriver.ChromeOptions()

        # options.add_argument("--headless")
        # options.add_argument("--incognito")
        options.add_argument("--disable-gpu")

        options.add_argument('--disable-infobars')
        options.add_argument('--disable-cookies')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-blink-features')
        options.add_argument('--profile-directory=Default')
        options.add_argument('--disable-plugins-discovery')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches',['enable-automation'])
        options.add_experimental_option('useAutomationExtension',False)


        driver = webdriver.Chrome(service=service, options = options)

        # Replace 'url' with the URL you want to scrape
        url = 'https://www.workwise.io/jobsuche?search_id=140401002&page=1&id=16124'
        driver.get(url)

        # Find all job listings
        time.sleep(1)
        print('Getting HTML...')
        try:
            time.sleep(5)
            # Wait for the span element to appear for a maximum of 10 seconds
            elem_h4 = driver.find_element(by = 'xpath', value = '//h4[@class="sc-d36d06f9-0 inPmyu"]')
            print("Span found:", elem_h4.text)
            cookies_button = driver.find_element(by = 'xpath', value = '//button[@class="sc-554faedc-2 jgDpKf sc-486347bd-0 enjVkD"]')
            cookies_button.click()
            time.sleep(1)

            # You can continue your script here using the 'span' variable
        except:
            print("Span did not appear within 10 seconds. Continuing...")

        time.sleep(1)

        data = []
        j = 1
        while True:
            lol = driver.page_source
            print('Getting soup...')
            soup = BeautifulSoup(lol,'html.parser')
            job_listings = soup.find_all('div', class_ = 'sc-2c82bd37-0 haQhb')

            for i, job in enumerate(job_listings):
                title = job.find('div', class_ = 'sc-2c82bd37-0 sc-e2ccb30b-0 hBLdhE bdzvMe').text
                company = job.find('div', class_ = 'sc-2c82bd37-0 sc-e2ccb30b-0 jGGNQN dvQAce').text
                link = job.find('a', class_ = 'sc-554faedc-1').get('href') 
                place_n_office = job.find_all('p', class_ = 'sc-9cc15fd9-0 iNsLIe')
                location = place_n_office[0].text
                homeoffice = place_n_office[1].text
                other_info = job.find_all('p', class_="sc-9cc15fd9-0 iyPKpw")
                other_info = [i.text for i in other_info]
                other_info.append(homeoffice)

                data.append({'date_of_extraction':str(date.today()),
                             'websource': 'Workwise',
                             'search_job':key,
                             'title': title, 
                             'company': company, 
                             'location': location, 
                             'duration':'--',
                             'date_of_posting': '--',
                             'reference':'https://www.workwise.io/'+link,
                             'other_info':other_info,
                             'compagination' : j
                            })

            if soup.find('svg', class_ = 'sc-21a3677b-0 eBxGKb') == None:
                print('All done!')
                break
            else:
                print('There is another webpage to bot')

                button_login = driver.find_element(by = 'xpath', value = '//button[@class="sc-554faedc-2 jgDpKf sc-486347bd-0 vGbzf"]')
                button_login.click()
                time.sleep(5)
                j += 1

        driver.quit()

        df = pd.DataFrame(data)
        return df
    
    
if __name__ == "__main__":
    a = bot_jobteaser()
    b = bot_stellen()
    c = bot_indeed()
    d = bot_workwise()