# Python Imports
from datetime import datetime
import string
import time
import math
import pandas as pd

# External library imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException

joblist_infocomm = [
    "ict sales professional",
    "marketing manager",
    "product analyst",
    "product manager",
    "product designer",
    "business intelligence professional",
    "infrastructure engineer",
    "computer systems analyst",
    "software infrastructure architect",
    "web developer",
    "software developer",
    "app developer",
    "user interface designer",
    "software engineer",
    "software architect",
    "software quality assurance analysts and testers",
    "embedded systems engineer",
    "web and digital interface designers",
    "database infrastructure engineer",
    "network architect",
    "database administrator",
    "database architect",
    "network and computer systems administrator",
    "artificial intelligence engineer",
    "machine learning engineer",
    "data science engineer",
    "data analyst",
    "data scientist",
    "artificial intelligence scientist",
    "data architect",
    "ict security specialist",
    "it security operations",
    "information security analyst",
    "product security and it security integration specialist",
    "product risk specialist",
    "security architect",
    "database support engineer",
    "data center operations engineer",
    "support systems engineer",
    "computer network support specialist"
]

# Driver configurations
_service = ChromeService(ChromeDriverManager().install())
_option= webdriver.ChromeOptions()
driver = webdriver.Chrome(service = _service, options = _option)

# Pagination & HTML definitions
PAGINATION_URL = "https://www.occ.com.mx/empleos/de-{}/en-{}/?page={}"
LOCATION = "Mexico"
XPATH_RESULTADOS_1 = "/html/body/main/div[4]/aside/div/div[1]/p"
XPATH_RESULTADOS_2 = "/html/body/div[1]/div[1]/div[7]/div/div[1]/div[1]/div[1]/p"
CSS_SELECTOR_JOBCARD = "div[id^=jobcard]"
CSS_SELECTOR_JOBCARD_TITLE = "#{} > div > h2"
CSS_SELECTOR_JOB_INFO = "body > main > div.sm\:container.sm\:mx-auto.grid.grid-cols-12 > div > div > div.mb-8.break-words"
CSS_SELECTOR_JOB_INFO_2= "#jobbody"

def find_job_elements(h2,
                      description_list: list,
                      job_title_list: list,
                      job_url_list: list):
    """ Find job elements """
    titulo = h2[0].text
    job_title_list.append(titulo)
    try:
        h2[0].click()
        job_url = driver.current_url
        job_url_list.append(job_url)
        time.sleep(1.3)
        description = driver.find_elements(by=By.CSS_SELECTOR,
                                           value = CSS_SELECTOR_JOB_INFO)
        if len(description) > 0:
            for description_text in description:
                description_list.append(description_text.text)
        else:
            time.sleep(0.5)
            description = driver.find_elements(by=By.CSS_SELECTOR, 
                                               value = CSS_SELECTOR_JOB_INFO_2)
            if len(description) > 0:
                for description_text in description:
                    description_list.append(description_text.text)
            else:
                description_list.append("")
    except ElementClickInterceptedException:
        print("Error: ElementClickInterceptedException")
        job_url_list.append("error")
        description_list.append("error")

    return job_title_list, description_list, job_url_list

def obtain_descriptions(jobs_found_list,
                        jobs_ids):
    """ Obtain descriptions """
    description_list = []
    job_title_list = []
    job_url_list = []
    for jobcard, id_html in zip(jobs_found_list, jobs_ids):
        solo_id = id_html.split("-")[1]
        solo_id = solo_id.strip()
        css_selector = CSS_SELECTOR_JOBCARD_TITLE.format(id_html)
        h2 = jobcard.find_elements(by=By.CSS_SELECTOR,
                                   value=css_selector)
        if len(h2) > 0:
            description_list, job_title_list, job_url_list = find_job_elements(h2,
                                                                               description_list,
                                                                               job_title_list,
                                                                               job_url_list)
        else:
            time.sleep(0.5)
            h2 = jobcard.find_elements(by=By.TAG_NAME,value="h2")
            if len(h2) > 0:
                description_list, job_title_list, job_url_list = find_job_elements(h2,
                                                                                   description_list,
                                                                                   job_title_list,
                                                                                   job_url_list)
            else:
                print("No Job Title to click")
    return job_title_list, description_list, job_url_list

def prepare_data_frame(list_of_titles, 
                       descriptions_list, 
                       list_of_urls, 
                       job):
    """ Prepare data frame """
    current_date = datetime.now().strftime("%Y-%m-%d")
    csv_route = "CSVInfo2V2/"
    csv_filename = csv_route + job + "-" + str(current_date) +".csv"
    df = pd.DataFrame({'Job_Title': list_of_titles, 'Job_Description': descriptions_list, 'Job_Url': list_of_urls})
    df.to_csv(csv_filename, index=False)

def calculate_num_pages(num_resultados: int, max_resultados = 100) -> int:
    """ Calculate number of pages for a resulting Job """
    total_pages = math.ceil(num_resultados / 20)
    total_pages = min(total_pages, math.ceil(max_resultados / 20))
    return total_pages

def scrap_job_infos(job: string) -> int:
    """ Main entering to LinkedIn webpage """
    driver.get(PAGINATION_URL.format(job, LOCATION, 1))
    time.sleep(1.5)
    resultados = driver.find_elements(by=By.XPATH,
                                      value=XPATH_RESULTADOS_1)
    # if len(resultados) == 0:
    #     resultados = driver.find_elements(by=By.XPATH,
    #                                       value=XPATH_RESULTADOS_2)
    # total = 0
    if resultados:
        print(resultados[0].text)
    else:
        print(int("0"))
    # numero_resultados = int((resultados[0].text.split(" ")[0]).replace(",","")) if resultados else int("0")
    # print(numero_resultados)
    # numero_paginas = calculate_num_pages(numero_resultados, max_resultados=100)
    # if numero_paginas == 1:
    #     descriptions_list =[]
    #     jobs_ids = []
    #     jobs_found_list = driver.find_elements(by=By.CSS_SELECTOR,
    #                                            value=CSS_SELECTOR_JOBCARD)
    #     for job in jobs_found_list:
    #         try:
    #             id_html = job.get_attribute("id")
    #             jobs_ids.append(id_html)
    #         except StaleElementReferenceException:
    #             print("ID No encontrado")
    #     if len(jobs_found_list) > 0:
    #         list_of_titles, descriptions_list, list_of_urls = obtain_descriptions(jobs_found_list, jobs_ids)
    #         total = total + len(descriptions_list)
    #         prepare_data_frame(list_of_titles, descriptions_list, list_of_urls, job)

    # elif numero_paginas > 1:
    #     titlesListConca = []
    #     descriptionsListConca = []
    #     urlsListConca= []
    #     for i in range(1, numero_paginas + 1):
    #         descriptionsList=[]
    #         jobsIDs = []
    #         driver.get(PAGINATION_URL.format(job, LOCATION, i))
    #         time.sleep(0.5)
    #         jobsFoundList = driver.find_elements(by=By.CSS_SELECTOR, value=cssSelector_Jobcard)
    #         for i in jobsFoundList:
    #             try:
    #                 id_html = i.get_attribute("id")
    #                 jobsIDs.append(id_html)
    #             except StaleElementReferenceException:
    #                 print("ID No encontrado")
    #         listOfTitles, descriptionsList, listOfUrls = obtain_descriptions(jobsFoundList,jobsIDs)
    #         descriptionsListConca.extend(descriptionsList)
    #         titlesListConca.extend(listOfTitles)
    #         urlsListConca.extend(listOfUrls)
    #     total = total + len(descriptionsListConca)
    #     for l in descriptionsListConca:
    #         l = l.replace(","," ")
    #     prepareDataFrame(titlesListConca, descriptionsListConca, urlsListConca,job_)
    # return total
    return 1

def main():
    """ Main function call for Web Scrapper """
    total_jobs = 0
    for job_ in joblist_infocomm:
        job_ = job_.replace(" ","%20")
        total = scrap_job_infos(job_)
        total_jobs = total_jobs + total

    driver.close()
    driver.quit()

    print("\n")
    print(f"\nTotal Job posts extracted: {total_jobs}")

if __name__ == "__main__":
    main()
