from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time
import datetime
import logging
import random
import argparse
import pandas as pd
from tqdm import tqdm

from selenium.webdriver.chrome.service import Service

infocomm_jobs = ["Software Developer",
    "Systems Engineer", 
    "Data Analyst",
    "Data Scientist",
    "Network Engineer",
    "Web Developer",
    "Database Administrator",
    "IT Security Specialist",
    "Telecommunications Engineer",
    "Business Analyst",
    "BI Analyst (Business Intelligence)",
    "Business Analytics Consultant",
    "Business Analysis Specialist",
    "Cybersecurity Analyst",
    "Information Security Manager",  "Cybersecurity Consultant",
    "Penetration Tester",
    "Ethical Hacker",
    "Security Architect",
    "Network Security Engineer",
    "Information Assurance Analyst",
    "Incident Response Analyst",
    "Vulnerability Analyst",
    "Compliance Analyst",
    "Security Software Developer","IT Project Manager",
    "Technical Project Manager",
    "Digital Project Manager",
    "Agile Project Manager",
    "Scrum Master",
    "Program Manager",
    "Project Coordinator",
    "Project Analyst",
    "Portfolio Manager",
    "PMO Analyst (Project Management Office Analyst)",
    "Change Management Specialist",
    "Implementation Manager",
    "Project Lead",
    "Product Owner",
    "DevOps Engineer",
    "Cloud Architect",    
    "Systems Administrator",
    "IT Support Specialist",
    "Network Administrator",
    "IT Consultant",
    "Technical Support Engineer",
    "Cybersecurity Engineer",
    "IT Auditor",
    "Quality Assurance Analyst",
    "IT Trainer",
    "Network Operations Center (NOC) Technician"]

