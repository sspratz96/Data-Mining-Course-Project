#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import pandas as pd

class JobScraper:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_jobs(self):
        """Extract job data from a single HTML file."""
        with open(self.file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        company_names, company_ratings, job_titles, job_locations = [], [], [], []

        for company_name in soup.find_all('span', class_='EmployerProfile_compactEmployerName__LE242'):
            company_names.append(company_name.text.strip())

        for rating_container in soup.find_all('div', class_='EmployerProfile_ratingContainer__ul0Ef'):
            rating = rating_container.find('span')
            company_ratings.append(rating.text.strip() if rating else 'Not rated')

        for job_title in soup.find_all('a', class_='JobCard_jobTitle___7I6y'):
            job_titles.append(job_title.text.strip())

        for location in soup.find_all('div', class_='JobCard_location__rCz3x'):
            job_locations.append(location.text.strip())

        jobs_data = [{
            'Company Name': company_names[i] if i < len(company_names) else 'Not listed',
            'Rating': company_ratings[i] if i < len(company_ratings) else 'Not rated',
            'Job Title': job_titles[i] if i < len(job_titles) else 'No title',
            'Location': job_locations[i] if i < len(job_locations) else 'No location',
        } for i in range(len(job_titles))]

        return pd.DataFrame(jobs_data)

    @classmethod
    def process_files(cls, file_paths):
        """Process multiple HTML files and combine the results into a single DataFrame."""
        all_jobs_df = pd.DataFrame()

        for file_path in file_paths:
            scraper = cls(file_path)
            df = scraper.extract_jobs()
            all_jobs_df = pd.concat([all_jobs_df, df], ignore_index=True)

        return all_jobs_df

# List of file paths
file_paths = [
    'data_analyst_Jobs_in_Germany_April_2024_Glassdoor.html',
    'data_engineer_Jobs_in_Germany_April_2024_Glassdoor.html',
    'data_scientist_Jobs_in_Germany_April_2024_Glassdoor.html'
]

# Process all files and print the combined DataFrame
all_jobs_df = JobScraper.process_files(file_paths)
print(all_jobs_df)


# In[2]:


# Export DataFrame to a CSV file
all_jobs_df.to_csv('glassdoor_data_professionals_listings.csv', index=False)


# In[ ]:




