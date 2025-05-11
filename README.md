# 📊 Data Mining Project: Job Market Analysis for Data Professionals in Germany (2024)

Welcome to our data mining project for the **Data Mining and Knowledge Discovery** course (2024). This repository explores current job market trends for **Data Scientists**, **Data Analysts**, and **Data Engineers** in Germany using data scraped from Glassdoor in April 2024.

---

## 🔍 Objective

Our goal was to extract and analyze job listings to answer:
- What skills and tools are most in demand for data roles in Germany?
- How do requirements differ between job titles?
- What regional patterns or salary expectations can be observed?

---

## 🛠️ Technologies Used

- **Python** for data processing and analysis
- **BeautifulSoup** for web scraping
- **Pandas & NumPy** for data wrangling
- **Matplotlib & Seaborn** for visualizations
- **Jupyter Notebooks** for exploratory analysis
- **Excel & HTML** for supplementary data and scraping output

---

## 📁 Repository Structure

| File/Folder | Description |
|------------|-------------|
| `Data_professionals_Glassdoor.py` | Web scraper script used to collect job data from Glassdoor |
| `*.html` | Raw HTML pages of job listings per role |
| `all_datasets.xlsx` | Consolidated dataset of all roles and job listings |
| `Job_Analysis_Data.ipynb` | Core analysis notebook (skills, location, trends) |
| `Data_professionals_Glassdoor.ipynb` | Notebook demonstrating scraping logic and samples |
| `*.pptx / *.pdf` | Final presentations summarizing findings and insights |

---

## 📈 Key Insights

- **Top Skills**: Python, SQL, and machine learning dominate job requirements.
- **Role Differences**: Data Engineers skew toward cloud and ETL tools; Data Analysts prioritize BI tools like Power BI or Tableau.
- **Geographic Hotspots**: Berlin, Munich, and Frankfurt lead in job postings.
- **Remote Work**: Remote roles are growing but still under 20% of total listings.

(Full analysis available in the presentation slides)

---

## 📌 How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/sspratz/Data-Mining-Project-Constructor-2024
   cd Data-Mining-Project-Constructor-2024
   ```

2. (Optional) Create a virtual environment and install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the notebooks or the scraper script (only if scraping is enabled).

---

## 👨‍👩‍👧‍👦 Authors

Group 5 — Data Mining & Knowledge Discovery 2024  
(Include names or initials if appropriate)

---

## 📄 License

This project is for academic purposes only. All scraped data is public and used under fair use for research.