class LinkedIn_bot:
    def __init__(self):
        service = Service()
        options = webdriver.ChromeOptions()
        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt)
        # chromedriver_autoinstaller.install()
        # logging.info(chromedriver_autoinstaller.get_chrome_version())
        logging.info("Starting driver")
        self.driver = webdriver.Chrome(service=service, options=options)
        logging.info("Initialization successful")
        logging.warning("This automated scraper uses few seconds of random waits throughout the whole process to mimic human behaviour!")

    def random_wait(self, a=4, b=6):
        '''Wait a random amount of time'''
        if type(a) == int:
            delay = random.randint(a, b)
        else:
            delay = random.uniform(a, b)
        time.sleep(delay)

    def search_jobs(self, job_title='', location='United States'):
        '''Enter tags and search'''
        self.driver.get("https://www.linkedin.com/jobs/search")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "job-search-bar-keywords"))
        )
        search_job_name_input = self.driver.find_element(by=By.ID, value="job-search-bar-keywords")
        search_job_name_input.send_keys(Keys.CONTROL + "a")
        search_job_name_input.send_keys(Keys.DELETE)
        search_job_name_input.send_keys(job_title)

        search_job_location_input = self.driver.find_element(by=By.ID, value="job-search-bar-location")
        search_job_location_input.send_keys(Keys.CONTROL + "a")
        search_job_location_input.send_keys(Keys.DELETE)
        search_job_location_input.send_keys(location)

        search_button = self.driver.find_element(by=By.XPATH, value='//button[@data-tracking-control-name="public_jobs_jobs-search-bar_base-search-bar-search-submit"]')
        search_button.click()
        logging.info(f"Search for '{job_title}' in '{location}' successful")

    def load_all_results(self, max_page):
        '''Scroll through the whole page to load all the job search results'''
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll = True
        scroll_page = 1

        while scroll:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.random_wait()
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height or scroll_page == max_page:
                scroll = False
            else:
                last_height = new_height
                scroll_page += 1
        logging.info("Successfully loaded all search results.")

    def time_ago_to_month_year(self, time_ago):
        '''Calculate the job posting month'''
        dic_to_days = {'minute': 0, 'hour': 0, 'day': 1, 'week': 7, 'month': 30, 'year': 365}
        p = list(time_ago.split('ago')[0].strip())
        if p[-1] == 's':
            p[-1] = ''
        p = ''.join(p).split(' ')
        delta_days = int(p[0]) * dic_to_days[p[1]]

        today = datetime.date.today()
        date = today - datetime.timedelta(days=delta_days)
        job_post_month = date.strftime("%B")
        job_post_year = date.strftime("%Y")
        return job_post_month, job_post_year

    def close_session(self):
        '''This function closes the current session'''
        logging.info("Closing session")
        self.driver.close()

    def run(self, job_title, location, max_pages=40):
        '''Running the bot to extract all the job search results data'''
        self.results_dic = {'Position': [], 'Company_Name': [], 'Location': [], 'Post_Month': [], 'Post_Year': [], 'Details': []}
        self.search_jobs(job_title, location)
        self.load_all_results(max_pages)

        list_items = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list"))
        )
        jobs_list = list_items.find_elements(by=By.TAG_NAME, value="li")
        nbr_jobs = len(jobs_list)
        logging.info(f"{nbr_jobs} jobs found")

        for job in tqdm(jobs_list, desc="Extracting Job Offers Details"):
            self.driver.execute_script("arguments[0].scrollIntoView();", job)
            job.click()
            self.random_wait()
            try:
                show_more = self.driver.find_element(by=By.CLASS_NAME, value="show-more-less-html__button")
                show_more.click()
            except:
                continue
            self.random_wait()

            [position, company, location, *remaining] = job.text.split('\n')
            try:
                time_ago = self.driver.find_element(by=By.XPATH, value="//span[@class='posted-time-ago__text topcard__flavor--metadata']").text
            except:
                try:
                    time_ago = remaining[-1]
                except:
                    time_ago = "10 years ago"

            try:
                details = self.driver.find_element(by=By.XPATH, value="//div[@class='show-more-less-html__markup relative overflow-hidden']").text
            except:
                details = ''
                continue

            job_post_month, job_post_year = self.time_ago_to_month_year(time_ago)

            self.results_dic['Position'].append(position)
            self.results_dic['Company_Name'].append(company)
            self.results_dic['Location'].append(location)
            self.results_dic['Post_Month'].append(job_post_month)
            self.results_dic['Post_Year'].append(job_post_year)
            self.results_dic['Details'].append(details)

        logging.info("Done scraping.")
        self.close_session()

        return self.results_dic

def parse_args():
    parser = argparse.ArgumentParser(description='LinkedIn Bot job search')
    parser.add_argument('--job-title', metavar='Job_title', default='Data Analyst', type=str, help='Enter a valid job title, e.g. Data Analyst.')
    parser.add_argument('--location', metavar='Location', default='Mexico', type=str, help='Enter the location "Country" or "City, Country" where to search for job offers.')
    parser.add_argument('--max-pages', metavar='Maximum_pages', default=40, type=int, help='Enter the maximum number of pages to load.')
    return parser.parse_args()

def generate_file_name(job_title, location, max_pages=40):
    today = datetime.date.today().strftime("%d-%m-%Y")
    name = f'results_{job_title}_{location}_{max_pages}pages_{today}'
    return name

if __name__ == "__main__":
    # args = parse_args()
    location = "México"
    max_pages = 40
    bot = LinkedIn_bot()

    for job_title in infocomm_jobs:
        results_dic = bot.run(job_title, location, max_pages)
        # results_dic = bot.run(**vars(args))
        results_df = pd.DataFrame(results_dic)
        # file_name = generate_file_name(**vars(args))
        file_name = generate_file_name(job_title, location, max_pages)
        results_df.to_csv(f'./{file_name}.csv', index=False)
        logging.info(f"Results for {job_title} saved in {file_name}.csv")

    bot.driver.quit()
